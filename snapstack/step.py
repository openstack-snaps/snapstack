'''
Define an individual step in a Plan.

'''

import logging
import os
import requests
import stat
import subprocess
import tempfile

from snapstack import config
from snapstack.errors import InfraFailure, TestFailure


class Step:
    '''
    A Step is a single Step in a Plan. Each step may do multiple
    things, including installing a snap, running setup scripts,
    running test scripts for a snap, and installing config files.

    '''
    def __init__(self, snap=None, script_loc='{local}', scripts=None,
                 files=None, snap_store=True, classic=False):
        '''
        @param string snap: The name of a snap, if any, to be installed in
          this Step.
        @param string script_loc: parent location of the test scripts for this
            snap. Possibly a url, possibly a relative or absolute path.
        @param list scripts: List of scripts, to execute in order.
        @param list files: List of config files that the scripts may need
          to reference.
        @param bool snap_store: if True, install the snap from the store.
          If False, install it from local source.
        @param bool classic: if True, install the snap with the --classic flag.

        '''
        self.log = logging.getLogger()
        self.snap = snap
        self._location = script_loc
        self._scripts = scripts or []
        self._files = files or []
        self._snap_store = snap_store
        self._tempdir = None
        self._classic = ' --classic' if classic else ''
        self._snap_build_proxy = None

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

    def _install_snap(self):
        '''
        Install a snap. This will be a noop if the snap is alrady installed.

        '''
        if not self._snap_store:
            env = dict(os.environ)
            if self._snap_build_proxy:
                env['HTTP_PROXY'] = self._snap_build_proxy
                env['HTTPS_PROXY'] = self._snap_build_proxy

            subprocess.run(["snapcraft", "clean"], env=env, check=True)
            subprocess.run(["snapcraft", "prime"], env=env, check=True)
            subprocess.run(
                ["sudo", "snap", "try", "--devmode", "prime/"],
                env=env,
                check=True
            )
            return

        # TODO: Add handling for channels?
        p = subprocess.run(
            [config.INSTALL_SNAP.format(
                snap=self.snap, classic=self._classic)],
            shell=True
        )
        if p.returncode > 0:
            raise InfraFailure(
                "Failed to install snap {}".format(self.snap))

    def run(self, tempdir=None, snap_build_proxy=None):
        '''
        Run the set of tests defined by this snap (or just download some
        config files, if the step has no executable components).

        '''

        if tempdir is not None:
            self._tempdir = tempdir
        if snap_build_proxy is not None:
            self._snap_build_proxy = snap_build_proxy

        location_vars = dict(config.LOCATION_VARS)  # Copy
        location_vars['snap'] = self.snap
        location = self._location.format(**location_vars)

        env = dict(os.environ)
        env.update({'BASE_DIR': self.tempdir})

        if self.snap:
            self._install_snap()

        for f in self._files:
            self._fetch(location, f)

        for script in self._scripts:
            script = self._fetch(location, script)
            p = subprocess.run([script], env=env)
            if p.returncode > 0:
                raise TestFailure(
                    'Failed to run test "{script}'.format(script=script))
