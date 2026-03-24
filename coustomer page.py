from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image,ImageTk
import mysql.connector as con
from dotenv import load_dotenv
import os

load_dotenv()



#tkinter window
root = Tk()
root.title("PHARMACY MANAGMENT SYSTEM")
root.geometry("1250x700")

#msql connection
mycon=con.connect(host="localhost",
    user="root",
    password=os.getenv("PASSWORD"),
    database=os.getenv("DATABASE"))

def cursor1(event=''):
    #focus is used to retrive selected data
    selected_item = medtable.focus() #makes the widget active until termination
    if selected_item:

        #gets the values of selected columns 
        row = medtable.item(selected_item)['values'] 

        #set the stringVar with the data effectively filling in the widgets when selected 
        ref_no.set(row[0])
        med_name.set(row[1])
        stock1.set(row[2])
        price.set(row[3])

        medtable.see(selected_item)

# Function to refresh the Treeview widget and adjust the scrollbar
def refresh_table():
    medtable.delete(*medtable.get_children())  #clearing scrollbar
    cursor = mycon.cursor()
    cursor.execute("SELECT refno,medname,stock,cost FROM medicines")
    rows = cursor.fetchall()
    for row in rows:
        medtable.insert("", END, values=row)
    medtable.yview_moveto(0)  # Reset scrollbar position to the top of the list

# Scrollbar and Treeview

#creating and placing scrollbar frame
sbframe = Frame(root, bd=5, relief=RIDGE, padx=3, pady=3, background="#141D24")
sbframe.place(x=10, y=390, width=480, height=232)

# creating and placing scrollbar
sb = ttk.Scrollbar(sbframe, orient=VERTICAL)
sb.pack(side=RIGHT, fill=Y)

#initializing all the cols for the scrollbar
cols = ("refno", "medname", "stock", "cost")

#treeview allows you to display data in a tabular way 
medtable = ttk.Treeview(sbframe, columns=cols, show="headings")

#giving headings to all the cols 
medtable.heading("refno", text="Reference No.")
medtable.heading("medname", text="Medicine Name")
medtable.heading("stock", text="Units Available")
medtable.heading("cost", text="Price")


#setting the cols in the scrollbar with a particular width
medtable.column("refno", width=50)
medtable.column("medname", width=50)
medtable.column("stock", width=50)
medtable.column("cost", width=50)


medtable.pack(fill=BOTH, expand=0)

# Fetch values from the table and populate the Treeview widget
refresh_table()

# Configure the scrollbar to control the medtable widget
medtable.configure(yscrollcommand=sb.set)    #used to scroll the scrollbar up and down
sb.configure(command=medtable.yview)   

# Binding the cursor1 function to the Treeview selection event meaning that when treeview function happens in the scrollbar
# which is genrally when you select something from the scrollbar its calls the cursor1 function
medtable.bind("<<TreeviewSelect>>", cursor1)



def placeorder():
    f_name = input_fname.get()
    l_name = input_lname.get()
    f_no = input_fno.get()
    app_name = input_appname.get()
    city1 = input_city.get()
    state1 = input_state.get()
    pin_code = input_pincode.get()
    med_name = input_medname.get()
    stock1 = input_stock.get()

    if not f_name or not l_name or not f_no or not app_name or not city1 or not state1 or not pin_code or not med_name or not stock1:
        messagebox.showerror("ERROR", "Please fill all the fields.")
        return

    cursor1=mycon.cursor()
    cursor1.execute("select medname from medicines")
    data=cursor1.fetchall()
    l=[]
    for row in data:
        l.append(row)
    lnew = []
    for i in range(len(l)):
        e=l[i][0]
        lnew.append(e)
    if med_name in lnew:
        # Inserting data into the database
        cursor = mycon.cursor()
        query = "INSERT INTO cust (fname,lname,fno,appname,city,state,pincode,medname,quantity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (f_name,l_name,f_no,app_name,city1,state1,pin_code,med_name,stock1)
        cursor.execute(query, values)
        mycon.commit()
        clear()
        refresh_table()
        messagebox.showinfo("Success", "Order placed. Order will arrive in 4-5 working days")

    else:
        messagebox.showinfo("ERROR","Medicine not found.")


   
    cursor1=mycon.cursor()
    query = "select stock from medicines where medname = %s"
    value = (med_name,)
    cursor1.execute(query, value)
    stock=cursor1.fetchall()
    print(stock)
    st = int(stock[0][0])
    print(st)

    ns = st - int(stock1)
    tup = (ns,med_name)

    cursor2 = mycon.cursor()
    query = "update medicines set stock = %s where medname = %s"
    cursor2.execute(query,tup)
    mycon.commit()
    refresh_table()



