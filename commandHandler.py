import abc
import config
import commands
import exceptions
import utils

class CommandHandler:
    def __init__(self, message_object):
        self._author = message_object.sender
        self._channel = message_object.channel
        self._message = message_object.text
        self._getCommandValue()

    def _getCommandValue(self):
        msg = self._message.split(" ")
        self.command = msg[0][1:]
        self.value = " ".join(msg[1:])

    def _getKeyValue(self):
        msg = self._message.split(" ")
        key = msg[1]
        value = " ".join(msg[2:])
        return key, value

    def handler(self):
        # ---Command-managing---
        if self.command == "addcom":
            if not utils.isMod(self._author, self._channel):
                return
            if len(self.value.split()) < 2:
                raise exceptions.NotEnoughArguments
            keyValuePair = self._getKeyValue()
            return commands.AddCommand(self._channel, *keyValuePair)
        elif self.command == "delcom":
            if not utils.isMod(self._author, self._channel):
                return
            if len(self.value.split()) < 1:
                raise exceptions.NotEnoughArguments
            key = self._getKeyValue()[0]
            return commands.DeleteCommand(self._channel, key)
        elif self.command == "addevent":
            if not utils.isMod(self._author, self._channel):
                return
            if len(self.value.split()) < 2:
                raise exceptions.NotEnoughArguments
            keyValuePair = self._getKeyValue()
            return commands.AddEventCommand(self._channel, *keyValuePair)
        elif self.command == "delevent":
            if not utils.isMod(self._author, self._channel):
                return
            if len(self.value.split()) < 1:
                raise exceptions.NotEnoughArguments
            return commands.DeleteEventCommand(self._channel, self.value)
        # ----------------------
        else:
            return commands.StaticCommand(self._channel, self.command)