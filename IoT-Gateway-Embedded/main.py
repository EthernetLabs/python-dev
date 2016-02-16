#!/usr/bin/python

__author__ = "Weqaar Janjua & Ahmer Malik"
__copyright__ = "Copyright (C) 2016 Linux IoT"
__revision__ = "$Id$"
__version__ = "6.0"

from print_header import _header
from init import sysinit
import gc

from serial_config import ser_init
from serial_frame import serial_get
from serial_IO import serial_data
from filter_IO import filter_data
from CFAR_decoder import CFAR_Thread
from time import *
import sys
from GW_COAPTHON import start_coap

sys.path.insert(0, '/home/ahmer/Ahmer/Techknox/Python_Exercises/IoT-Gateway-Embedded/coapthon/')
##from coapthon.server.coap import CoAP
from coapserver import CoAPServer

#Please modify the directory path (_firmware_dir) for the variable below: 
#_firmware_dir = '/opt/IoT-Gateway'
#_firmware_dir = '/home/ahmer/Ahmer/Techknox/Python_Exercises/IoT-Gateway-V2/'
_thread_pool = []




def main():
        # Print headers. Use print_header.py
        h = _header(__file__,__author__,__copyright__,__version__)
        h._print()
        # Initiallize the System. Use init.py
        sysinit_obj = sysinit()
        sysinit_obj.run()
        print "Garbage Collector Enabled: " + str(gc.isenabled()) + "\n"

        # Initiallize the Serial Port
        ser_obj = ser_init()
        ser = ser_obj.serial_init()
        print ser
        #ser_obj.flush_buffer()
        get = serial_get(ser)

        ip = "192.168.10.4"
        port = 5683
        multicast = False

        # Spawn Threads
        t0 = start_coap(ip,port,multicast)
        t0.start()
        _thread_pool.append(t0)
        
        
        # Get Serial Data by spawning thread t0. Use serial_IO.py
        t1 = serial_data(ser)
        t1.start()
        _thread_pool.append(t1)

        # Filter the serial data based on the frame structure.
        t2 = filter_data()
        t2.start()
        _thread_pool.append(t2)

        t3 = CFAR_Thread()
        t3.start()
        _thread_pool.append(t3)




if __name__ == '__main__':
        main()

