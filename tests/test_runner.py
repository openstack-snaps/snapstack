import os
import mock
import unittest

from snapstack import Runner, InfraFailure, config


class TestRunner(unittest.TestCase):

    @mock.patch('snapstack.runner.subprocess')
    def test_faux_run(self, mock_subprocess):
        '''
        _test_faux_run

        Test to verify that it looks like we are going to run all the
        right scripts, without actually setting up a snapstack.

        '''
        # Pick something in the base to test, so we don't actually
        # need to fake out tests for it:
        r = Runner('keystone')

        faux_p = mock.Mock()
        faux_p.returncode = 0

        env = dict(os.environ)
        env.update(config.ADMIN_ENV)

        mock_subprocess.run.return_value = faux_p

        r.run()

        mock_subprocess.run.assert_called_with(
            [os.sep.join([r.tempdir, 'neutron-ext-net.sh'])],
            env=env)

        r.cleanup()
        mock_subprocess.run.assert_called_with(
            ['sudo', 'rabbitmqctl', 'delete_user', 'openstack'])

    def test_validate_base(self):
        r = Runner('keystone')

        invalid_base01 = [{'foo': 'bar'}]
        valid_base01 = [{'location': '{github}', 'snap': 'foo', 'tests': []}]

        self.assertRaises(InfraFailure, r._validate_base, invalid_base01)
        self.assertTrue(r._validate_base(valid_base01))

    @unittest.skipUnless(
        os.environ.get('SNAPSTACK_TEST_INSTALL'),
        'Enabling this test will install software and tools on your machine.')
    def test_real_run(self):
        '''
        _test_real_run

        Comment out the skip above to setup snapstack on this machine.

        '''
        r = Runner('keystone')
        try:
            r.run()
        finally:
            r.cleanup()
