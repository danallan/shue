# shue-server

Control Sonos and Hue bulbs from a single place.

## Development

* Clone repo
* `make prep`

Preparation will install a Python3 virtual environment and all
the prerequisites. You can then run with `make run` or, perhaps best,
activate the virtual environment and run the server manually:

* `source venv/bin/activate`
* `python app/shue.py`

## Deployment

The server is meant to be run on a Drobo 5N. To build the Drobo
application:

* `make build`
* Drag the resulting tgz file into the DroboApps directory on the Drobo.
* Restart the Drobo, or SSH in and run `/usr/bin/DroboApps.sh install` as root
* The server can then be accessed at `http://DROBO-IP:9999/`

