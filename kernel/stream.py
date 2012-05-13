class Stream(object):
    def __init__(self, callback=None, name='', value='', listeners=None):
        self.value = value
        if listeners is not None:
            self.listeners = [listeners]
        else:
            self.listeners = []
        self.name = name
        self.listening = []

    def __nonzero__(self):
        return bool(self.listening)

    def add(self, callback, stream=False):
        if stream:
            self.listeners.append(callback.write)
            callback.listening.append(self)
        else:
            self.listeners.append(callback)

    def write(self, value):
        self.value = value
        self.broadcast()

    def get_value(self):
        return self.value

    def broadcast(self):
        if self.listeners:
            for f in self.listeners:
                f(self.value)
        else:
            print "<%s> %s" %(self.name, self.value),
