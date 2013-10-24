from collections import defaultdict
from timetracker.tracking.backends.json_file import JSONBackend
from timetracker.tracking.watchers.active_window import ActiveWindowWatcher
from timetracker.tracking.watchers.keyboard_and_mouse import KeyboardAndMouseWatcher
from multiprocessing import Queue

import time

def add_process(x,y):
    x[y['exe']][y['title']]+=y['time']
    return x

def initialize_process():
    return defaultdict( lambda : defaultdict (lambda :0))

event_params = {
    'active_process' : {
                            'adder' : add_process,
                            'initializer' : initialize_process
                       }
    }

watchers = {
    'keyboard_and_mouse' : {'class':KeyboardAndMouseWatcher},
    'active_window' : {'class':ActiveWindowWatcher}
}

def create_and_start_watcher(watcher_params,event_queue):
    watcher_instance = watcher_params['class'](event_queue)
    watcher_instance.start()
    return watcher_instance

if __name__ == '__main__':
    event_queue = Queue()
    backend = JSONBackend(interval = 60,path = "./timetracker/data")

    active_watchers = {}

    for watcher_name,watcher_params in watchers.items():
        active_watchers[watcher_name] = create_and_start_watcher(watcher_params,event_queue)

    try:
        while True:
            time.sleep(0.1)
            for watcher_name,watcher_instance in active_watchers.items():
                if not watcher_instance.is_alive():
                    print "Watchers %s died, restarting..." % watcher_name
                    active_watchers[watcher_name] = create_and_start_watcher(watchers[watcher_name],event_queue)
            while not event_queue.empty():
                key,value = event_queue.get()
                if key in event_params: 
                    adder,initializer = event_params[key]['adder'],event_params[key]['initializer']
                    backend.add(key,value,adder = adder,initializer = initializer)
                else:
                    backend.add(key,value)
    except KeyboardInterrupt:
        active_window_watcher.terminate()
        keyboard_and_mouse_watcher.terminate()