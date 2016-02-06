#!/bin/sh

. /etc/service.subr

framework_version="2.1"
name="shue"
version="1.0.1"
description="Automatic and manual control over both Sonos and Hue devices."
depends="python3"
webui=""

prog_dir="$(dirname "$(realpath "${0}")")"
pidfile="/tmp/DroboApps/${name}/pid.txt"
logfile="/tmp/DroboApps/${name}/log.txt"

start() {
    . "${prog_dir}/libexec/bin/activate"
    setsid gunicorn -w 2 -b 0.0.0.0:9999 --pythonpath "${prog_dir}/app" \
            --daemon --pid ${pidfile} --log-file ${logfile} shue:app
}

main "$@"
