import unittest

from snapstack import Runner


class ExampleTest(unittest.TestCase):

    def test(self):
        # TODO: install snap from local

        r = Runner(
            snap='example',  # Name of the snap
            location='./tests/',  # Parent location for tests and files
                                  # below. {local} is a magic string that
                                  # points at the 'tests' directory.
            tests=['example.sh'],  # Test the snap
            files=['example.json'],  # Config files
            base=None  # Don't override default Base.
        )
        
        try:
            r.run()
        finally:
            r.cleanup()
