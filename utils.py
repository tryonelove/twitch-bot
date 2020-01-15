import json
import requests
import logging
import glob
import twitch

def getChannels():
    glob.c.execute("SELECT id, name FROM channels")
    return glob.c.fetchall()

def getEvents(channel):
    glob.c.execute("SELECT message, interval FROM events WHERE channel = ?", (channel,))
    return glob.c.fetchall()

def getAllCommands(channel):
    glob.c.execute("SELECT * FROM commands WHERE channel = ?", (channel,))

def isMod(username, channel):
    r = requests.get("http://tmi.twitch.tv/group/user/{}/chatters".format(username))
    if r.status_code != 200:
        logging.error("Error getting list of mods")
    js = r.json()
    chatters = js["chatters"]
    if username in chatters["broadcaster"] or username in chatters["moderators"] or username == "tryonelove":
        return True
    return False
    