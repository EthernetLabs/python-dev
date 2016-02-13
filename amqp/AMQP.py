import pika
import multiprocessing
from sysconfigx import *
from FILTER_queue_singleton import *
import socket

class AMQP_Functions():

	def __init__(self):
		global FILTER_queue
		FILTER_queue = outbound_FILTER_queue()

		global _data
		global _queue_host
		global _queue_port
		global _queue_name
		global _routing_key
		global _heartbeat_interval

		global _data

		_data = None

		self.parse = Parser_Functions()
		self.parse.parser_init()
		self.parse.ConfigSectionMap()

		_section = 'AMQP'
		_queue_host = self.parse.getSectionOption(_section, 'qhost')
		_queue_port = int(self.parse.getSectionOption(_section, 'qport'))
		_queue_name = self.parse.getSectionOption(_section, 'queue_name')
		_routing_key = self.parse.getSectionOption(_section, 'routing_key')
		_heartbeat_interval = int(self.parse.getSectionOption(_section, 'heartbeat_interval'))

                while self.test_network(_queue_host, _queue_port) is False:
                        print "Retrying connection to AMQP Service...."

		self.amqp_connection = pika.BlockingConnection(pika.ConnectionParameters(host=str(_queue_host)))
		self.amqp_channel = self.amqp_connection.channel()
		self.amqp_channel.queue_declare(queue=str(_queue_name), durable=True)
		self.amqp_heartbeat = pika.heartbeat.HeartbeatChecker(self.amqp_connection, _heartbeat_interval)


        def test_network(self, ip_address, port, timeout=1):
	        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        	s.settimeout(timeout)
                result = s.connect_ex((ip_address, port))
                s.close()
                if(result == 0):
	                return True
                else:
                        return False
                                

	def amqp_connect_status(self):
		if self.amqp_connection.is_open is True:
			return True
		else:
			return False


	def process_data(self):
		if self.amqp_connect_status() is False:
			self.amqp_connection = pika.BlockingConnection(pika.ConnectionParameters\
					       (host=str(_queue_host)))
			self.amqp_channel = self.amqp_connection.channel()
			self.amqp_channel.queue_declare(queue=str(_queue_name), durable=True)
			self.amqp_heartbeat = pika.heartbeat.HeartbeatChecker(self.amqp_connection, _heartbeat_interval)
		else:
			if(FILTER_queue.is_empty() is True):
				pass
			else: 
				FILTER_queue.get_lock()
				_data = FILTER_queue.get()
				FILTER_queue.release_lock()
				self.amqp_channel.basic_publish(exchange='', routing_key=str(_routing_key),\
 							   body=str(_data), properties=pika.BasicProperties(delivery_mode = 2,))
				print 'AMQP: Data is: ' + str(_data) + '\n'


	def close(self):
		self.amqp_connection.close()