def clear():

    #clearing all input fields
    input_fname.delete(0, END)
    input_lname.delete(0, END)
    input_fno.delete(0,END)
    input_appname.delete(0, END)
    input_city.delete(0, END)
    input_state.delete(0,END)
    input_medname.delete(0, END)
    input_stock.delete(0, END)
    input_pincode.delete(0, END)


title = Label(root,text="CUSTOMER WINDOW",bd=15,relief=RIDGE,fg="black",font=("times new roman",30,"bold"),padx=2,pady=4,background="#C3CEDA")
title.pack(side=TOP,fill=X)

# Create StringVar variables
ref_no = StringVar()
med_name = StringVar()
med_type = StringVar()
mfd_dt = StringVar()
exp_dt = StringVar()
presc_by = StringVar()
lot_no = StringVar()
stock1 = StringVar()
price = StringVar()
manufacturer = StringVar()
#stringvar is used to track the changes in the string and auomatically update accosiated widget

#search bar frame
left=LabelFrame(root,bd=10,relief=RIDGE,text="Search Box",fg="black",font=("times new roman",15,"bold"),background="#537180",foreground="#E9E4DF")
left.place(x=10,y=120,width=480,height=250)

search = Label(left,font=("times new roman",10,"bold"),text="Search By:   ",background="#537180",foreground="#FFFFFF")
search.grid(row=0,column=0)
input_search = ttk.Combobox(left,state="readonly",font=("times new roman",10,"bold"),width=18)
input_search['values']=("Select Option","Refrence No.","Medicine Type","Prescribed By","Manufracturer","Medicine Name","Lot Number")
input_search.grid(row=0,column=1)
input_search.current(0)  #used to display the first element of the given values when reset/first opened

#search parameter 
data = Label(left,font=("times new roman",10,"bold"),text="Enter Parameter:   ",background="#537180",foreground="#FFFFFF")
data.grid(row=1,column=0)
input_data = Entry(left,font=("times new roman",10,"bold"),bd=5,relief=RIDGE,width=20,background="#DFC0CE")
input_data.grid(row=1,column=1)




#frame for search,showall,clear buttons
lframe=Frame(left,bd=5,relief=RIDGE)
lframe.place(x=280,y=40,width=147,height=118)

#search button
schbtn = Button(lframe,text="SEARCH",bd=5,font=("times new roman",11,"bold"),width=13,height=1,padx=3,background="#5F7160",fg="#FFFFFF")#,command=search_function)
schbtn.grid(row=0,column=0)

#SHOW ALL BUTTON
showbtn = Button(lframe,text="SHOW ALL",bd=5,font=("times new roman",11,"bold"),width=13,height=1,padx=3,background="#777180",fg="#FFFFFF")#,command=showall)
showbtn.grid(row=1,column=0)

#clear button
cbtn = Button(lframe,text="CLEAR",bd=5,font=("times new roman",11,"bold"),width=13,height=1,padx=3,background="#D4C2B0")#command=clear_search)
cbtn.grid(row=2,column=0)



right=LabelFrame(root,bd=10,relief=RIDGE,text="Order Box",fg="black",font=("times new roman",15,"bold"),background="#2D4754",foreground="#FFFFFF")
right.place(x=530,y=120,width=680,height=510)

