#!/bin/bash

set -ex

# $BASE_DIR is a tmp directory that gets created by the snapstack
# Runner. Files that are downloaded remotely get downloaded to this
# temp dir. We automatically download some useful config files. For
# example, an admin-openrc:
source $BASE_DIR/admin-openrc

echo "Foo!";  # The example snap is empty, so we can't do much with it
              # -- in an actual snap, you'd perhaps poke at a server
              # port to make sure that it got setup.
