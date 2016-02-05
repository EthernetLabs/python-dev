import serial
import os
from sysconfigx import *

class Serial_Functions_FILTER():

	def __init__(self):
		self.parse = Parser_Functions()
		self.parse.parser_init()
		self.parse.ConfigSectionMap()

	def serial_init_FILTER(self):
		_section = 'SERIAL'
		_device = self.parse.getSectionOption(_section, 'device')
		_baudrate = int(self.parse.getSectionOption(_section, 'baudrate'))
		_parity = self.parse.getSectionOption(_section, 'parity')
		_stopbits = int(self.parse.getSectionOption(_section, 'stopbits'))
		_bytesize = int(self.parse.getSectionOption(_section, 'bytesize'))
		_timeout = float(self.parse.getSectionOption(_section, 'timeout'))
		_inter_byte_delay = float(self.parse.getSectionOption(_section, 'inter_byte_delay'))
		try:
			self.ser = serial.Serial (port = _device, baudrate = _baudrate, timeout = _timeout, \
			   			  interCharTimeout = _inter_byte_delay, parity = _parity, \
						  stopbits = _stopbits, bytesize = _bytesize)
		except serial.SerialException:
			print "Serial Port Exception: " + _device + "\n"
            		return False
		self.ser.flush()

	def serial_write(self, _cmd):
		self.ser.write(_cmd)
		print "wrote: " + _cmd

	def serial_readline(self):
		_port_data = self.ser.readline().strip()
		if _port_data is None:
			return False
		elif _port_data is "":
			return False
		else:
			print "SERIAL: " + _port_data + "\n"
			return _port_data

	def get_serial_conf(self):
		print self.ser.getSettingsDict()

	def flush_buffer(self):
		self.ser.flush()

