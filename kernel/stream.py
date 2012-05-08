class Stream(object):
    def __init__(self, name='', value='', listener=None, listening=None):
        self.value = value
        self.listener = listener
        self.listening = listening
        self.name = name

    def write(self, value):
        print "<%s> %s" %(self.name, value)
        #self.value += value
        #self.broadcast()

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value
        self.broadcast()

    def digest_value(self):
        x = self.value
        self.set_value('')
        return x

    def broadcast():
        pass