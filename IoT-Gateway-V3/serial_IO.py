from serial_frame import serial_get
from serial_raw_queue import serial_queue
import threading
from time import *


class serial_data(threading.Thread):
	def __init__(self,ser):
		threading.Thread.__init__(self)
		self.ser = ser
		global _serial_data

	def run(self):
                s = serial_get(self.ser)
                queue = serial_queue()
                
        	while True:
                        print threading.currentThread(), 'Thread - 0 Starting'
            		sleep(2)
			_ser_data = s.serial_readline()
			if _ser_data is False:
				pass
			elif _ser_data == "NULL":
				pass
			else:
				queue.get_lock()
				queue.put(_ser_data)
				print "Write Data to Queue = "
				print str(_ser_data)
				queue.release_lock()
				s.flush_buffer()
                        print threading.currentThread(), 'Thread - 0 Exiting'
                        sleep(2)
                        
