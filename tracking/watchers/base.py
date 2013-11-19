from multiprocessing import Process
import signal

class BaseWatcher(Process):

    def __init__(self,name,queue):
        super(BaseWatcher,self).__init__()
        self._queue = queue
        self._name = name

    def disable_keyboard_interrupt(self):
        s = signal.signal(signal.SIGINT, signal.SIG_IGN)

    def send_event(self,value):
        self._queue.put([self._name,value])


