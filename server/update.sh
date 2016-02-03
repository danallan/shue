#!/bin/sh
#
# update.sh, stop current proc

prog_dir="$(dirname "$(realpath "$0")")"
/bin/sh "${prog_dir}/service.sh" stop
