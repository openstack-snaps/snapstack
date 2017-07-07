import subprocess


SQL_CLEANUP = """\
sudo mysql -u root << EOF
DROP DATABASE keystone;
DROP DATABASE nova;
DROP DATABASE nova_api;
DROP DATABASE nova_cell0;
DROP DATABASE neutron;
DROP DATABASE glance;
DROP DATABASE cinder;
EOF"""
subprocess.run([SQL_CLEANUP], shell=True)

subprocess.run(['sudo', 'rabbitmqctl', 'delete_user', 'openstack'])
