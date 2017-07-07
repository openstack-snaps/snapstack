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
        @param list setup_steps: A list of Step objects.
        @param list test_steps: A list of Step objects.
        @param list cleanup_steps: A list of Step objects.

        '''
        self._tempdir = tempfile.TemporaryDirectory()
        self.tempdir = self._tempdir.name

        self._setup = setup or base.Setup().steps()
        self._cleanup = cleanup or base.Cleanup().steps()
        self._tests = tests or []

    def __call__(self, cleanup=True):
        '''
        Setup a snapstack on this machine, and run some basic smoke tests
        on it.

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
