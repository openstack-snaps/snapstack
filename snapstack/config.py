'''
Default config values for snapstack live here, including a default
"base" of snaps to install and test before testing the snap to be
tested, some magic string, and environment variables to set.

'''
import os
import sys

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

INSTALL_SNAP = """\
snap list | grep -q "^{snap}\s" || {{
    sudo snap install --edge --classic {snap}
}}
"""
