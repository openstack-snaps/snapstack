Snapstack
=========

Snapstack is an integration testing harness for Openstack Snaps.

It is currently still a prototype. All comments and feedback welcome!

Using Snapstack
---------------

Snapstack provides a harness for doing basic CI on a snap. To use it,
you'll want to pass one or more Steps into a Plan object. Steps
typically specify a snap to install, along with an executable Python
or bash script that will perform a basic smoke test on the snap. For
example:

```
example = Step(
    snap='example',
    script_loc='./tests/',
    tests=['example.sh'],
    files=['example.json'],
    snap_store=False
)
plan = Plan(tests=[example])
plan()

```

This codebase is meant to be a fairly lightweight Python wrapper
around your shell scripts. The purpose is to test the snap, rather
than to extensively test the underlying source, so basic tests will
usually suffice.

Take a look in the example directory to see the source snippet above
in context.

Flags and Other Notes
---------------------

If you are in a network restricted environment, and need to go through
a proxy to make HTTP requests, set SNAPSTACK_HTTPS_PROXY and
SNAPSTACK_HTTP_PROXY in your terminal environment. This will set
HTTP/S_PROXY for the snap build steps, and give you an environment
variable that you can reference in your scripts.
