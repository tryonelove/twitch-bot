import abc
import utils
import logging
import twitch
import config
import commandHandler
import exceptions
import eventHandler
import glob
import sqlite3
import threading

class Bot:
    def __init__(self):
        logging.basicConfig(
            format='%(levelname)s: %(message)s', level=logging.DEBUG)
        self.active_chats = {}

    def messageHandler(self, message: twitch.chat.Message):
        if message.text.startswith("!") and message.sender != config.BOT_NAME:
            try:
                command = commandHandler.CommandHandler(message).handler()
                if command is not None:
                    response = command.execute()
            except exceptions.NotEnoughArguments:
                response = exceptions.template.format("Проверьте правильность аргументов")
            if response is not None:
                self.active_chats[message.channel].send(response)

    def start(self):
        for _, channel in utils.getChannels():
            self.active_chats[channel] = twitch.Chat(channel='#{}'.format(channel), nickname=config.BOT_NAME, oauth=config.OAUTH_TOKEN, helix=twitch.Helix(client_id=config.CLIENT_ID, use_cache=True))
            self.active_chats[channel].subscribe(self.messageHandler)
            events = utils.getEvents(channel)
            glob.events[channel] = eventHandler.MessagePoster(chat=self.active_chats[channel])
            for message, interval in events:
                glob.events[channel].addEvent(message, interval)
            logging.info("JOINED #{}".format(channel))
        logging.info("Succesfully started")


if __name__ == "__main__":
    glob.db = sqlite3.connect("db.sqlite", check_same_thread=False)
    glob.c = glob.db.cursor()
    glob.events = {}
    bot = Bot()
    bot.start()