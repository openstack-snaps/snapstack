#!/bin/bash
#
# A script for testing OpenStack snap packages on a single node.
#

# TODO: make this cross distro friendly

# Update apt. Skip setting -ex if we're allowing unsigned repositories
# (as we do in the openstack gate) until after we've apt updated, as
# it will always return an error when there are unsigned packages,
# even if we pass --allow-unauthenciated.
if [ ${ALLOW_UNAUTHENTICATED+x} ]; then
    sudo apt update $ALLOW_UNAUTHENTICATED
    set -ex
else
    set -ex
    sudo apt update
fi

DEBIAN_FRONTEND='noninteractive' sudo -E apt install $ALLOW_UNAUTHENTICATED --yes python3-openstackclient rabbitmq-server mysql-server \
    memcached libvirt-bin qemu-kvm apparmor-utils python-neutronclient openvswitch-switch

sudo snap install core
