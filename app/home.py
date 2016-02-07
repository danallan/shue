# Set Hue and Sonos state based on presence at home
# Dan Armendariz
#
# Plays the primary Sonos group if it is paused,
# pausing it otherwise.
# Simulates pressing hue tap buttons to turn on selected
# Hue scenes.

from soco import discover
from phue import Bridge
from astral import Astral
from datetime import datetime, timedelta
import re

# location for sunset detection
CITY="Boston"

# number of minutes before sunset to turn on lights
DELTA=15

# Sonos Constants
MIN_VOLUME=10
MAX_VOLUME=30

# Hue constants
BRIDGE_IP="10.0.1.3"
TAPS={
    "Bedroom": 2,
    "Living room": 2,
}

def daytime():
    """
    Compute whether it is currently daytime based on current location
    """
    city = Astral()[CITY]
    sundata = city.sun()

    sunrise = sundata['sunrise'] + timedelta(minutes=DELTA)
    sunset = sundata['sunset'] - timedelta(minutes=DELTA)
    now = datetime.now(sunrise.tzinfo)

    return sunrise < now < sunset

def sonos(play=True):
    # detect Sonos zones on the local network
    zones = list(discover())

    if len(zones) < 1:
        print("Error: no Sonos zones found")
        return

    # select zone (for now, only the first one)
    sonos = zones[0]

    if play:
        # bound volume by extremes
        sonos.volume = max(MIN_VOLUME, min(sonos.volume, MAX_VOLUME))
        sonos.play()
    else:
        sonos.pause()

def hue(power=True):
    # contact bridge
    hue = Bridge(BRIDGE_IP)

    # first time only!
    #hue.connect()

    # turn all off if requested
    if not power:
        hue.set_group(0, 'on', False)
        return

    # don't mess with lights during the day time
    if daytime():
        return

    # we'll find scenes by searching rules for "Tap X.Y $str", where
    # X is a Tap number, Y is the tap button. First, search for Tap
    # numbers based on their names:
    tap_names = []
    for num, sensor in hue.get_api().get("sensors", {}).items():
        name = sensor.get("name", "")
        if name in TAPS:
            tap_names.append("Tap %s.%d" % (num, TAPS[name]))

    # now, determine scenes
    scenes = []
    for _, rule in hue.get_api().get("rules", {}).items():
        # pull only "Tap X.Y" from name
        name = rule.get("name", "")
        match = re.match(r"(?P<tid>Tap [0-9]\.[0-9]).*", name)
        if match is None:
            continue

        # see if Tap button is one of interest, recall its scene if so
        if match.group("tid") in tap_names:
            action = rule.get("actions", [{}])[0]
            scene = action.get("body", {}).get("scene", "")
            scenes.append(scene)

    # set all scenes
    for scene in scenes:
        hue.set_group(0, 'scene', scene)
    

def on():
    sonos(True)
    hue(True)

def off():
    sonos(False)
    hue(False)

def main():
    import sys

    def usage():
        print("Usage: %s ON|OFF" % sys.argv[0])
        sys.exit(1)

    if len(sys.argv) != 2:
        usage()

    if sys.argv[1] == "ON":
        on()
    elif sys.argv[1] == "OFF":
        off()
    else:
        usage()

if __name__ == "__main__":
    main()
