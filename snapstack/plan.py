'''
A Plan is an ordered set of specs, comprising an integration test
for a snap inside of a temporary Openstack environment.

'''

import os
import subprocess
import tempfile

from snapstack import base


class Plan:
    '''

    '''
    def __init__(self, tests=None, test_cleanup=None, base_setup=None,
                 base_cleanup=None):
        '''
        @param list tests: A list of Step objects, comprising tests
          for a snap or snaps.
        @param list test_cleanup: A list of Step objects, comprising scripts
          that will cleanup after the tests. (These scripts will always run,
          even if a test fails or errors out.)
        @param list base_setup: A list of Step objects, comprising the setup
          for snapstack. You can customize this by initializing a base.Setup
          object, adding or removing Steps, then passing the return from that
          object's .steps method to this argument.
        @param list base_cleanup: A list of Step objects, comprising general
          cleanup for snapstack. Similar to the above, you can customize
          this with a base.Cleanup object.

        '''
        self._tempdir = tempfile.TemporaryDirectory()
        self.tempdir = self._tempdir.name

        self._base_setup = base.Setup().steps() if\
            base_setup is None else base_setup
        self._base_cleanup = base.Cleanup().steps() if\
            base_cleanup is None else base_cleanup

        self._tests = tests or []
        self._test_cleanup = test_cleanup or []

        self._http_proxy = os.environ.get('SNAPSTACK_HTTP_PROXY')
        self._https_proxy = os.environ.get('SNAPSTACK_HTTPS_PROXY')

    def deploy(self):
        '''
        Deploy the snaps in our plan, and run any auxillary scripts.

        '''
        for step in self._base_setup + self._tests:
            step.run(
                tempdir=self._tempdir,
                http_proxy=self._http_proxy,
                https_proxy=self._https_proxy)

    def destroy(self):
        '''
        Run any cleanup scripts that we have specified and remove any
        snaps that we have installed.

        '''

        for step in self._test_cleanup:
            step.run(tempdir=self._tempdir)

        for step in self._base_cleanup:
            step.run(tempdir=self._tempdir)

        for step in self._base_setup + self._tests:
            if not step.snap:
                continue
            subprocess.run(['sudo', 'snap', 'remove', step.snap])

    def run(self, cleanup=True):
        '''
        Execute all of our steps. Cleanup may be skipped.

        '''
        try:
            self.deploy()
        finally:
            if cleanup:
                self.destroy()
