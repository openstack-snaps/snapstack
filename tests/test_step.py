import unittest

from snapstack.step import fix_proxy_string


class TestStep(unittest.TestCase):

    def test_proxy_string(self):
        fps = fix_proxy_string

        self.assertEqual(fps('https://foo.bar'), 'http://foo.bar')
        self.assertEqual(fps('https://foo.bar', https=True), 'https://foo.bar')
        self.assertEqual(fps('http://foo.bar', https=True), 'https://foo.bar')
        self.assertEqual(fps('http://foo.bar'), 'http://foo.bar')
        self.assertEqual(fps('foo.bar', https=True), 'https://foo.bar')
        self.assertEqual(fps('foo.bar'), 'http://foo.bar')
