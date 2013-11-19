from Xlib.display import Display
from Xlib import X
from Xlib.ext import record
from Xlib.protocol import rq

from base import BaseWatcher
from collections import defaultdict

import math

class KeyboardAndMouseWatcher(BaseWatcher):

    def __init__(self,name,queue):
        super(KeyboardAndMouseWatcher,self).__init__(name,queue)
        self._queue = queue
        self._mouse_last_x = None
        self._mouse_last_y = None
        self._display = Display()

    def add_to_datapoint(self,x,y):
        if y[0] == 'keys_pressed':
            x[y[0]][y[1]]+=y[2]
        else:
            x[y[0]]+=y[1]
        return x

    def init_datapoint(self):
        return {'buttons_pressed': 0,'keys_pressed' :defaultdict(lambda :0),'mouse_moved':0}

    def handle_event(self,reply):
        """ This function is called when a xlib event is fired """
        
        data = reply.data

        while len(data):
            event, data = rq.EventField(None).parse_binary_value(data, self._display.display, None, None)
            
            if event.type == X.MotionNotify:
                if self._mouse_last_x != None:
                    mouse_distance=math.sqrt((event.root_x-self._mouse_last_x)**2+(event.root_y-self._mouse_last_y)**2)
                    self.send_event(('mouse_moved',mouse_distance))
                self._mouse_last_x,self._mouse_last_y = event.root_x,event.root_y
    
            if event.type == X.ButtonPress:
                self.send_event(('buttons_pressed',1))

            if event.type == X.KeyPress:
                key = event.detail
                self.send_event(('keys_pressed',key,1))

    def run(self):
        self.disable_keyboard_interrupt()
        root = self._display.screen().root
        ctx = self._display.record_create_context(
                    0,
                    [record.AllClients],
                    [{
                            'core_requests': (0, 0),
                            'core_replies': (0, 0),
                            'ext_requests': (0, 0, 0, 0),
                            'ext_replies': (0, 0, 0, 0),
                            'delivered_events': (0, 0),
                            'device_events': (X.KeyReleaseMask, X.PointerMotionMask),
                            'errors': (0, 0),
                            'client_started': False,
                            'client_died': False,
                    }])

        self._display.record_enable_context(ctx, self.handle_event)

