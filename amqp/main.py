#!/usr/bin/python

__author__ = "Weqaar Janjua"
__copyright__ = "Copyright (C) 2016 Linux IoT"
__revision__ = "$Id$"
__version__ = "0.2"

import signal
import threading
import os
from time import *
# Proprietary Code
from FILTER_queue_singleton import *
from CFAR_queue_singleton import *
from CFAR import *
from AMQP import *
from serial_FILTER import *
from sysconfigx import *


class sysinit():
	def __init__(self):
		global sys_obj
		pass

	def run(self):
		sys_obj = Parser_Functions()
		sys_obj.parser_init()
		sys_obj.conf_map = sys_obj.ConfigSectionMap()


class serial_IO_FILTER(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		global _serial_FILTER

	def run(self):
		_serial_FILTER = Serial_Functions_FILTER()
		_serial_FILTER.serial_init_FILTER()
		_serial_FILTER.flush_buffer()
        	while True:
            		sleep(0.01)
			_ser_data = _serial_FILTER.serial_readline()
			if _ser_data is False:
				pass
			elif '+' in _ser_data:
				pass
			elif _ser_data.startswith('OK'):
				print "_ser_data.startswith('OK')\n"
				pass
			else:
				CFAR_queue.get_lock()
				CFAR_queue.put(_ser_data)
				CFAR_queue.release_lock()
	


class CFAR_Thread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		_CFAR = CFAR_Functions()
		while True:
			sleep(0.01)
			_CFAR.process_data()


class AMQP_Thread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		_AMQP = AMQP_Functions()
		while True:
			sleep(0.01)
			_AMQP.process_data()


def main():
	sysinit_obj = sysinit()
	sysinit_obj.run()

	_print_header()

    	# Initialize local queues
	global FILTER_queue
	FILTER_queue = outbound_FILTER_queue()
	
	global CFAR_queue
	CFAR_queue = outbound_CFAR_queue()

    	# Spawn Threads
	t0 = serial_IO_FILTER()
	t0.start()

	t1 = CFAR_Thread()
	t1.start()

	t2 = AMQP_Thread()
	t2.start()


def _print_header():
	_marker = '-------------------------------------------'
        _n = '\n'
	print _n + _marker
	print "Process name:" + __file__ + _n
	print "Author: " + __author__ + _n 
	print "Copyright: " + __copyright__ + _n
	print "Version: " + __version__ + _n
	print _marker + _n
	return 

if __name__ == '__main__':
        main()

