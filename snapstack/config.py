import os

'''
Default config values for snapstack live here.

'''


LOCATION_VARS = {
    'snapstack': '{snapstack}/scripts/'.format(
        snapstack=os.path.dirname(__file__)),
    'openstack': 'https://raw.githubusercontent.com/openstack',
    'snap': None  # Filled in by _run
}


CHANNEL = 'ocata/edge'


INSTALL_SNAP = """\
snap list | grep -q "^{snap}\s" || {{
    sudo snap install{classic} {channel} {snap}
}}
"""
