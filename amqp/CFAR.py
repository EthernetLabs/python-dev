import multiprocessing
import json
from sysconfigx import *
from CFAR_queue_singleton import *
from FILTER_queue_singleton import *
from ringbuffer import *
import string
import time

class CFAR_Functions():

	def __init__(self):
		global FILTER_queue
		FILTER_queue = outbound_FILTER_queue()
	
		global CFAR_queue
		CFAR_queue = outbound_CFAR_queue()

		global alert_dict
		alert_dict = {'DEVID': 0.0}
	
		global sensor_dict
		sensor_dict = {'NetID' : '' , 'DevID' : '' , 'Dev_Type' : '' , 'Mesg_Type' : '' , \
			       'Priority' : '' , 'Seqnum' : '' , 'PDU' : ''}

		global json_object
		json_object = None

		global _queue_pass
		_queue_pass = 0

		self.parse = Parser_Functions()
		self.parse.parser_init()
		self.parse.ConfigSectionMap()

		global _cfar_expiry
		_section = 'CFAR'
		_cfar_expiry = int(self.parse.getSectionOption(_section, 'cfar_expiration'))

		global _auth_key
		_section_auth = 'AUTH'
		_auth_key = str(self.parse.getSectionOption(_section_auth, 'auth_key'))

		global _ringbuf_size
		global _ringbuf_activation
		_section_filter = 'FILTER'
		_ringbuf_size = int(self.parse.getSectionOption(_section_filter, 'ringbuffer_size'))
		_ringbuf_activation = int(self.parse.getSectionOption(_section_filter, 'ringbuffer_activate'))

		global _ringbuff
		_ringbuff = RingBuffer(_ringbuf_size)


	def process_data(self):
		if(CFAR_queue.is_empty() is True):
			_queue_it = 0
		else:
			_data = CFAR_queue.get()
			if _ringbuf_activation == 1:
				if self.ringbuffer_verify(_data) is False:
					_queue_it = 0
					#pass
				else:
					_queue_it = self.create_sensor_data(_data)
			else:
				_queue_it = self.create_sensor_data(_data)

		if _queue_it == 1:
			_json = self.create_json()
			print "JSON Formated: " + _json + "\n"
			self.queue_out_data(_json)		
		else:
			json_object = None


	def create_json(self):
		json_object = str(sensor_dict['NetID']) + ":" + str(sensor_dict['DevID']) + ":" + \
		      	      str(sensor_dict['Dev_Type']) + ":" + str(sensor_dict['Mesg_Type']) + ":" + \
		      	      str(sensor_dict['PDU'])
		return json_object


	def create_sensor_data(self, _data):
		sensor_dict['NetID'] = _data[1:3]
		sensor_dict['DevID'] = str(_data[3:5])
		sensor_dict['Dev_Type'] = str(_data[5])
		sensor_dict['Mesg_Type'] = str(_data[6])
		sensor_dict['Priority'] = str(_data[7])
		sensor_dict['Seqnum'] = str(_data[8:10])
			
		# A = Alert
		if sensor_dict['Mesg_Type'] == 'A':
			_sensor_head_no = str(_data[10:])
			#_sensor_head_no_prepend = '0,'
			#sensor_dict['PDU'] = _sensor_head_no_prepend = '0,' + _sensor_head_no
			sensor_dict['PDU'] = _sensor_head_no
			# DEBUG
			print "\nAlert Detected on device: " + sensor_dict['DevID'] + "\n"

			#CFAR - START
			if sensor_dict['DevID'] in alert_dict:
				_current_stamp = time.time()
				_elapsed = _current_stamp - float(alert_dict[sensor_dict['DevID']])
				if _elapsed < _cfar_expiry:
					print "Elapsed < _cfar_expiry - is: " + str(_elapsed) + "\n"
					#alert_dict[sensor_dict['DevID']] = _current_stamp 
					_queue_pass = 0
				else:
					alert_dict[sensor_dict['DevID']] = _current_stamp 
					_queue_pass = 1
			else:
				_current_stamp = time.time()
				alert_dict[sensor_dict['DevID']] = _current_stamp 
				_queue_pass = 1
			#CFAR - END
		# G = GPS
		elif sensor_dict['Mesg_Type'] == 'G':
			_gps_str = str(_data[10:]).split(',')
			if len(_gps_str[0]) < 1:
				print "Device: " + sensor_dict['DevID'] + " GPS data invalid! len(_gps_str[0]) < '1'\n"
				_queue_pass = 0
			elif _gps_str[0] == "":
				print "Device: " + sensor_dict['DevID'] + " GPS data invalid! elif _gps_str[0] is ""\n"
				_queue_pass = 0
			else:
				print "gps raw is: " + _data[10:] + "\n"
				_gps_formatted = self.kill_murphy(_gps_str)
				_lat = _gps_formatted[0]
				_lon = _gps_formatted[1]
				_alt = _gps_str[2]
				sensor_dict['PDU'] = _lat + ',' + _lon + ',' + _alt
				_queue_pass = 1
		# S = Status
		elif sensor_dict['Mesg_Type'] == 'S':
			_status = str(_data[10:])
			if _status.isdigit():
				print "STATUS is: " + _status + "\n"
				if _status == '9':
					print "Device: " + sensor_dict['DevID'] + \
					      " trying to lock GPS....\n"	
					_queue_pass = 1
					sensor_dict['PDU'] = _status
				elif _status == '10':
					print "Device: " + sensor_dict['DevID'] + " GPS lock failed!\n"
					_queue_pass = 1
					sensor_dict['PDU'] = _status
				elif _status == '1':
					print "Device: " + sensor_dict['DevID'] + " Turned ON!\n"
					_queue_pass = 1
					sensor_dict['PDU'] = _status
				elif _status == '0':
					print "Device: " + sensor_dict['DevID'] + " Turned OFF!\n"
					_queue_pass = 1
					sensor_dict['PDU'] = _status
				else:
					print "Device: " + sensor_dict['DevID'] + \
					      " sent Invalid Status Message!\n"
					_queue_pass = 0
			else:
					print "Device: " + sensor_dict['DevID'] + \
					      " sent Invalid Status Message: NAN!\n"
					_queue_pass = 0
		
		# B = Battery
		elif sensor_dict['Mesg_Type'] == 'B':
			_battery = str(_data[10:])
			sensor_dict['PDU'] = _battery
			_queue_pass = 1

		# R = Registration/Authentication
		elif sensor_dict['Mesg_Type'] == 'R':
			_registration = str(_data[10:])
			if ',' in _registration:
				_mac = _registration.split(',')[0]
				_key = _registration.split(',')[1]
				if _key == _auth_key:
					sensor_dict['PDU'] = _registration
					_queue_pass = 1
				else:
					print "AUTHENTICATION FAILED FROM DEVICE: " + sensor_dict['DevID'] + "\n"
					_queue_pass = 0
			else:
				_queue_pass = 0
	
		# H = Heartbeat
		elif sensor_dict['Mesg_Type'] == 'H':
			_heartbeat = str(_data[10:])
			if _heartbeat.isdigit():
				sensor_dict['PDU'] = _heartbeat
				_queue_pass = 1
			else:
				_queue_pass = 0
			
		# Invalid Message		
		else:
			print "Invalid Data\n"
			_queue_pass = 0

		return _queue_pass


	def kill_murphy(self, gps_coords):
		gps_coords[0] = str(self.toDecimalDegrees(gps_coords[0]))
		gps_coords[1] = str(self.toDecimalDegrees(gps_coords[1]))
		return gps_coords

	def toDecimalDegrees(self, ddmm):
		splitat = string.find(ddmm, '.') - 2
		return self._float(ddmm[:splitat]) + self._float(ddmm[splitat:]) / 60.0

	def _float(self, s):
		if s:
			return float(s)
		else:
			return None

	def concatinate(self, data1 , data2):
		temp = data1 << 8
		final = temp | data2
		return final

	def queue_out_data(self, _jobject):
		FILTER_queue.get_lock()
		FILTER_queue.put(_jobject)
		FILTER_queue.release_lock()

	# Checks for duplicate messages transmitetd over RF
	# Returns: True if match not found, False if match found
	def ringbuffer_verify(self, _data_):
		_md5_hash = _ringbuff.md5_generate(_data_)
		if (_ringbuff.search(_md5_hash) == 0):
			_ringbuff.append(_md5_hash)
			return True
		else:
			return False

