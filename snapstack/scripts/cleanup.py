#!/usr/bin/python3

import subprocess

subprocess.run(['sudo', 'rabbitmqctl', 'delete_user', 'openstack'])
