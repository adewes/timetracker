from Xlib.display import Display
from Xlib import X
from Xlib.ext import record
from Xlib.protocol import rq

import psutil
import time
from collections import defaultdict

from base import BaseWatcher

class ActiveWindowWatcher(BaseWatcher):

    def __init__(self,name,queue,interval = 1.0):
        super(ActiveWindowWatcher,self).__init__(name,queue)
        self._last_time = time.time()
        self._interval = interval

    def add_to_datapoint(self,x,y):
        x[y['exe']][y['title']]+=y['time']
        return x

    def init_datapoint(self):
        return defaultdict( lambda : defaultdict (lambda :0))

    def run(self):

        self.disable_keyboard_interrupt()

        display = Display()

        while True:
            try:
                time.sleep(self._interval)
                window = display.get_input_focus().focus

                if window.get_wm_class() is None and window.get_wm_name() is None:
                    window = window.query_tree().parent
                if window:
                    pid_value = window.get_full_property(display.intern_atom('_NET_WM_PID'),0)
                    if pid_value:
                        try:
                            pid = int(pid_value.value[0])
                            process = psutil.Process(pid)
                            name,exe,title = process.name,process.exe,window.get_wm_name()
                            value = {'exe':exe,'title':title.decode('latin-1'),'time':time.time()-self._last_time}
                            self.send_event(value)
                            self._last_time = time.time()
                        except:
                            pass
            except AttributeError:
                pass
