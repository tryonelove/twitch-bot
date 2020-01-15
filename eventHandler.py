import time
import threading
import twitch
from time import sleep
import logging

class MessagePoster:
    def __init__(self, chat: twitch.Chat):
        self._chat = chat
        self._threads = []

    def sendMessage(self, message, interval):
        while True:
            if message in self._threads:
                self._chat.send(message)
                sleep(interval)
            else:
                break

    def addEvent(self, message, interval):
        self._threads.append(message)
        logging.info("STARTING A NEW EVENT: POSTING MESSAGE IN {} EVERY {} SECS".format(self._chat, interval))
        threading.Thread(target = self.sendMessage, args=(message, interval)).start()

    def deleteEvent(self, message):
        logging.info("REMOVING AN EVENT FROM {}".format(self._chat))
        self._threads.remove(message)
