from Xlib.display import Display
from Xlib import X
from Xlib.ext import record
from Xlib.protocol import rq

import psutil
import time

from base import BaseWatcher

class ActiveWindowWatcher(BaseWatcher):

    def __init__(self,queue,interval = 1.0):
        super(ActiveWindowWatcher,self).__init__(queue)
        self._last_time = time.time()
        self._interval = interval

    def run(self):

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
                            print value
                            self.send_event('active_process',value)
                            self._last_time = time.time()
                        except:
                            pass
            except AttributeError:
                pass
