Snapstack Example
=================

This is a bare bones "snap" that is intended to demonstrate the basic
flow of testing an openstack snap with snapstack.

After you've installed the example snap (see below), you should be
able to run the tests with tox:

    tox -v

The verbose option is highly recommended, as snapstack takes a while
to run, and the prototype simply lets the bash scripts it calls dump
their output to stdout.

WARNING: this will make alternations to your machine, including
installing (and then removing) a bunch of openstack snaps, and
installing (and not necessarily removing) some related tools to your
system.

In addition to running tox, you should read
example/tests/example_test.py. Using examples/tox.ini and that file as
templates, you should be able to write tests using snapstack yourself.

As noted above, you'll need to install the example snap in your local
system before running these tests. To do so:

    sudo apt install snapstack
    snapcraft prime
    sudo snap try --devmode prime/

You will want to clean up the installed snap afterward with:

    sudo snap remove example

In a fully automated testing environment, you would script these steps
using the tools for your prefer CI framework.

