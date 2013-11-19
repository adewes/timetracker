import json
import datetime
import time
import os.path
import pprint

from base import BaseBackend

class JSONBackend(BaseBackend):

    def __init__(self,interval = 5*60,path = ""):
        self._path = os.path.abspath(path)
        self._current_time = int(time.time()/interval)*interval
        self._interval = interval
        self._current_dict = {'timestamp' : self._current_time}

    def get_date_str(self):
        return datetime.datetime.fromtimestamp(self._current_time).strftime("%Y-%m-%d")

    def get_output_filename(self):
        return self._path + "/" + self.get_date_str() + ".json"

    def write_dict(self):
        with open(self.get_output_filename(),"ab") as output_file:
            pprint.pprint(self._current_dict)
            output_file.write(json.dumps(self._current_dict).strip()+"\n")

    def get_dict(self):
        current_time = time.time()
        if (current_time-self._current_time) > self._interval:
            self.write_dict()
            self._current_time = int(current_time/self._interval)*self._interval
            self._current_dict = {'timestamp' : self._current_time}
        return self._current_dict

    def add_datapoint(self,key,value,adder,initializer):
        current_dict = self.get_dict()
        if not key in current_dict:
            current_dict[key] = initializer()
        current_dict[key] = adder(current_dict[key],value)

    def __del__(self):
        self.write_dict()
