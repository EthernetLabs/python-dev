#!/usr/bin/python

__author__ = "Weqaar Janjua"
__copyright__ = "Copyright (C) 2016 Linux IoT"
__revision__ = "$Id$"
__version__ = "0.1"

import zmq
import sys
import signal
import threading
import os
import ConfigParser
import socket
import puka
import errno
from time import *
# Proprietary Code
from inbound_queue_singleton import *
from outbound_queue_singleton import *


class ZMQ_Router_Inbound_Thread_HLL(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		context = zmq.Context()
		print "Starting High-latency Service"
		socket = context.socket(zmq.PULL)
		socket.connect ("tcp://" + _meg_device_ip + ":%s" % _port_high_latency)
		print "Started, polling for messages (PULL) from: " + _meg_device_ip + "\n"
		poller = zmq.Poller()
		poller.register(socket, zmq.POLLIN)

        	while True:
			sleep(0.02)
			socks = dict(poller.poll())
        		if socket in socks and socks[socket] == zmq.POLLIN:
                		message = socket.recv()
				print message
			if message is None:
				pass
			else:
				inbound_queue.get_lock()
				inbound_queue.put(message)
				inbound_queue.release_lock()


class ZMQ_Router_Inbound_Thread_LLL(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		context = zmq.Context()
		print "Starting Low-latency Service"
		socket = context.socket(zmq.SUB)
		socket.setsockopt (zmq.SUBSCRIBE, '')
		socket.connect ("tcp://" + _meg_device_ip + ":%s" % _port_low_latency)
		print "Started, listening for messages (SUB) from: " + _meg_device_ip + "\n"

        	while True:
			sleep(0.02)
			message = socket.recv()
			print message
			if message is None:
				pass
			else:
				inbound_queue.get_lock()
				inbound_queue.put(message)
				inbound_queue.release_lock()


class AMQP_Router_Inbound_Thread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

        def test_network(self, ip_address, port, timeout=3):
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.settimeout(timeout)
                        result = s.connect_ex((ip_address, port))
                        s.close()
                        if(result == 0):
                                return True
                        else:
                                return False

	def _connect_amqp(self):
		global client
		client = puka.Client("amqp://" + _qhost + ":" + _qport)
		try:
			promise = client.connect()
			client.wait(promise)
			print "Connection Successful!\n"
			return True
		#except puka.ConnectionBroken:
		except Exception as e:
			print "Connection Failed: " + str(e) + "\n"
			return False
		


	def run(self):
                #while self.test_network(_qhost, _qport) is False:
                #        print "Retrying connection to AMQP Host Service to %r...." % (_qhost,)
		_conn_status = self._connect_amqp()
		if _conn_status is False:
			pass
		else:
			try:
				promise = client.queue_declare(queue=str(_queue_inbound_name))
				client.wait(promise)
			except puka.PreconditionFailed:
   				promise = client.queue_declare(queue=str(_queue_inbound_name), durable=True)
				client.wait(promise)

			while True:
				sleep(0.02)
				if inbound_queue.is_empty() is True:
					pass
				else:
					inbound_queue.get_lock()
					message = inbound_queue.get()
					client.basic_publish(exchange='', routing_key=str(_routing_inbound_key), \
			           			     body=str(message))
				#client.wait(promise)
					inbound_queue.release_lock()


def main():
	_print_header()

	#global conf_file
	conf_file = "CZS.conf"

	#Initialize Config Parameters
	_conf = ConfigParser.ConfigParser()
	_conf.read(conf_file)

	#Read CZS Section
	_section = 'CZS'
	_high_latency = int(_conf.get(_section, 'high_latency'))
	_low_latency = int(_conf.get(_section, 'low_latency'))

	#Read ZMQ Section
	_section = 'ZMQ'
	global _port_high_latency
	global _port_low_latency
	global _meg_device_ip
	_port_high_latency = _conf.get(_section, 'port_high_latency')
	_port_low_latency = _conf.get(_section, 'port_low_latency')
	_meg_device_ip = _conf.get(_section, 'meg_device_ip')

	#Read AMQP Section
	_section = 'AMQP'
	global _qhost
	global _qport
	global _queue_inbound_name
	global _routing_inbound_key
	global _queue_outbound_name
	global _routing_outbound_key
	global _heartbeat_interval
	_qhost = _conf.get(_section, 'qhost')
	_qport = _conf.get(_section, 'qport')
	_queue_inbound_name = _conf.get(_section, 'queue_inbound_name')
	_routing_inbound_key = _conf.get(_section, 'routing_inbound_key')
	_queue_outbound_name = _conf.get(_section, 'queue_outbound_name')
	_routing_outbound_key = _conf.get(_section, 'routing_outbound_key')
	_heartbeat_interval = int(_conf.get(_section, 'heartbeat_interval'))

    	# Initialize local queues
	global inbound_queue
	inbound_queue = inbound_queue()
	
	global outbound_queue
	outbound_queue = outbound_queue()

    	# Spawn Threads
	if (_high_latency == 1) and (_low_latency == 1):
		print "ERROR -> Please select either HLL or LLL\n"
		sys.exit(0)
	elif _high_latency == 1:
		t0 = ZMQ_Router_Inbound_Thread_HLL()
		t0.start()
	elif _low_latency == 1:
		t0 = ZMQ_Router_Inbound_Thread_LLL()
		t0.start()
	else:
		print "ERROR -> Please select either HLL or LLL\n"

	t1 = AMQP_Router_Inbound_Thread()
	t1.start()


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

