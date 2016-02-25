#!/usr/bin/python

import MySQLdb as _sql
import sys

class MK_LIT_DB():
	def __init__(self,host,user,passwd,database):
		self.host = host
		self.user = user
		self.passwd = passwd
		self.database = database

	def mk_db (self):
		try:
			db = _sql.connect(self.host,self.user,self.passwd,self.database)
			cursor = db.cursor()
			cursor.execute("DROP TABLE IF EXISTS LITFRAME")

			# Create a table as per requirement

			_LITFRAME =""" CREATE TABLE LITFRAME (
				NETID CHAR(2) NOT NULL,
				SRCID CHAR(2) NOT NULL,
				DEVTYPE CHAR(1) NOT NULL,
				TOM CHAR(1) NOT NULL,
				PDU CHAR(80) NOT NULL
				)"""
			cursor.execute(_LITFRAME)
			print "Yes LIT FRAME TABLE IS initiallized Succesfully!!!"
		
		except _sql.Error, e:
			print "Error %d: %s" % (e.args[0],e.args[1])
			sys.exit(1)
		
		finally:
			if db:
				db.close()





