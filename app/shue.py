# shue.py
# Dan Armendariz
#
# Provide a Flask web interface for home control.
# Track present users, turning on all items when the first
# arrives home and turning off all items when the last leaves.
# Provide a manual, web-based control over all items.

import home
import json
from flask import Flask, render_template
app = Flask(__name__)

SAVE_FILE="../var/state.txt"

def getState():
    """
    Read save file as json, returning blank object if not present.
    """
    try:
        with open(SAVE_FILE, 'r') as f:
            j = json.load(f)
        return j
    except (IOError, OSError, ValueError):
        return {}

def saveState(s):
    """
    Save state object to file as json.
    """
    with open(SAVE_FILE, 'w') as f:
        json.dump(s, f)

@app.route("/")
def index():
    return render_template("shue.html")
    s = getState()
    p = s.get("people", 0)

    if p == 1:
        return "There is one person at home right now."
    else:
        return "There are %d people at home right now." % p

@app.route("/arrive")
def arrive():
    s = getState()
    s['people'] = s.get("people", 0) + 1
    saveState(s)

    if s['people'] == 1:
        home.on()
        return "You're the first to come home; turning on!"
    
    return "Welcome home! There are now %d people here." % s['people']

@app.route("/leave")
def leave():
    s = getState()
    s['people'] = max(s.get("people", 1)-1, 0)
    saveState(s)

    if s['people'] == 0:
        home.off()
        return "You're the last to leave; turning everything off!"

    p = "people remain" if s['people'] > 1 else "person remains"
    return "Goodbye! Keeping power on since %d %s." % (s['people'], p)

@app.route("/count")
def count():
    s = getState()
    return "%d" % s.get("people", 0)

@app.route("/reset/", defaults={'num':0})
@app.route("/reset/<int:num>")
def reset(num):
    saveState({"people": num})
    return "%d" % num

@app.route("/on")
def turnOn():
    home.on()
    return "ok"

@app.route("/off")
def turnOff():
    home.off()
    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9999)
