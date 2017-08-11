from collections import OrderedDict

from snapstack.config import CONF_FILES
from snapstack.step import Step


class Base:
    def __init__(self):
        '''
        Setup a private OrderedDict to store steps.

        '''
        self._steps = OrderedDict()

    def steps(self):
        '''
        Return a list of Step objects, in order.

        '''
        return [s for _, s in self._steps.items()]

    def add_steps(self, *steps):
        '''
        Each step arg should be a tuple, comprising a name as its first
        element, and a Step object as its second.

        '''
        for name, value in steps:
            self._steps[name] = value

    def remove_steps(self, *steps):
        '''
        Each arg should be a stirng naming a step. We'll remove the named
        step from our map of steps.

        '''
        for name in steps:
            del self._steps[name]


class Setup(Base):
    def __init__(self):
        super(Setup, self).__init__()
        self._steps['confs'] = Step(
            script_loc='{snapstack}',
            files=CONF_FILES
        )
        self._steps['packages'] = Step(
            script_loc='{snapstack}',
            scripts=['packages.sh']
        )
        self._steps['rabbit_and_db'] = Step(
            script_loc='{snapstack}',
            scripts=['rabbitmq.sh', 'database.sh']
        )
        self._steps['keystone'] = Step(
            snap='keystone',
            script_loc='{openstack}/snap-{snap}/master/',
            scripts=['tests/keystone.sh'],
            files=[
                ('tests/etc/snap-keystone/keystone/keystone.conf.d/'
                 'database.conf')
            ]
        )
        self._steps['nova'] = Step(
            snap='nova',
            script_loc='{openstack}/snap-{snap}/master/',
            scripts=['tests/nova.sh'],
            files=[
                'tests/etc/snap-nova/nova/nova.conf.d/nova-placement.conf',
                'tests/etc/snap-nova/nova/nova.conf.d/scheduler.conf',
                'tests/etc/snap-nova/nova/nova.conf.d/database.conf',
                'tests/etc/snap-nova/nova/nova.conf.d/keystone.conf',
                'tests/etc/snap-nova/nova/nova.conf.d/rabbitmq.conf',
                'tests/etc/snap-nova/nova/nova.conf.d/neutron.conf',
            ]
        )
        self._steps['neutron'] = Step(
            snap='neutron',
            script_loc='{openstack}/snap-{snap}/master/',
            scripts=['tests/neutron.sh'],
            files=[
                'tests/etc/snap-neutron/neutron/neutron.conf.d/database.conf',
                'tests/etc/snap-neutron/neutron/neutron.conf.d/nova.conf',
                'tests/etc/snap-neutron/neutron/neutron.conf.d/keystone.conf',
            ]
        )
        self._steps['glance'] = Step(
            snap='glance',
            script_loc='{openstack}/snap-{snap}/master/',
            scripts=['tests/glance.sh'],
            files=[
                'tests/etc/snap-glance/glance/glance.conf.d/database.conf',
                'tests/etc/snap-glance/glance/glance.conf.d/keystone.conf'
            ]
        )
        self._steps['nova_hypervisor'] = Step(
            snap='nova-hypervisor',
            script_loc='{openstack}/snap-{snap}/master/',
            scripts=['tests/nova-hypervisor.sh'],
            files=[
                'tests/etc/snap-nova-hypervisor/nova/nova.conf.d/glance.conf',
                ('tests/etc/snap-nova-hypervisor/nova/nova.conf.d/'
                 'nova-placement.conf'),
                ('tests/etc/snap-nova-hypervisor/nova/nova.conf.d/'
                 'keystone.conf'),
                ('tests/etc/snap-nova-hypervisor/nova/nova.conf.d/'
                 'rabbitmq.conf'),
                'tests/etc/snap-nova-hypervisor/nova/nova.conf.d/neutron.conf',
                ('tests/etc/snap-nova-hypervisor/neutron/plugins/ml2/'
                 'openvswitch_agent.ini'),
                'tests/etc/snap-nova-hypervisor/neutron/metadata_agent.ini',
            ]
        )
        self._steps['neutron_ext_net'] = Step(
            script_loc='{snapstack}',
            scripts=['neutron-ext-net.sh']
        )


class Cleanup(Base):
    def __init__(self):
        super(Cleanup, self).__init__()
        self._steps['sql_cleanup'] = Step(
            script_loc='{snapstack}',
            scripts=['sql_cleanup.py']
        )
