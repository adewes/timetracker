#!/usr/bin/python
from collections import defaultdict
from timetracker.tracking.backends.json_file import JSONBackend
from timetracker.tracking.watchers.active_window import ActiveWindowWatcher
from timetracker.tracking.watchers.keyboard_and_mouse import KeyboardAndMouseWatcher
from multiprocessing import Queue
from timetracker import settings

import time


def create_and_start_watcher(watcher_name,watcher_params,event_queue):
    watcher_instance = watcher_params['class'](watcher_name,event_queue)
    watcher_instance.start()
    return watcher_instance

watchers = {
    'active_window': {'class':ActiveWindowWatcher},
    'keyboard_and_mouse' : {'class':KeyboardAndMouseWatcher},
}

if __name__ == '__main__':
    event_queue = Queue()
    backend = JSONBackend(interval = 10,path = settings.DATA_PATH)

    active_watchers = {}

    for watcher_name,watcher_params in watchers.items():
        active_watchers[watcher_name] = create_and_start_watcher(watcher_name,watcher_params,event_queue)

    try:
        while True:
            time.sleep(0.1)
            for watcher_name,watcher_instance in active_watchers.items():
                if not watcher_instance.is_alive():
                    print "Watchers %s died, restarting..." % watcher_name
                    active_watchers[watcher_name] = create_and_start_watcher(watcher_name,watchers[watcher_name],event_queue)
            while not event_queue.empty():
                key,value = event_queue.get()
                if not key in active_watchers:
                    continue
                backend.add_datapoint(key,value,adder = active_watchers[key].add_to_datapoint,initializer = active_watchers[key].init_datapoint)
    except KeyboardInterrupt:
        print "Quitting..."
        for watcher in active_watchers.values():
            watcher.terminate()
            watcher.join()