fname = Label(right,font=("times new roman",10,"bold"),text="First Name:     ",background="#2D4754",fg="#FFFFFF")
fname.grid(row=0,column=0,sticky=W,pady=10)
input_fname = Entry(right,font=("times new roman",10,"bold",),bd=5,relief=RIDGE,width=20,background="#DFC0CE")
input_fname.grid(row=0,column=1,pady=10)

lname = Label(right,font=("times new roman",10,"bold"),text="Last Name:       ",background="#2D4754",fg="#FFFFFF")
lname.grid(row=1,column=0,sticky=W,pady=10)
input_lname = Entry(right,font=("times new roman",10,"bold",),bd=5,relief=RIDGE,width=20,background="#DFC0CE")
input_lname.grid(row=1,column=1,pady=10)

fno = Label(right,font=("times new roman",10,"bold"),text="Flat/House No. :       ",background="#2D4754",fg="#FFFFFF")
fno.grid(row=2,column=0,sticky=W,pady=10)
input_fno = Entry(right,font=("times new roman",10,"bold",),bd=5,relief=RIDGE,width=20,background="#DFC0CE")
input_fno.grid(row=2,column=1,pady=10)


appname = Label(right,font=("times new roman",10,"bold"),text="Appartment/House Name :       ",background="#2D4754",fg="#FFFFFF")
appname.grid(row=3,column=0,sticky=W,pady=10)
input_appname = Entry(right,font=("times new roman",10,"bold",),bd=5,relief=RIDGE,width=20,background="#DFC0CE")
input_appname.grid(row=3,column=1,pady=10)


city = Label(right,font=("times new roman",10,"bold"),text="City :       ",background="#2D4754",fg="#FFFFFF")
city.grid(row=4,column=0,sticky=W,pady=10)
input_city = Entry(right,font=("times new roman",10,"bold",),bd=5,relief=RIDGE,width=20,background="#DFC0CE")
input_city.grid(row=4,column=1,pady=10)


state = Label(right,font=("times new roman",10,"bold"),text="State :       ",background="#2D4754",fg="#FFFFFF")
state.grid(row=5,column=0,sticky=W,pady=10)
input_state = Entry(right,font=("times new roman",10,"bold",),bd=5,relief=RIDGE,width=20,background="#DFC0CE")
input_state.grid(row=5,column=1,pady=10)


pincode = Label(right,font=("times new roman",10,"bold"),text="Pincode:       ",background="#2D4754",fg="#FFFFFF")
pincode.grid(row=6,column=0,sticky=W,pady=10)
input_pincode = Entry(right,font=("times new roman",10,"bold",),bd=5,relief=RIDGE,width=20,background="#DFC0CE")
input_pincode.grid(row=6,column=1,pady=10)


medname = Label(right,font=("times new roman",10,"bold"),text="Medicine Name:   ",background="#2D4754",fg="#FFFFFF")
medname.grid(row=7,column=0,sticky=W,pady=10)
input_medname = Entry(right,font=("times new roman",10,"bold"),bd=5,relief=RIDGE,width=20,background="#DFC0CE",textvariable=med_name)
input_medname.grid(row=7,column=1,pady=10)


stock = Label(right,font=("times new roman",10,"bold"),text="Units Needed:   ",background="#2D4754",fg="#FFFFFF")
stock.grid(row=8,column=0,sticky=W)
input_stock = Entry(right,font=("times new roman",10,"bold"),bd=5,relief=RIDGE,width=20,background="#DFC0CE")
input_stock.grid(row=8,column=1)


#frame for search,showall,clear buttons
clrframe=Frame(right,bd=5,relief=RIDGE)
clrframe.place(x=400,y=40,width=145,height=45)


#clear button
cbtn = Button(clrframe,text="CLEAR",bd=5,font=("times new roman",11,"bold"),width=13,height=1,padx=3,background="#D4C2B0",command=clear)
cbtn.grid()


obtnframe=Frame(right,bd=5,relief=RIDGE)
obtnframe.place(x=400,y=150,width=145,height=45)


obtn = Button(obtnframe,text="PLACE ORDER",bd=5,font=("times new roman",11,"bold"),width=13,height=1,padx=3,background="#D4C2B0",command=placeorder)
obtn.grid()






root.mainloop()