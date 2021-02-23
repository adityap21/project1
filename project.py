from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from sqlite3 import *
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sqlite3
import socket
import requests
import bs4
import json


root = Tk()
root.title("S.M.S")
root.geometry("630x500+400+100")
root.configure(bg='ghostwhite')

def f1():
	root.withdraw()
	adst.deiconify()

def f2():
	adst.withdraw()
	root.deiconify()

def f3():
	stdata.delete(1.0,END)
	visit.deiconify()
	root.withdraw()
	con = None	
	try:
		con =connect("sms.db")
		#print("connected")
		cursor = con.cursor()
		sql = "select * from student"
		cursor.execute(sql)
		data = cursor.fetchall()
		info = ""
		for d in data:
			info = info +"Rno = "+str(d[0])+" Name = "+str(d[1])+" Marks = "+str(d[2]) + "\n"
		stdata.insert(INSERT, info)		
		stdata.configure(state = 'disabled')
	except Exception as e:
		print("select issue ", e)
		con.rollback()

	finally:
		if con is not None:
			con.close()
			#print("disconnected")

def f4():
	visit.withdraw()
	root.deiconify()
	
def f5():
	con = None
	try:
		con = connect("sms.db")
		#print("connected")
		#rno = int(entAddRno.get())
		#name = entAddName.get()
		#marks = int(entAddMarks.get())
		cursor = con.cursor()
		sql = "insert into student values('%d', '%s', '%d')"
		rno= entAddRno.get()
		if not rno.isdigit():
			showerror("failed", "rno must be +ve integer")
			entAddRno.delete(0,END)
			entAddRno.focus()
			return
		rno = int(rno)
		name = entAddName.get()
		if not name.isalpha():
			showerror("failed", "name shud be alphabates")
			entAddName.delete(0,END)
			entAddName.focus()
			return
		if len(name) < 2:
			showerror("failed", "name must contain atleast 2 letters")
			entAddName.delete(0,END)
			entAddName.focus()
			return
		marks = entAddMarks.get()
		if not marks.isdigit():
			showerror("failed", "marks shud be integer")
			entAddMarks.delete(0,END)
			entAddMarks.focus()
			return
		marks = int(marks)
		if marks < 0 or marks > 100:
			showerror("failed", "marks shud be in range(0-100)")
			entAddMarks.delete(0,END)
			entAddMarks.focus()
			return
		args =(rno, name, marks)
		cursor.execute(sql % args)
		con.commit()
		stdata.configure(state = 'normal')
		showinfo("success", "record added")				
	except Exception as e:
		showerror("failure", "rno already exists")
		con.rollback()

	finally:
		if con is not None:
			con.close()
	entAddRno.delete(0,END)
	entAddName.delete(0,END)
	entAddMarks.delete(0,END)
	entAddRno.focus()
			#print("disconnected")	

def f6():
	root.withdraw()
	updt.deiconify()

def f10():
	con = None
	try:
		con = connect("sms.db")
		#print("connected")
		cursor = con.cursor()
		sql = "update student set name = '%s', marks= '%d'  where rno = '%d' "
		#rno= int(entupdRno.get())
		#name = entupdName.get()
		#marks = int(entupdMarks.get())
		rno= entupdRno.get()
		if not rno.isdigit():
			showerror("failed", "rno must be +ve integer")
			entupdRno.delete(0,END)
			entupdRno.focus()
			return
		rno = int(rno)
		name = entupdName.get()
		if not name.isalpha():
			showerror("failed", "name shud be alphabates")
			entupdName.delete(0,END)
			entupdName.focus()
			return
		if len(name) < 2:
			showerror("failed", "name must contain atleast 2 letters")
			entupdName.delete(0,END)
			entupdName.focus()
			return
		marks = entupdMarks.get()
		if not marks.isdigit():
			showerror("failed", "marks shud be integer")
			entupdMarks.delete(0,END)
			entupdMarks.focus()
			return
		marks = int(marks)
		if marks < 0 or marks > 100:
			showerror("failed", "marks must be in range(0-100)")
			entupdMarks.delete(0,END)
			entupdMarks.focus()
			return
		args =(name, marks, rno)
		cursor.execute(sql % args)
		con.commit()
		stdata.configure(state = 'normal')
		if cursor.rowcount >= 1:
			showinfo("success", "record updated")
		else:
			showerror("failed", "rno does not exists")
			
	
	except Exception as e:
		con.rollback()
		#print("failure", "update issue ", e)
		showerror("failure", e)
			

	finally :
		if con is not None :
			con.close()
	entupdRno.delete(0,END)
	entupdName.delete(0,END)
	entupdMarks.delete(0,END)
	entupdRno.focus()
			#print("disconnected")


