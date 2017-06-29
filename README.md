Snapstack
=========

Snapstack is an integration testing harness for Openstack Snaps.

It is currently still a prototype. All comments and feedback welcome!

Using Snapstack
---------------

Snapstack provides a harness for doing basic CI on a snap. To use this
library, you should:

1) Import snapstack.Runner into the tests for your snap.

2) Create an instance of the Runner class, and invoke its .run and
.cleanup routine, passing in your snap name, and pointers to shell
scripts that will install the snap, test it, and clean it up.

The runner is meant to be a fairly lightweight Python wrapper around
your shell scripts. It also wraps around a set of scripts that will
setup a "base" openstack via a standard set of snaps. You can define
your own base if necessary.

The overarching purpose is to test the snap, rather than to
extensively test the underlying surface, so basic tests will usually
suffice.

See the example directory for a sample bare bones snap with snapstack
tests.
