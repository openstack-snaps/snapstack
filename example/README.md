Snapstack Example
=================

This is a bare bones "snap" that is intended to demonstrate the basic
flow of testing an openstack snap with snapstack.

You may run the tests with tox like so:

    tox -v

The verbose option is highly recommended, as snapstack takes a while
to run, and the prototype simply lets the bash scripts it calls dump
their output to stdout.

WARNING: this will make alternations to your machine, including
installing (and then removing) a bunch of openstack snaps, and
installing (and not necessarily removing) some related tools to your
system.

This example contains a lot of files. The two most important are
`example/tests/example_test.py` and `examples/tox.ini`. By using
those files as templates, you should be able to write tests using
snapstack yourself.
