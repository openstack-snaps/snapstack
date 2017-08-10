import unittest

from snapstack import Plan, Step, Setup, Cleanup


class ExampleTest(unittest.TestCase):

    def test_example(self):
        '''
        _test_example_

        Basic test, which installs and tests an example
        snap, after letting the Plan object build the default
        snapstack.

        Note: this will install snapstack on your system!

        '''
        example = Step(
            snap='example',  # Name of the snap
            script_loc='./tests/',  # Parent location for tests and files
                                    # below. {local} is a magic string that
                                    # points at the 'tests' directory.
            scripts=['example.sh'],  # Test the snap
            files=['example.json'],  # Config files
            snap_store=False  # Build from local source, rather than
                              # install from the snap store.
        )
        plan = Plan(tests=[example])
        plan.run()

    def test_custom_base(self):
        '''
        _test_custom_base_

        Reference code for adding and removing stuff from our Setup
        and Cleanup.

        '''
        setup = Setup()
        cleanup = Cleanup()

        # Add a step.
        somesnap = Step(
            snap='example',  # Re-use our example snap, for convenience.
            script_loc='./tests/',  # In an actual test, these would
                                    # probably be remote, as the snap
                                    # we're adding to the base isn't
                                    # part of our source.
            scripts=['somesnap.sh'],
            files=[],
            snap_store=False
        )
        setup.add_steps(('somesnap', somesnap))

        # Remove steps.
        setup.remove_steps(
            'keystone', 'nova', 'neutron', 'glance', 'nova_hypervisor',
            'neutron_ext_net')

        # Note that Cleanup can be modified in the same way as the above.

        # Setup our test
        example = Step(
            snap='example',  # Name of the snap
            script_loc='./tests/',  # Parent location for tests and files
                                    # below. {local} is a magic string that
                                    # points at the 'tests' directory.
            scripts=['example.sh'],  # Test the snap
            files=['example.json'],  # Config files
            snap_store=False  # Build from local source, rather than
                              # install from the snap store.
        )

        # Run with our changes (this will download the config files,
        # but then install nothing but the example snap).
        plan = Plan(
            tests=[example],
            base_setup=setup.steps(),
            base_cleanup=cleanup.steps()
        )
        plan.run()
