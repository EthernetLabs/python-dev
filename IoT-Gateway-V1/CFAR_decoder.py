from CFAR import CFAR_Functions
import threading
from time import *

class CFAR_Thread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		_CFAR = CFAR_Functions()
		while True:
			sleep(0.01)
			_CFAR.process_data()