def f7():
	root.withdraw()
	delt.deiconify()

def f8():
	con = None
	try:

		con = connect("sms.db")
		#print("connected")
		rno = int(entdelRno.get())
		args =(rno)
		cursor = con.cursor()
		sql = "delete from student where rno = '%d' "
		cursor.execute(sql % args)
		if rno < 1:
			showerror("failed", "rno must be +ve")
		elif cursor.rowcount >= 1:
			con.commit()
			stdata.configure(state = 'normal')
			info = str(cursor.rowcount) + "record deleted"
			showinfo("deleted", "record deleted")
		else:
			showerror("Sorry", "rno not found")
			
	except Exception as e:
		#print("failure", "delete issue ", e)
		showerror("failure", "plz enter integer")
		con.rollback()	

	finally :
		if con is not None :
			con.close()
			entdelRno.delete(0,END)
			entdelRno.focus()
			#print("disconnected")


def f9():
	updt.withdraw()
	root.deiconify()

def f11():
	delt.withdraw()
	root.deiconify()

def f12():
	con = None	
	try:
		con = connect("sms.db")
		data = pd.read_sql_query("select name, marks from student order by marks DESC limit 5", con)
		#print(data.head(10))
		name = data["name"].tolist()
		marks = data["marks"].tolist()
		plt.bar(name, marks, width=0.50, label = 'marks')
		plt.xlabel("Name Of Students")
		plt.ylabel("Marks")
		plt.title("Top 5 Students")
		plt.grid()
		plt.legend(shadow = True)
		plt.show()

	except Exception as e:
		print("chart issue ", e)
		con.rollback()

	finally :
		if con is not None :
			con.close()
			#print("disconnected")




res = requests.get("https://www.brainyquote.com/quote_of_the_day")
#print(res)

soup = bs4.BeautifulSoup(res.text, "lxml")
#print(soup)


data = soup.find("img", {"class" :"p-qotd"})
#print(data)


text = data['alt']
#print(text)


img_url = "https://www.brainyquote.com" + data["data-img-url"]
#print(img_url)


#res = requests.get(img_url)
#f = open("iml.jpg", "wb")
#f.write(res.content)
#f.close()


socket.create_connection( ("www.google.com", 80) )
#print("u r connected ")
res = requests.get("https://ipinfo.io")
#print(res)
data = res.json() # res into dict ==> key & value
#print(data)
ip = data['ip']
#print(ip)
city = data['city']
#print(city)
loc = data['loc']
#print(loc)
info = loc.split(",")
#print("lat = ", info[0])
#print("lon = ", info[1])
socket.create_connection( ("www.google.com", 80))
#city = input("enter location name")
	
# base URL
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?units=metric"
city = "Mumbai"
data = res.json() # res into dict ==> key & value
#print(data)
API_KEY = "c6e315d09197cec231495138183954bd"
# updating the URL
URL = BASE_URL + "&q=" + city + "&appid=" + API_KEY
# HTTP request
response = requests.get(URL)
# checking the status code of the request

# getting data in the json format
data = response.json()
#print(data)
# getting the main dict block
main = data['main']
# getting temperature
temperature = main['temp']
temp = temperature - 273.15
# getting the humidity
humidity = main['humidity']
# getting the pressure
pressure = main['pressure']
   # weather report
report = data['weather']
#print(f"{CITY:-^30}")
#print(f"Temperature: {temperature}")
#print(f"Humidity: {humidity}")
#print(f"Pressure: {pressure}")
#print(f"Weather Report: {report[0]['description']}")



btnAdd = Button(root , text="ADD" , width = 18 , bg='Pink', font =('arial',15,'bold'), command=f1)
btnView = Button(root , text="VIEW" , width = 18, bg='Pink', font =('arial',15,'bold'), command=f3)
btnUpdate = Button(root , text="UPDATE" , width = 18, bg='Pink', font =('arial',15,'bold'), command=f6)
btnDelete = Button(root , text="DELETE" , width = 18 , bg='Pink', font =('arial',15,'bold'), command=f7)
btnChart = Button(root , text="CHART" , width = 18 , bg='Pink', font =('arial',15,'bold'), command=f12)
frame2 = Frame(root)
frame2.pack()
upperframe = Frame(root,highlightbackground="black",highlightthickness=2,bg='Pink')

