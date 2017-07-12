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
            script_loc='{snap-test}',
            files=CONF_FILES
        )
        self._steps['packages'] = Step(
            script_loc='{snapstack}',
            scripts=['packages.sh']
        )
        self._steps['rabbit_and_db'] = Step(
            script_loc='{snap-test}',
            scripts=['scripts/rabbitmq.sh', 'scripts/database.sh']
        )
        self._steps['keystone'] = Step(
            snap='keystone',
            script_loc='{snap-test}',
            scripts=['scripts/keystone.sh']
        )
        self._steps['nova'] = Step(
            snap='nova',
            script_loc='{snap-test}',
            scripts=['scripts/nova.sh']
        )
        self._steps['neutron'] = Step(
            snap='neutron',
            script_loc='{snap-test}',
            scripts=['scripts/neutron.sh']
        )
        self._steps['glance'] = Step(
            snap='glance',
            script_loc='{snap-test}',
            scripts=['scripts/glance.sh']
        )
        self._steps['nova_hypervisor'] = Step(
            snap='nova-hypervisor',
            script_loc='{snap-test}',
            scripts=['scripts/nova-hypervisor.sh']
        )
        self._steps['neutron_ext_net'] = Step(
            script_loc='{snap-test}',
            scripts=['scripts/neutron-ext-net.sh']
        )


class Cleanup(Base):
    def __init__(self):
        super(Cleanup, self).__init__()
        self._steps['sql_cleanup'] = Step(
            script_loc='{snapstack}',
            scripts=['sql_cleanup.py']
        )
