import os
from glob import glob
from setuptools import setup, find_packages

this_dir = os.path.abspath(os.path.dirname(__file__))
reqs_file = os.path.join(this_dir, 'requirements.txt')
scripts = glob('snapstack/scripts/*.sh') + glob('snapstack/scripts/*.py')


with open(reqs_file) as f:
    reqs = [line for line in f.read().splitlines()
            if not line.startswith('--')]

SETUP = {
    'name': "snapstack",
    'packages': find_packages(),
    'version': "0.0.1",
    'author': "Pete Vander Giessen",
    'author_email': "petevg@canonical.com",
    'description': "Openstack Snap CI Harness [Prototype]",
    'url': "https://github.com/petevg/snapstack",
    'license': "Apache 2 License",
    'long_description': open('README.md').read(),
    'install_requires': reqs,
    'scripts': scripts,
}

if __name__ == '__main__':
    setup(**SETUP)
