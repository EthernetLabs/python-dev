from serial_frame import serial_get
from COAP_queue import coap_queue
import threading
from time import *



class serial_data_in(threading.Thread):
	def __init__(self,ser):
		threading.Thread.__init__(self)
		self.ser = ser
		global _serial_data_in

	def run(self):
                write = serial_get(self.ser)
                queue = coap_queue()
                
        	while True:
                        print threading.currentThread(), 'Thread - 1 Starting'
            		sleep(2)
			queue.get_lock()
			_ser_data_in=queue.get()
			if _ser_data_in == False:
                            print "Queue is Empty!!!"
                        else:
                            print "Get Data from Queue = "
                            print _ser_data_in
                            queue.release_lock()
                            write.serial_write(_ser_data_in)   
                        print threading.currentThread(), 'Thread - 1 Exiting'



##from COAP_queue import coap_queue
##import threading
##from time import *
##
##
##class serial_data_in(threading.Thread):
##	def __init__(self):
##		threading.Thread.__init__(self)
##		global _serial_data_in
##
##	def run(self):
##                queue = coap_queue()
##                
##        	while True:
##                        print threading.currentThread(), 'Thread - 1 Starting'
##            		sleep(1)
##			queue.get_lock()
##			a=queue.get()
##			print "Get Data from Queue = "
##			print a
##			queue.release_lock()
##                        print threading.currentThread(), 'Thread - 1 Exiting'
##                        
