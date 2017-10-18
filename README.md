Snapstack
=========

Snapstack is an integration testing harness for Openstack Snaps.

Snapstack also includes scripts for deploying a minimal snap-based
OpenStack cloud.

Using Snapstack
---------------

### Deploying a Cloud

If you just want to deploy and configure a minimal snap-based OpenStack
cloud (keystone, neutron, glance, nova, nova-hypervisor) you can run:

```
snap-deploy
source admin-openrc
```

To destroy the cloud you can run:

```
snap-destroy
```

### Testing a Cloud

The main purpose of snapstack, however, is that it provides a harness
for doing basic CI on a snap. To use it, you'll want to pass one or
more Steps into a Plan object, and then run the Plan. Steps typically
specify a snap to install, config files to write, and executable Python
or bash scripts that will configure and perform a basic smoke test on the
snap.

The Setup class in snapstack/base.py defines the Steps for the default
base OpenStack cloud. While the steps for the base OpenStack cloud
exist in the snapstack code base, steps for individual snaps will
usually live in the corresponding snap's git repo.

The following example is a basic test that installs and tests an
example snap, after letting the Plan object install and configure the
default base OpenStack (keystone, neutron, glance, nova, and
nova-hypervisor) from the snap store.

```
example = Step(
    snap='example',
    script_loc='./tests/',
    scripts=['example.sh'],
    files=['example.json'],
    snap_store=False
)
plan = Plan(tests=[example])
plan.run()
```

Take a look in the example directory to see the source snippet above
in context.

The following example is a bit different than the first. While it also
installs and configures the default base OpenStack, it does so while
overriding the default base keystone with a locally built keystone snap.
It then runs the specified test scripts. This is taken from the keystone
snap's git repo.

```
setup = Setup()
setup.add_steps(('keystone', Step(
    snap='keystone',
    script_loc='./tests/',
    scripts=['keystone.sh'],
    files=['etc/snap-keystone/keystone/keystone.conf.d/database.conf'],
    snap_store=False)))
plan = Plan(base_setup=setup.steps())
plan.run()
```

In the previous examples, the script location (script_loc) is a local
relative path, however this could also be a remote URL location. If you
take a closer look at the Setup class in snapstack/base.py, you'll see
that the script_loc for each of the base snaps corresponds to each
individual snap on github. For example, the glance script is located at:
https://raw.githubusercontent.com/openstack/snap-glance/master/tests/glance.sh

This codebase is meant to be a fairly lightweight Python wrapper
around your shell scripts. The purpose is to test the snap, rather
than to extensively test the underlying source, so basic tests will
usually suffice.

Flags and Other Notes
---------------------

If you are in a network restricted environment, and need to go through
a proxy to make HTTP requests, set SNAPSTACK_HTTPS_PROXY and
SNAPSTACK_HTTP_PROXY in your terminal environment. This will set
HTTP/S_PROXY for the snap build steps, and give you an environment
variable that you can reference in your scripts.
