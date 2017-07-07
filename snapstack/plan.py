'''
A Plan is an ordered set of specs, comprising an integration test
for a snap inside of a temporary Openstack environment.

'''

import subprocess
import tempfile

from snapstack import base


class Plan:
    '''

    '''
    def __init__(self, tests=None, setup=None, cleanup=None):
        '''
        @param list tests: A list of Step objects, comprising tests
          for a snap or snaps.
        @param list setup: A list of Step objects, comprising the setup for
          snapstack.
        @param list cleanup: A list of Step objects, comprising cleanup steps.

        '''
        self._tempdir = tempfile.TemporaryDirectory()
        self.tempdir = self._tempdir.name

        self._setup = setup or base.Setup().steps()
        self._cleanup = cleanup or base.Cleanup().steps()
        self._tests = tests or []

    def __call__(self, cleanup=True):
        '''
        Execute all of our steps. Cleanup may be skipped.

        '''
        try:
            for step in self._setup + self._tests:
                step(tempdir=self._tempdir)
        finally:
            if not cleanup:
                return

            for step in self._setup + self._tests:
                if not step.snap:
                    continue
                subprocess.run(['sudo', 'snap', 'remove', step.snap])

            for step in self._cleanup:
                step(tempdir=self._tempdir)
