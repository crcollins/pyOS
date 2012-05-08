class Stream(object):
    def __init__(self, callback=None, name='', value='', listening=None):
        self.value = value
        if listening is not None:
            self.listening = [listening]
        else:
            self.listening = []
        self.name = name

    def add(self, callback):
        self.listening.append(callback)

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
        for f in self.listening:
            f(self.value)