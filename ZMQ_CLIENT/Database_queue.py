import multiprocessing

class db_queue (object):
   	_queue = None
	_lock = None

	def __init__ (self):
        	global _queue
		global _lock
        	_queue = multiprocessing.Queue() 
		_lock = multiprocessing.Lock()

	def put (self, data):
		'''host_queue.put(data, block=True, timeout=None)'''
		_queue.put(data)

	def get (self):
		if self.is_empty() is True:
			return False
		else:
			return _queue.get()

	def get_nowait (self):
		return _queue.get_nowait()

	def get_lock (self):
		_lock.acquire()
	
	def release_lock (self):
		_lock.release()

	def close_queue (self):
		_queue.close()

	def is_empty (self):
		if _queue.empty():
			return True
		else:
			return False

