from sqlite3 import *
con = None
try:
	con = connect("sms.db")
	print("connected")
	rno = int(input("enter rno to insert "))
	name = input("enter name to insert ")
	marks = int(input("enter marks to insert "))
	args = (rno, name, marks)
	cursor = con.cursor()
	sql = "insert into student values('%d', '%s', '%d')"
	cursor.execute(sql % args)
	con.commit()
	print("record added")
except Exception as e:
	print("insert issue ", e)
	con.rollback()
finally:
	if con is not None:
		con.close()
		print("disconnected")