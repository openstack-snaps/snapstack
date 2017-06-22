'''
Harness for doing basic CI on a snap. To use this library, you should:

1) Import it into the tests for your snap.

2) Create an instance of the Runner class, and invoke its run and
cleanup routine, passing in your snap name, and pointers to shell
scripts that will install the snap, test it, and clean it up.

The runner is meant to be a fairly lighweight Python wrapper around
your shell scripts. It also serves as a lighweight wrapper around a
set of scripts that will setup a "base" openstack via a standard set
of snaps. You can define your own base if necessary.

The overarching purpose is to test the snap, rather than to
extensively test the underlying surface, so basic tests will usually
suffice.

'''

import logging
import os
import requests
import stat
import subprocess
import tempfile
from textwrap import dedent

from snapstack import config
from snapstack.errors import InfraFailure, TestFailure


class Runner:
    '''
    This is the heart of snapstack: tools to build an openstack environemnt
    out of a "base" of snaps, deploy a new snap against it, then run a
    set of lightweight integration tests.

    '''

    def __init__(self, snap, location='{local}', tests=None, base=None):
        '''
        @param string name: Name of the snap being tested.
        @param string location: location of the test scripts for this snap.
        @param list tests: List of scripts to execute in order.
        @param list base: collection of snap tests to run to setup a "base"
          environment.

        '''
        self.log = logging.getLogger()
        self._snap = snap
        self._location = location
        self._tests = tests
        self._base = self._validate_base(base or config.DEFAULT_BASE)
        self._tempdir = None

    @property
    def tempdir(self):
        '''
        Magic method that creates a temporary dir to store scripts in if
        none exists. Otherwise, returns the location.

        (The TemporaryDirectory object will clean itself up when it is
        destroyed, so we skip explit cleanup.)

        '''
        if self._tempdir is None:
            self._tempdir = tempfile.TemporaryDirectory()

        return self._tempdir.name

    def _validate_base(self, base):
        '''
        Do some basic validation of the specs for a base suite of tests.

        This could be expanded to check for invalid magic strings in
        the location, etc.

        '''
        for spec in base:
            if 'location' not in spec:
                raise InfraFailure(
                    "Invalid spec. Missing location for {}".format(spec))
            if 'tests' not in spec:
                raise InfraFailure(
                    "Invalid spec. Missing tests for {}".format(spec))
            if type(spec['tests']) != list:
                raise InfraFailure(
                    "Invalid spec. Tests must be a list. {}".format(spec))

        return base

    def _path(self, location, test):
        '''
        Given a 'location' and a test name, return a path that
        subprocess can use to execute the script.

        If the location is a remote location, fetch the script first.

        '''
        path_ = ''.join([location, test])
        if path_.startswith('https://'):
            # TODO: make this much more robust
            remote = requests.get(path_)
            remote.raise_for_status()
            new_path = os.sep.join([self.tempdir, test])
            with open(new_path, 'w') as f:
                f.write(remote.text)
            os.chmod(new_path, os.stat(new_path).st_mode | stat.S_IEXEC)

            path_ = new_path
        return path_

    def _run(self, location, tests, snap=None):
        '''
        Given a snap name, 'location' designator, and list of tests, run
        the tests for that snap.

        (This may be the main snap for this runner, or a snap in the 'base')

        '''
        tests = tests or []
        if not tests:
            self.log.warning("No tests for {}{}".format(location, snap))

        location_vars = dict(config.LOCATION_VARS)  # Copy
        location_vars['snap'] = snap
        location = location.format(**location_vars)

        env = dict(os.environ)
        env.update(config.ADMIN_ENV)

        if snap:
            # Run INSTALL_SNAP script first, which will install the
            # snap, of be a noop if the snap is already installed
            # (allows you to override the default install process).
            p = subprocess.run(
                [config.INSTALL_SNAP.format(snap=snap)],
                shell=True
            )
            if p.returncode > 0:
                raise InfraFailure("Failed to install snap {}".format(snap))

        for test in tests:
            script = self._path(location, test)
            p = subprocess.run([script], env=env)
            if p.returncode > 0:
                raise TestFailure(
                    'Failed to run test "{script}'.format(script=script))

    def run(self):
        '''
        Setup a snapstack on this machine, and run some basic smoke tests
        on it.

        '''
        for spec in self._base:
            try:
                self._run(**spec)
            except TestFailure as e:
                # Transform TestFailure here into an InfraFailure, to
                # help devs figure out just why the test failed.
                if self._snap != spec.get('snap'):
                    raise InfraFailure('Snapstack setup failed: {}'.format(e))

        if self._snap not in [spec.get('snap') for spec in self._base]:
            # Skip running tests separately for something that is
            # already smoke tested in the base.
            self._run(self._location, self._tests, self._snap)

    def cleanup(self):
        '''
        Tear snapstack down.

        '''
        # Uninstall snaps
        for spec in self._base:
            if not spec.get('snap'):
                continue
            subprocess.run(['sudo', 'snap', 'remove', spec['snap']])

        SQL_CLEANUP = dedent("""\
            sudo mysql -u root << EOF
            DROP DATABASE keystone;
            DROP DATABASE nova;
            DROP DATABASE nova_api;
            DROP DATABASE nova_cell0;
            DROP DATABASE neutron;
            DROP DATABASE glance;
            DROP DATABASE cinder;
            EOF""")
        subprocess.run([SQL_CLEANUP], shell=True)

        subprocess.run(
            ['sudo', 'rabbitmqctl', 'delete_user', 'openstack'])
