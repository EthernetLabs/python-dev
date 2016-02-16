from serial_frame import serial_get
from serial_raw_queue import serial_queue
import threading
from time import *
from frame_FILTER import frame_filter
from CFAR_queue_singleton import *


class filter_data(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        global _filter_data

    def run(self):
        sleep(2)
        f = frame_filter()
        queue = outbound_CFAR_queue()
        while True:
            print threading.currentThread(), 'Thread - 1 Starting - While True\n'
            sleep(2)
            _data = f.read_frame()
            if _data is False:
                print threading.currentThread(), 'Thread - 1 Exiting _data is FALSE\n'
                sleep(2)
                pass
            elif _data == "NULL":
                print threading.currentThread(), 'Thread - 1 Exiting _data == NULL'
                sleep(2)
                pass
            else:
                queue.get_lock()
                queue.put(_data)
                print "PUT Data to Filter Queue = "
                print str(_data)
                queue.release_lock()
                print threading.currentThread(), 'Thread - 1 Exiting CFAR done'
                sleep(2)
