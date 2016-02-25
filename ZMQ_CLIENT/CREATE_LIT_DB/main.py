from LIT_DATABASE import MK_LIT_DB

host="192.168.122.10"
user="litadmin"
passwd="litadmin123"
DB ="LITdb"
mkdb = MK_LIT_DB(host,user,passwd,DB)
mkdb.mk_db()

