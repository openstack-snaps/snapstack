import mock
import unittest

from snapstack.step import Step


class TestStep(unittest.TestCase):

    @mock.patch('snapstack.step.subprocess')
    def test_make_env(self, mock_subprocess):
        step = Step()

        faux_p = mock.Mock()
        mock_subprocess.run.return_value = faux_p

        faux_p.stdout.decode.return_value = 'internap.openstack.org\nbar'

        ret = step._make_env()

        self.assertEqual(
            ret.get('ALLOW_UNAUTHENTICATED'), '--allow-unauthenticated')

        faux_p.stdout.decode.return_value = 'foo.openstack.com\nbar'

        ret = step._make_env()
        self.assertFalse(ret.get('ALLOW_UNAUTHENTICATED'))
