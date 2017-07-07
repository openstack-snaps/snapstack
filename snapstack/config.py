'''
Default config values for snapstack live here.

'''


CONF_FILES = [
    'admin-openrc',
    'etc/snap-nova-hypervisor/nova/nova.conf.d/glance.conf',
    'etc/snap-nova-hypervisor/nova/nova.conf.d/nova-placement.conf',
    'etc/snap-nova-hypervisor/nova/nova.conf.d/keystone.conf',
    'etc/snap-nova-hypervisor/nova/nova.conf.d/rabbitmq.conf',
    'etc/snap-nova-hypervisor/nova/nova.conf.d/neutron.conf',
    'etc/snap-nova-hypervisor/neutron/plugins/ml2/''openvswitch_agent.ini',
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
    'etc/snap-glance/glance/glance.conf.d/keystone.conf']


LOCATION_VARS = {
    'snapstack': '',  # Snapstack adds some scripts to your PATH.
    'snap-test': (
        'https://raw.githubusercontent.com/openstack-snaps/snap-test/master/'
    ),
    'snap': None  # Filled in by _run
}

INSTALL_SNAP = """\
snap list | grep -q "^{snap}\s" || {{
    sudo snap install --edge {classic}{snap}
}}
"""