upper_location = Label(upperframe, text = " Location: " + str(city) + "              " + "Temp: " + str(temperature) +"" +".C", font=("courier",15,'bold'),bg='Pink',width=300,anchor=W,wraplength=615)



frame1 = Frame(root)
frame1.pack()
bottomframe = Frame(root,highlightbackground="black",highlightthickness=2,bg='Pink')

bottom_location = Label(bottomframe, text = " QOTD: " + str(text), font=("courier",15,'bold'),bg='Pink',width=300,anchor=W,wraplength=615)


bottomframe.pack(side = BOTTOM)
bottom_location.pack(pady=20)
btnAdd.pack(pady=10)
btnView.pack(pady=10)
btnUpdate.pack(pady=10)
btnDelete.pack(pady=10)
btnChart.pack(pady=10)
upperframe.pack()
upper_location.pack(pady=20)


adst = Toplevel(root)
adst.title("Add St. ")
adst.geometry("500x500+200+200")

lblAddRno = Label(adst , text="Enter roll no", font=('arial' , 16 ,'bold italic '))
entAddRno = Entry(adst , bd = 10 ,font=('arial' , 16 ,'bold italic '))

lblAddName = Label(adst , text="Enter Name", font=('arial' , 16 ,'bold italic '))
entAddName= Entry(adst , bd = 10 ,font=('arial' , 16 ,'bold italic '))

lblAddMarks = Label(adst , text="Enter Marks", font=('arial' , 16 ,'bold italic '))
entAddMarks= Entry(adst , bd = 10 ,font=('arial' , 16 ,'bold italic '))

btnAddSave = Button(adst , text = "Save" ,font=('arial' , 16 , 'bold italic'), command=f5)

btnAddBack = Button(adst , text = "Back" ,font=('arial' , 16 , 'bold italic'), command=f2)


lblAddRno.pack(pady=10)
entAddRno.pack(pady=10)
lblAddName.pack(pady=10)
entAddName.pack(pady=10)
lblAddMarks.pack(pady=10)
entAddMarks.pack(pady=10)
btnAddSave.pack(pady=10)
btnAddBack.pack(pady=10)

adst.withdraw()


visit = Toplevel(root)
visit.title("View St.")
visit.geometry("500x500+200+200")

stdata = ScrolledText(visit , width=40 , height =25)
btnViewBack = Button(visit , text = "Back" ,font=('arial' , 16 ,'bold italic '), command=f4)

stdata.pack(pady=10)
btnViewBack.pack(pady=10)
visit.withdraw()


updt = Toplevel(root)
updt.title("Update St.")
updt.geometry("500x500+200+200")

lblupdRno = Label(updt, text="Enter roll no", font=('arial' , 16 ,'bold italic'))
entupdRno = Entry(updt , bd = 10 ,font=('arial' , 16 ,'bold italic '))

lblupdName = Label(updt , text="Enter New Name", font=('arial' , 16 ,'bold italic'))
entupdName= Entry(updt , bd = 10 ,font=('arial' , 16 ,'bold italic '))

lblupdMarks = Label(updt, text="Enter New Marks", font=('arial' , 16 ,'bold italic'))
entupdMarks= Entry(updt , bd = 10 ,font=('arial' , 16 ,'bold italic '))

btnupdSave = Button(updt , text = "Save" ,font=('arial' , 16 ,'bold italic '), command=f10)

btnupdBack = Button(updt , text = "Back" ,font=('arial' , 16 ,'bold italic '), command=f9)


lblupdRno.pack(pady=10)
entupdRno.pack(pady=10)
lblupdName.pack(pady=10)
entupdName.pack(pady=10)
lblupdMarks.pack(pady=10)
entupdMarks.pack(pady=10)
btnupdSave.pack(pady=10)
btnupdBack.pack(pady=10)

updt.withdraw()

delt = Toplevel(root)
delt.title("Delete St.")
delt.geometry("550x550+200+200")

lbldelRno = Label(delt , text="Enter roll no to delete", font=('arial' , 16 ,'bold italic '))
entdelRno = Entry(delt , bd = 10 ,font=('arial' , 16 ,'bold italic '))

btndelSave = Button(delt , text = "Delete" ,font=('arial' , 16 ,'bold italic '), command=f8)

btndelBack = Button(delt , text = "Back" ,font=('arial' , 16 ,'bold italic '), command=f11)


lbldelRno.pack(pady=10)
entdelRno.pack(pady=10)
btndelSave.pack(pady=10)
btndelBack.pack(pady=10)

delt.withdraw()


root.mainloop()