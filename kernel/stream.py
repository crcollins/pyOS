class Stream(object):
    def __init__(self, callback=None, name='', value='', listeners=None):
        self.value = value
        if listeners is not None:
            self.listeners = [listeners]
        else:
            self.listeners = []
        self.name = name

    def add(self, callback):
        self.listeners.append(callback)

    def write(self, value):
        print "<%s> %s" %(self.name, value)
        self.value += value
        self.broadcast()

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value
        self.broadcast()

    def digest_value(self):
        x = self.value
        self.set_value('')
        return x

    def broadcast(self):
        for f in self.listeners:
            f(self.value)