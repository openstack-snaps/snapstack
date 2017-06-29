'''
The main Runner class lives here; import it and invoke its .run
and .cleanup routines to test a snap.

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

    def __init__(self, snap, location='{local}', tests=None, files=None,
                 base=None, override_local_build=False):
        '''
        @param string name: Name of the snap being tested.
        @param string location: location of the test scripts for this snap.
        @param list tests: List of scripts to execute in order.
        @param list files: List of config files that we may need to reference.
        @param list base: collection of snap tests to run to setup a "base"
          environment.

        '''
        self.log = logging.getLogger()
        self._snap = snap
        self._location = location
        self._tests = tests
        self._files = files
        self._base = self._validate_base(base or config.DEFAULT_BASE)
        self._tempdir = None
        self._override = override_local_build

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
            if 'tests' not in spec and 'files' not in spec:
                raise InfraFailure(
                    "Invalid spec. Missing tests or files in {}".format(spec))
            if 'tests' in spec and type(spec['tests']) != list:
                raise InfraFailure(
                    "Invalid spec. Tests must be a list. {}".format(spec))
            if 'files' in spec and type(spec['files']) != list:
                raise InfraFailure(
                    "Invalid spec. Files must be a list. {}".format(spec))

        return base

    def _fetch(self, parent, rel_path):
        '''Given a parent location and a relative path to a file, return a
        local path to the file.

        If the parent location is a url, download the file first.

        '''
        path_ = ''.join([parent, rel_path])
        if path_.startswith('https://'):
            # Download remote file and write to disk.
            remote = requests.get(path_)
            remote.raise_for_status()
            new_path = os.sep.join([self.tempdir, rel_path])

            d = os.path.dirname(new_path)
            if not os.path.exists(d):
                os.makedirs(d)

            with open(new_path, 'w') as f:
                f.write(remote.text)
            os.chmod(new_path, os.stat(new_path).st_mode | stat.S_IEXEC)

            path_ = new_path
        return path_

    def _install_snap(self, snap):
        '''
        Install a snap. This will be a noop if the snap is alrady installed.

        '''
        if snap == self._snap and not self._override:
            # This is the snap that we are testing. Install it from
            # source, unless we've overridden this behavior (for
            # example, we are testing the version of a snap that has
            # been pushed to the store).
            # TODO: make this be based on channels, with a special
            # string for a "not in the snapstore" channel?
            subprocess.check_output(["snapcraft", "prime"])
            subprocess.check_output(
                ["sudo", "snap", "try", "--devmode", "prime/"])

            return

        p = subprocess.run(
            [config.INSTALL_SNAP.format(snap=snap, classic='')],
            shell=True
        )
        if p.returncode > 0:
            # Temp HACK: try to install in classic mode if
            # standard mode doesn't work.'
            p = subprocess.run(
                [config.INSTALL_SNAP.format(
                    snap=snap,
                    classic='--classic ')],
                shell=True)
            if p.returncode > 0:
                raise InfraFailure(
                    "Failed to install snap {}".format(snap))

    def _run(self, location, tests=None, snap=None, files=None):
        '''
        Run a set of tests, specified by a parent location, a list of
        test scripts to execute, and possibly a snap to install.

        Alternately, simply download a set of config files.

        '''
        tests = tests or []
        files = files or []

        location_vars = dict(config.LOCATION_VARS)  # Copy
        location_vars['snap'] = snap
        location = location.format(**location_vars)

        env = dict(os.environ)
        env.update({'BASE_DIR': self.tempdir})

        if snap:
            self._install_snap(snap)

        for f in files:
            self._fetch(location, f)

        for test in tests:
            script = self._fetch(location, test)
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
            self._run(self._location, self._tests, self._snap, self._files)

    def cleanup(self):
        '''
        Tear snapstack down.

        '''
        # Uninstall snaps
        for spec in self._base:
            if not spec.get('snap'):
                continue
            subprocess.run(['sudo', 'snap', 'remove', spec['snap']])

        if self._snap not in [spec.get('snap') for spec in self._base]:
            subprocess.run(['sudo', 'snap', 'remove', self._snap])

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
