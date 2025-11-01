class Event:
    def __init__(self):
        self.handlers = []

    def register(self, func):
        self.handlers.append(func)
        return func

    def unregister(self, func):
        self.handlers.remove(func)

    def fire(self, *args, **kwargs):
        for handler in self.handlers:
            handler(*args, **kwargs)


class Observer:
    def __init__(self, value=None):
        self._value = value
        self.on_change = Event()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if new_value != self._value:
            old_value = self._value
            self._value = new_value
            self.on_change.fire(old_value, new_value)
