#!/usr/bin/python

import MySQLdb as sql
import threading
from Database_queue import db_queue 
from time import *



class LIT_DB_Thread(threading.Thread):
	def __init__(self,db,cursor):
		threading.Thread.__init__(self)
		self.db=db
		self.cursor=cursor
		self.queue = db_queue()
		
	def run(self):
			while True:
				sleep(0.02)
				if self.queue.is_empty() == True:
					pass
				else:
				
					packet = self.queue.get()
					print "packet = " + packet
					split_pkt = packet.split(':')
					FRAME = """INSERT INTO LITFRAME (
						NETID,SRCID,DEVTYPE,TOM,PDU)
						VALUES ('%s','%s','%s','%s','%s'
						)""" % (split_pkt[0],split_pkt[1],split_pkt[2],split_pkt[3],split_pkt[4])
					self.cursor.execute(FRAME)
					self.db.commit()
					results = self.cursor.fetchall()
					print "Written ON Database"
