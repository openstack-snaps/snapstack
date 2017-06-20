import logging
import os
import subprocess
import sys

from textwrap import dedent


class InfraFailure(Exception):
    pass


class TestFailure(Exception):
    pass


class Runner:
    '''
    The heart of snapstack: tools to build an openstack environemnt
    out of a "base" of snaps, deploy a new snap against it, then run a
    set of integration tests.

    '''

    DEFAULT_BASE = [
        # Setup
        {'location': '{snapstack}', 'tests': ['packages.sh', 'rabbitmq.sh',
                                              'database.sh']},
        {'snap': 'keystone', 'location': '{snapstack}',
         'tests': ['keystone.sh']},
        {'snap': 'nova', 'location': '{snapstack}', 'tests': ['nova.sh']},
        {'snap': 'neutron', 'location': '{snapstack}',
         'tests': ['neutron.sh']},
        {'snap': 'glance', 'location': '{snapstack}', 'tests': ['glance.sh']},
        {'snap': 'nova-hypervisor', 'location': '{snapstack}',
         'tests': ['nova-hypervisor.sh']},
        # Post install scripts
        {'location': '{snapstack}', 'tests': ['neutron-ext-net.sh']}
    ]

    LOCATION_VARS = {
        'snapstack': '',  # Just exists in the PATH.
        'github': 'https://github.com/openstack-snaps-span-',
        'local': 'tests/',
        'snap': None  # Filled in by _run
    }

    ADMIN_ENV = {
        'OS_PROJECT_DOMAIN_NAME': 'default',
        'OS_USER_DOMAIN_NAME': 'default',
        'OS_PROJECT_NAME': 'admin',
        'OS_USERNAME': 'admin',
        'OS_PASSWORD': 'keystone',
        'OS_AUTH_URL': 'http://localhost:35357',
        'OS_IDENTITY_API_VERSION': '3',
        'OS_IMAGE_API_VERSION': '2',
        'BASE_DIR': os.path.dirname(sys.modules[__name__].__file__)
    }

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
        self._base = self._validate_base(base or self.DEFAULT_BASE)

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
        if location.startswith('http') or location.startswith('ssh'):
            # TODO Fetch stuff from github when appropriate
            # TODO Need to figure out what to do with config files
            # when we do -- they currently live in
            # site-packages/snapstack/etc
            raise Exception('Github fetching not yet implemented')

        return ''.join([location, test])

    def _run(self, location, tests, snap=None):
        '''
        Given a snap name, 'location' designator, and list of tests, run
        the tests for that snap.

        (This may be the main snap for this runner, or a snap in the 'base')

        '''
        tests = tests or []
        if not tests:
            self.log.warning("No tests for {}{}".format(location, snap))

        location_vars = dict(self.LOCATION_VARS)  # Copy
        location_vars['snap'] = snap
        location = location.format(**location_vars)

        env = dict(os.environ)
        env.update(self.ADMIN_ENV)

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
