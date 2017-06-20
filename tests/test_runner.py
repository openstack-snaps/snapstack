import os
import mock
import unittest

from snapstack import Runner


class TestRunner(unittest.TestCase):

    @mock.patch('snapstack.main.subprocess')
    def test_faux_run(self, mock_subprocess):
        '''
        Test to verify that it looks like we are going to run all the
        right scripts, without actually setting up a snapstack.

        '''
        # Pick something in the base to test, so we don't actually
        # need to fake out tests for it:
        r = Runner('keystone')

        faux_p = mock.Mock()
        faux_p.returncode = 0

        env = dict(os.environ)
        env.update(Runner.ADMIN_ENV)

        mock_subprocess.run.return_value = faux_p

        r.run()

        mock_subprocess.run.assert_called_with(
            ['neutron-ext-net.sh'],
            env=env)

        r.cleanup()
        mock_subprocess.run.assert_called_with(
            ['sudo', 'rabbitmqctl', 'delete_user', 'openstack'])

    # TODO: convert to skipif statement, and depend on env variable.
    @unittest.skip('Comment this out to run a real snapstack')
    def test_real_run(self):
        '''
        Comment out the skip above to setup snapstack on this machine.

        '''
        r = Runner('keystone')
        try:
            r.run()
        finally:
            r.cleanup()
