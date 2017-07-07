import unittest

from snapstack import Plan, Step, Setup, Cleanup


class ExampleTest(unittest.TestCase):

    def test(self):
        example = Step(
            snap='example',  # Name of the snap
            script_loc='./tests/',  # Parent location for tests and files
                                    # below. {local} is a magic string that
                                    # points at the 'tests' directory.
            tests=['example.sh'],  # Test the snap
            files=['example.json'],  # Config files
        )
        plan = Plan(tests=[example])
        plan()

    @unittest.skip("fnord")
    def test_custom_base(self):

        # Reference code for adding and removing stuff from our Setup
        # and Cleanup.

        setup = Setup()
        cleanup = Cleanup()

        # Add a step.
        example = Step(
            snap='example',
            script_loc='./tests/',
            tests=['example.sh'],
            files=['example.json'],
        )
        setup.add_steps(example=example)

        # Remove steps.
        setup.remove_steps(
            'keystone', 'nova', 'neutron', 'glance', 'nova_hypervisor',
            'neutron_exit_net')

        # Run with our changes (this will download the config files,
        # but then install nothing but the example snap).
        plan = Plan(tests=[], setup=setup.steps(), cleanup=cleanup.steps())
        plan()
