#!/usr/bin/python

import MySQLdb as sql
import threading
from Database_queue import db_queue 
from time import *
import sys

class LIT_DB_OPS():
	def __init__(self):
		pass
		
	def search(self):
				db = sql.connect("192.168.122.10","litadmin","litadmin123","LITdb")
        			cursor = db.cursor()	
				print "Search. . . "
				print "NETID, SRCID, DEVTYPE, TOM, PDU"
				while True:
					sleep(0.02)
					FIELD = input('SEARCH: ')
					VALUE = input('FILTER: ')
					print "INSTANCE:"
					print isinstance(FIELD,str)
					
					#SELECT * FROM LITFRAME WHERE TOM = 'A';
					query = "SELECT * FROM LITFRAME WHERE %s = '%s'" % (FIELD,VALUE)
					print "You have selected %s from %s" %(VALUE,FIELD)  				

					try:
						cursor.execute(query)
						results = cursor.fetchall()
						print "Results = "
						print results
						for row in results:
							netid = row[0]
							srcid = row[1]
							devtype = row[2]
							tom = row[3]
							pdu = row[4]
							print "NETID:%s, SRCID:%s, DEVTYPE:%s, TOM:%s, PDU:%s " % (netid,srcid,devtype,tom,pdu)

					except:
						print "Error: Enable to fetch Data!!! No Such Entry!!!"


	def update(self):
                                db = sql.connect("192.168.122.10","litadmin","litadmin123","LITdb")
                                cursor = db.cursor()
                                while True:
                                        sleep(0.02)
                                        FIELD = input('UPDATE FIELD: ')
                                        OLD_VALUE = input('SEARCH VALUE: ')
					NEW_VALUE = input('NEW VALUE: ')

                                        #SELECT * FROM LITFRAME WHERE TOM = 'A';
                                        query = "UPDATE LITFRAME SET %s = '%s' WHERE %s = '%s'" % (FIELD,NEW_VALUE,FIELD,OLD_VALUE)
                                        print "You have updated field: %s with %s, Having field: %s == %s" %(FIELD,NEW_VALUE,FIELD,OLD_VALUE)

                                        try:
                                                cursor.execute(query)
						db.commit()

                                        except:
                                                print "Error: Enable to Update Data!!!. No such Entry."
						db.rollback()

def main():
	print "Do You want (U)Update or (S)Search"
	IN = input("U/S: ")
	if IN == 'S':
		_search = LIT_DB_OPS()
		_search.search()
	elif IN == 'U':
		_update = LIT_DB_OPS()
		_update.update()
	else:
		"INVALID INPUT. . . Please Type 'S' or 'U'!!!"
		sys.exit()

if __name__ == '__main__':
	main()
