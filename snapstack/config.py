'''
Default config values for snapstack live here, including a default
"base" of snaps to install and test before testing the snap to be
tested, some magic string, and environment variables to set.

'''
import os
import sys

DEFAULT_BASE = [
    # Setup
    {'location': '{snapstack}', 'tests': ['packages.sh']},
    {'location': '{snap-test}', 'tests': ['rabbitmq.sh', 'database.sh']},
    {'snap': 'keystone', 'location': '{snap-test}',
     'tests': ['keystone.sh']},
    {'snap': 'nova', 'location': '{snap-test}', 'tests': ['nova.sh']},
    {'snap': 'neutron', 'location': '{snap-test}',
     'tests': ['neutron.sh']},
    {'snap': 'glance', 'location': '{snap-test}', 'tests': ['glance.sh']},
    {'snap': 'nova-hypervisor', 'location': '{snap-test}',
     'tests': ['nova-hypervisor.sh']},
    # Post install scripts
    {'location': '{snap-test}', 'tests': ['neutron-ext-net.sh']}
]

LOCATION_VARS = {
    'snapstack': '',  # Just exists in the PATH.
    'snap-test': (
        'https://raw.githubusercontent.com/openstack-snaps/snap-test/master/'
        'scripts/'
    ),
    'local': 'tests/',
    'snap': None  # Filled in by _run
}

ADMIN_ENV = {
    'BASE_DIR': os.path.dirname(sys.modules[__name__].__file__)
}

INSTALL_SNAP = """\
snap list | grep -q "^{snap}\s" || {{
    sudo snap install --edge --classic {snap}
}}
"""
