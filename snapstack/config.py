'''
Default config values for snapstack live here, including a default
"base" of snaps to install and test before testing the snap to be
tested, some magic string, and environment variables to set.

'''

DEFAULT_BASE = [
    # Setup
    {'location': '{snap-test}', 'files': [
         'admin-openrc',
         'etc/snap-nova-hypervisor/nova/nova.conf.d/glance.conf',
         'etc/snap-nova-hypervisor/nova/nova.conf.d/nova-placement.conf',
         'etc/snap-nova-hypervisor/nova/nova.conf.d/keystone.conf',
         'etc/snap-nova-hypervisor/nova/nova.conf.d/rabbitmq.conf',
         'etc/snap-nova-hypervisor/nova/nova.conf.d/neutron.conf',
         'etc/snap-nova-hypervisor/neutron/plugins/ml2/openvswitch_agent.ini',
         'etc/snap-nova-hypervisor/neutron/metadata_agent.ini',
         'etc/snap-neutron/neutron/neutron.conf.d/database.conf',
         'etc/snap-neutron/neutron/neutron.conf.d/nova.conf',
         'etc/snap-neutron/neutron/neutron.conf.d/keystone.conf',
         'etc/snap-keystone/keystone/keystone.conf.d/database.conf',
         'etc/snap-nova/nova/nova.conf.d/nova-placement.conf',
         'etc/snap-nova/nova/nova.conf.d/scheduler.conf',
         'etc/snap-nova/nova/nova.conf.d/database.conf',
         'etc/snap-nova/nova/nova.conf.d/keystone.conf',
         'etc/snap-nova/nova/nova.conf.d/rabbitmq.conf',
         'etc/snap-nova/nova/nova.conf.d/neutron.conf',
         'etc/snap-glance/glance/glance.conf.d/database.conf',
         'etc/snap-glance/glance/glance.conf.d/keystone.conf']},
    {'location': '{snapstack}', 'tests': ['packages.sh']},
    # Install snaps
    {'location': '{snap-test}', 'tests': [
        'scripts/rabbitmq.sh', 'scripts/database.sh']},
    {'snap': 'keystone', 'location': '{snap-test}',
     'tests': ['scripts/keystone.sh']},
    {'snap': 'nova', 'location': '{snap-test}', 'tests': ['scripts/nova.sh']},
    {'snap': 'neutron', 'location': '{snap-test}',
     'tests': ['scripts/neutron.sh']},
    {'snap': 'glance', 'location': '{snap-test}', 'tests': [
        'scripts/glance.sh']},
    {'snap': 'nova-hypervisor', 'location': '{snap-test}',
     'tests': ['scripts/nova-hypervisor.sh']},
    # Post install scripts
    {'location': '{snap-test}', 'tests': ['scripts/neutron-ext-net.sh']}
]

LOCATION_VARS = {
    'snapstack': '',  # Just exists in the PATH.
    'snap-test': (
        'https://raw.githubusercontent.com/openstack-snaps/snap-test/master/'
    ),
    'local': 'tests/',
    'snap': None  # Filled in by _run
}

INSTALL_SNAP = """\
snap list | grep -q "^{snap}\s" || {{
    sudo snap install --edge {classic}{snap}
}}
"""
