from multiprocessing import Process

class BaseWatcher(Process):

    def __init__(self,queue):
        super(BaseWatcher,self).__init__()
        self._queue = queue

    def send_event(self,key,value):
        self._queue.put([key,value])


