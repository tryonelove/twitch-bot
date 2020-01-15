import abc
import utils
import glob
import eventHandler

class Command(metaclass=abc.ABCMeta):
    def __init__(self, chat, key, value):
        self._key = key
        self._value = value
        self._chat = chat

    @abc.abstractmethod
    def execute(self):
        pass


class AddCommand(Command):
    def __init__(self, chat, key, value):
        super().__init__(chat, key, value)

    def execute(self):
        glob.c.execute("INSERT INTO commands VALUES (?, ?, ?)", (self._chat, self._key, self._value))
        glob.db.commit()
        return "Команда {} была успешно добавлена!".format(self._key)


class DeleteCommand(Command):
    def __init__(self, chat, key):
        super().__init__(chat, key, None)
    
    def execute(self):
        glob.c.execute("DELETE FROM commands WHERE key = ? AND channel = ?",(self._key, self._chat))
        glob.db.commit()
        return "Команда {} была успешно удалена!".format(self._key)


class AddEventCommand(Command):
    def __init__(self, chat, key, value):
        super().__init__(chat, key, value)
    
    def execute(self):
        glob.c.execute("INSERT INTO events VALUES (?, ?, ?)", (self._chat, self._value, self._key))
        glob.db.commit()
        glob.events[self._chat].addEvent(self._value, int(self._key))
        return "Событие добавлено! Сообщение {} будет отправляться с интервалом {}".format(self._value, self._key)


class DeleteEventCommand(Command):
    def __init__(self, chat, value):
        super().__init__(chat, None, value)
    
    def execute(self):
        glob.c.execute("DELETE FROM events WHERE channel = ? AND message = ?", (self._chat, self._value))
        glob.db.commit()
        glob.events[self._chat].deleteEvent(self._value)
        return "Событие удалено! Сообщение {} больше не будет отправляться".format(self._value)

class StaticCommand(Command):
    def __init__(self, chat, key):
        super().__init__(chat, key, None)
    
    def execute(self):
        return glob.c.execute("SELECT value FROM commands WHERE channel = ? AND key = ?",(self._chat, self._key)).fetchone()[0]