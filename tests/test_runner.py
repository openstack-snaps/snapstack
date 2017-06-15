import unittest

from snapstack import Runner


class TestRunner(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Runner.LOCATION_VARS['snapstack'] = 'snapstack/scripts'


    def test_run(self):
        r = Runner('keystone')  # Pick something in the base, so we
                                # don't actually need to fake out
                                # tests for it.

        #r.run()
