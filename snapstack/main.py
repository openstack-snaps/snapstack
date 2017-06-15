import os
import subprocess


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
        {'name': 'packages', 'location': '{snapstack}',
         'tests': ['packages.sh']},  # TODO: make this cross-distro friendly
        {'name': 'rabbitmq', 'location': '{snapstack}',
         'tests': ['rabbitmq.sh']},
        {'name': 'database', 'location': '{snapstack}',
         'tests': ['database.sh']},
        {'name': 'keystone', 'location': '{snapstack}',
         'tests': ['keystone.sh']},
        {'name': 'nova', 'location': '{snapstack}', 'tests': ['nova.sh']},
        {'name': 'neutron', 'location': '{snapstack}',
         'tests': ['neutron.sh']},
        {'name': 'glance', 'location': '{snapstack}', 'tests': ['glance.sh']},
        {'name': 'nova-hypervisor', 'location': '{snapstack}',
         'tests': ['nova-hypervisor.sh']},
        {'name': 'neutron-ext-net', 'location': '{snapstack}',
         'tests': ['neutron-ext-net.sh']}
    ]

    LOCATION_VARS = {
        'snapstack': '../snapstack/scripts',  # TODO: just put default
                                              # scripts in path
        'github': 'https://github.com/openstack-snaps-span-',
        'local': 'tests',
        'name': None  # Filled in by _run
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
        'BASE_DIR': '.'  # TODO: put this stuff someplace sensible
    }

    def __init__(self, name, location='{local}', tests=None, base=None):
        '''
        @param string name: Name of the snap being tested.
        @param string location: location of the test scripts for this snap.
        @param list tests: List of scripts to execute in order.
        @param list base: collection of snap tests to run to setup a "base"
          environment.

        '''
        self._name = name
        self._location = location
        self._tests = tests
        self._base = self._validate_base(base or self.DEFAULT_BASE)

    def _validate_base(self, base):
        # TODO
        return base

    def _path(self, location, test):
        '''
        Given a 'location' and a script name, return a path that
        subprocess can use to execute the script.

        If the location is a remote location, fetch the script to a
        cache first. (TODO: or execute off of github?)

        '''
        if location.startswith('http') or location.startswith('ssh'):
            # TODO
            raise Exception('Github fetching not yet implemented')

        return os.sep.join([location, test])

    def _run(self, name, location, tests):
        '''
        Given a snap name, 'location' designator, and list of tests, run
        the tests for that snap.

        (This may be the main snap for this runner, or a snap in the 'base')

        '''
        tests = tests or []  # TODO: just fail if no tests?

        location_vars = dict(self.LOCATION_VARS)  # Copy
        location_vars['name'] = name
        location = location.format(**location_vars)

        env = dict(os.environ)
        env.update(self.ADMIN_ENV)

        for test in tests:
            script = self._path(location, test)
            p = subprocess.run([script], env=env)
            if p.returncode > 0:
                raise TestFailure(
                    'Failed to run test "{script}" for "{name}"'.format(
                        script=script, name=name))

    def run(self):
        for spec in self._base:
            try:
                self._run(**spec)
            except TestFailure as e:
                # Transform TestFailure here into an InfraFailure, to
                # help devs figure out just why the test failed.
                if self._name not in self._base:
                    raise InfraFailure('Snapstack setup failed: {}'.format(e))

        if self._name not in self._base:
            # Skip running tests separately for something that is
            # already smoke tested in the base.
            self._run(self._name, self._location, self._tests)
