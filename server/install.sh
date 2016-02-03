#!/bin/sh
#
# shue install script

prog_dir="$(dirname "$(realpath "$0")")"
VENV="${prog_dir}/libexec"

# create libexec virtualenv in prog_dir
/mnt/DroboFS/Shares/DroboApps/python3/bin/pyvenv "$VENV"

# install requirements
. "$VENV/bin/activate"
pip install --upgrade pip
pip install -r "${prog_dir}/etc/requirements.txt"

# make sure var directory exists for state saving
mkdir -p "${prog_dir}/var"
