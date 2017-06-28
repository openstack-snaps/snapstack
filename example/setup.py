import os
from setuptools import setup, find_packages

this_dir = os.path.abspath(os.path.dirname(__file__))
reqs_file = os.path.join(this_dir, 'requirements.txt')


with open(reqs_file) as f:
    reqs = [line for line in f.read().splitlines()
            if not line.startswith('--')]

SETUP = {
    'name': "example",
    'packages': find_packages(),
    'version': "0.0.1",
    'author': "Pete Vander Giessen",
    'author_email': "petevg@canonical.com",
    'description': "Example snap for snapstack",
    'url': "https://github.com/petevg/snapstack",
    'license': "Apache 2 License",
    'long_description': open('README.md').read(),
    'install_requires': reqs,
}

if __name__ == '__main__':
    setup(**SETUP)
