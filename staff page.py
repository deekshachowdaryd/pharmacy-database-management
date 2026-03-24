from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image,ImageTk
import mysql.connector as con
from dotenv import load_dotenv
import os

load_dotenv()





#msql connection
mycon=con.connect(host="localhost",
    user="root",
    password=os.getenv("PASSWORD"),
    database=os.getenv("DATABASE"))


#tkinter window
root = Tk()
root.title("PHARMACY MANAGMENT SYSTEM")
root.geometry("1250x700")


# Function to handle row selection
def cursor1(event=''):
    #focus is used to retrive selected data
    selected_item = medtable.focus() #makes the widget active until termination
    if selected_item:

        #gets the values of selected columns 
        row = medtable.item(selected_item)['values'] 

        #set the stringVar with the data effectively filling in the widgets when selected 
        ref_no.set(row[0])
        med_name.set(row[1])
        med_type.set(row[2])
        mfd_dt.set(row[3])
        exp_dt.set(row[4])
        presc_by.set(row[5])
        lot_no.set(row[6])
        stock1.set(row[7])
        price.set(row[8])
        manufacturer.set(row[9])

        medtable.see(selected_item)

# Function to refresh the Treeview widget and adjust the scrollbar
def refresh_table():
    medtable.delete(*medtable.get_children())  #clearing scrollbar
    cursor = mycon.cursor()
    cursor.execute("SELECT * FROM medicines")
    rows = cursor.fetchall()
    for row in rows:
        medtable.insert("", END, values=row)
    medtable.yview_moveto(0)  # Reset scrollbar position to the top of the list

# Scrollbar and Treeview

#creating and placing scrollbar frame
sbframe = Frame(root, bd=5, relief=RIDGE, padx=3, pady=3, background="#141D24")
sbframe.place(x=0, y=405, width=1250, height=232)

# creating and placing scrollbar
sb = ttk.Scrollbar(sbframe, orient=VERTICAL)
sb.pack(side=RIGHT, fill=Y)

#initializing all the cols for the scrollbar
cols = ("refno", "medname", "medtype", "mfddt", "expdt", "presc", "lotno", "stock", "cost", "manuf")

#treeview allows you to display data in a tabular way 
medtable = ttk.Treeview(sbframe, columns=cols, show="headings")

#giving headings to all the cols 
medtable.heading("refno", text="Reference No.")
medtable.heading("medname", text="Medicine Name")
medtable.heading("medtype", text="Medicine Type")
medtable.heading("mfddt", text="Date of Mfd")
medtable.heading("expdt", text="Date of Exp")
medtable.heading("presc", text="Prescribed by")
medtable.heading("lotno", text="Lot No.")
medtable.heading("stock", text="Units available")
medtable.heading("cost", text="Price")
medtable.heading("manuf", text="Manufacturer")

#setting the cols in the scrollbar with a particular width
medtable.column("refno", width=100)
medtable.column("medname", width=100)
medtable.column("medtype", width=100)
medtable.column("mfddt", width=100)
medtable.column("expdt", width=100)
medtable.column("presc", width=100)
medtable.column("lotno", width=100)
medtable.column("stock", width=100)
medtable.column("cost", width=100)
medtable.column("manuf", width=100)

medtable.pack(fill=BOTH, expand=0)

# Fetch values from the table and populate the Treeview widget
refresh_table()

# Configure the scrollbar to control the medtable widget
medtable.configure(yscrollcommand=sb.set)    #used to scroll the scrollbar up and down
sb.configure(command=medtable.yview)   

# Binding the cursor1 function to the Treeview selection event meaning that when treeview function happens in the scrollbar
# which is genrally when you select something from the scrollbar its calls the cursor1 function
medtable.bind("<<TreeviewSelect>>", cursor1)



# Function to add a medicine
def add_medicine():

    #getting the values of the inputs
    ref_no = input_refno.get()
    med_name = input_medname.get()
    med_type = input_medtype.get()
    mfd_dt = input_mfddt.get()
    exp_dt = input_expdt.get()
    presc_by = input_presc.get()
    lot_no = input_lotno.get()
    stock = input_stock.get()
    price = input_cost.get()
    manufacturer = input_manuf.get()
    
   

    #checking if any of the feilds are empty
    if not ref_no or not med_name or not med_type or not mfd_dt or not exp_dt or not presc_by or not lot_no or not stock or not price or not manufacturer:
        messagebox.showerror("ERROR", "Please fill all the fields.")
        return

    #checking if refno in table
    cursor1=mycon.cursor()
    cursor1.execute("select refno from medicines")
    data=cursor1.fetchall()
    l=[]
    for row in data:
        l.append(row)
    lnew = []
    for i in range(len(l)):
        e=l[i][0]
        lnew.append(e)
    if int(ref_no) in lnew:
        messagebox.showinfo("ERROR","2 Elements can't have same Ref.No., Please enter another number")
    else:
        # Inserting data into the database
        cursor = mycon.cursor()
        query = "INSERT INTO medicines (refno, medname, medtype, mfddt, expdt, presc, lotno, stock, cost, manuf) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (ref_no, med_name, med_type, mfd_dt, exp_dt, presc_by, lot_no, stock, price, manufacturer)
        cursor.execute(query, values)
        mycon.commit()
        messagebox.showinfo("Success", "Medicine added successfully.")
        clear()
        refresh_table()

        # Clearing the input fields after adding medicine
        input_refno.delete(0, END)
        input_medname.delete(0, END)
        input_medtype.current(0)
        input_mfddt.delete(0, END)
        input_expdt.delete(0, END)
        input_presc.current(0)
        input_lotno.delete(0, END)
        input_stock.delete(0, END)
        input_cost.delete(0, END)
        input_manuf.delete(0, END)







def upadte_medicine():

    #getting the values of the inputs
    ref_no = input_refno.get()
    med_name = input_medname.get()
    med_type = input_medtype.get()
    mfd_dt = input_mfddt.get()
    exp_dt = input_expdt.get()
    presc_by = input_presc.get()
    lot_no = input_lotno.get()
    stock = input_stock.get()
    price = input_cost.get()
    manufacturer = input_manuf.get()

    # updating data into the database
    cursor = mycon.cursor()
    query = "update medicines set medname=%s,medtype=%s,mfddt=%s,expdt=%s,presc=%s,lotno=%s,stock=%s,cost=%s,manuf=%s where refno=%s"
    values = (med_name, med_type, mfd_dt, exp_dt, presc_by, lot_no, stock, price, manufacturer,ref_no)
    cursor.execute(query, values)
    mycon.commit()
    messagebox.showinfo("Success", "Medicine updated successfully.")
    clear()
    refresh_table()

    # Clearing the input fields after updating
    input_refno.delete(0, END)
    input_medname.delete(0, END)
    input_medtype.current(0)
    input_mfddt.delete(0, END)
    input_expdt.delete(0, END)
    input_presc.current(0)
    input_lotno.delete(0, END)
    input_stock.delete(0, END)
    input_cost.delete(0, END)
    input_manuf.delete(0, END)







def delete_medicine():
    ref_no = input_refno.get()

    # deleting data from database
    cursor = mycon.cursor()
    query = "delete from medicines where refno=%s"
    values = values = (ref_no,)
    cursor1=mycon.cursor()
    cursor1.execute("select refno from medicines")
    data=cursor1.fetchall()
    
    #checking if refno in table
    l=[]
    for row in data:
        l.append(row)
    lnew = []
    for i in range(len(l)):
        e=l[i][0]
        lnew.append(e)

    if int(ref_no) in lnew:
        cursor.execute(query, values)
        messagebox.showinfo("Success", "Medicine deleted successfully.")
    else:
        messagebox.showinfo("ERROR","Refrance Number Not In Table Enter Suitable Referance Number")
    clear()
    refresh_table()
    mycon.commit()
    

    # Clearing the input fields after deleting
    input_refno.delete(0, END)
    input_medname.delete(0, END)
    input_medtype.current(0)
    input_mfddt.delete(0, END)
    input_expdt.delete(0, END)
    input_presc.current(0)
    input_lotno.delete(0, END)
    input_stock.delete(0, END)
    input_cost.delete(0, END)
    input_manuf.delete(0, END)







def clear():

    #clearing all input fields
    input_refno.delete(0, END)
    input_medname.delete(0, END)
    input_medtype.current(0)
    input_mfddt.delete(0, END)
    input_expdt.delete(0, END)
    input_presc.current(0)
    input_lotno.delete(0, END)
    input_stock.delete(0, END)
    input_cost.delete(0, END)
    input_manuf.delete(0, END)






def clear_search():

    #clearing search box inputs
    input_search.current(0)
    input_data.delete(0,END)






def show_search_results():
    medtable.delete(*medtable.get_children())  # Clear previous search results

    for row in search_results:
        medtable.insert("", END, values=row)   #inserting values into scrollbar

    medtable.yview_moveto(0)  # Scroll to the top of the table

def search_function():
    global search_results  # declaring search_results as a global variable 

    search_by = input_search.get()
    e = ""
    if search_by == "Refrence No.":
        e = "refno"
    elif search_by == "Medicine Type":
        e = "medtype"
    elif search_by == "Prescribed By":
        e = "presc"
    elif search_by == "Manufracturer":
        e = "manuf"
    elif search_by == "Medicine Name":
        e = "medname"
    elif search_by == "Lot Number":
        e="lotno"
    

    data_1 = input_data.get()
    if e == "refno":
        data_1 = int(data_1)
    else:
        pass

    cursor = mycon.cursor()
    query = "SELECT * FROM medicines WHERE {} = %s".format(e)
    value = (data_1,)
    cursor.execute(query, value)
    rows = cursor.fetchall()

    search_results = rows  # Update the global variable with search results

    if search_results:
        #checking is there are any values in the search results
        show_search_results()
    else:
        messagebox.showinfo("No Results", "No matching records found.")
        input_search.current(0)
        input_data.delete(0,END)








def showall():
    medtable.delete(*medtable.get_children())
    cursor = mycon.cursor()
    cursor.execute("SELECT * FROM medicines")
    rows = cursor.fetchall()
    for row in rows:
        medtable.insert("", END, values=row)
    



    
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





title = Label(root,text="PHARMACY MANAGEMENT SYSTEM",bd=15,relief=RIDGE,fg="black",font=("times new roman",30,"bold"),padx=2,pady=4,background="#C3CEDA")
title.pack(side=TOP,fill=X)

#colour of upper label
label1=Label(root,background="#D8E2F0")
label1.pack(fill=BOTH)





#border from medical info and search bar
dataframe = Frame(root,bd=15,relief=RIDGE,padx=3,pady=3)
dataframe.place(x=0,y=100,width=1250,height=300)

#background colour of medical info and search bar
bg=Label(root,bd=15,relief=RIDGE,padx=3,pady=3,background="#D8E2F0")
bg.place(x=0,y=100,width=1250,height=300)


#medical info frame
left=LabelFrame(root,bd=10,relief=RIDGE,text="Medical Info",fg="black",font=("times new roman",15,"bold"),background="#2D4754",foreground="#E9E4DF")
left.place(x=20,y=120,width=700,height=250)

#search bar frame
right=LabelFrame(root,bd=10,relief=RIDGE,text="Search Box",fg="black",font=("times new roman",15,"bold"),background="#537180",foreground="#E9E4DF")
right.place(x=730,y=120,width=480,height=250)


#x----------------------------------medical info------------------------------------------x

# entries for adding medicine  
#frist label is created and placed in a frame 
#then entery widget is created and placed
refno = Label(left,font=("times new roman",10,"bold"),text="Refrence No:   ",background="#2D4754",fg="#FFFFFF")
refno.grid(row=0,column=0,sticky=W)
input_refno = Entry(left,font=("times new roman",10,"bold",),bd=5,relief=RIDGE,width=20,background="#DFC0CE",textvariable=ref_no)
input_refno.grid(row=0,column=1)


medname = Label(left,font=("times new roman",10,"bold"),text="Medicine Name:   ",background="#2D4754",fg="#FFFFFF")
medname.grid(row=1,column=0,sticky=W)
input_medname = Entry(left,font=("times new roman",10,"bold"),bd=5,relief=RIDGE,width=20,background="#DFC0CE",textvariable=med_name)
input_medname.grid(row=1,column=1)


#changing the colour of the comboboxes
combostyle = ttk.Style()
combostyle.theme_create('combostyle', parent='alt',  #used to define a new theme
                         settings = {'TCombobox':{'configure':{'selectbackground': '#DFC0CE','fieldbackground': '#DFC0CE','background': '#DFC0CE'}}}) 
                            #dictionaries to define a new theme
combostyle.theme_use('combostyle') #applying theme



medtype = Label(left,font=("times new roman",10,"bold"),text="Medicine Type:   ",background="#2D4754",fg="#FFFFFF")
medtype.grid(row=2,column=0,sticky=W)
input_medtype = ttk.Combobox(left,state="readonly",font=("times new roman",10,"bold"),width=18,textvariable=med_type)
input_medtype['values']=("Select type","syrup","tablet","capsule","drops","injections","topical")
input_medtype.grid(row=2,column=1)
input_medtype.current(0)


mfddt = Label(left,font=("times new roman",10,"bold"),text="Date of Mfd:   ",background="#2D4754",fg="#FFFFFF")
mfddt.grid(row=3,column=0,sticky=W)
input_mfddt = Entry(left,font=("times new roman",10,"bold"),bd=5,relief=RIDGE,width=20,background="#DFC0CE",textvariable=mfd_dt)
input_mfddt.grid(row=3,column=1)


expdt = Label(left,font=("times new roman",10,"bold"),text="Date of Exp:   ",background="#2D4754",fg="#FFFFFF")
expdt.grid(row=4,column=0,sticky=W)
input_expdt = Entry(left,font=("times new roman",10,"bold"),bd=5,relief=RIDGE,width=20,background="#DFC0CE",textvariable=exp_dt)
input_expdt.grid(row=4,column=1)



presc = Label(left,font=("times new roman",10,"bold"),text="Prescribed By:   ",background="#2D4754",fg="#FFFFFF")
presc.grid(row=5,column=0,sticky=W)
input_presc = ttk.Combobox(left,state="readonly",font=("times new roman",10,"bold"),width=18,textvariable=presc_by)
input_presc['values']=("Select Doctor","Dr. Ritu","Dr. Sudhanya","Dr. Aditi","Dr. Rajesh","Dr. Abhishiek")
input_presc.grid(row=5,column=1)
input_presc.current(0)



lotno = Label(left,font=("times new roman",10,"bold"),text="Lot No:   ",background="#2D4754",fg="#FFFFFF")
lotno.grid(row=6,column=0,sticky=W)
input_lotno = Entry(left,font=("times new roman",10,"bold"),bd=5,relief=RIDGE,width=20,background="#DFC0CE",textvariable=lot_no)
input_lotno.grid(row=6,column=1)


stock = Label(left,font=("times new roman",10,"bold"),text="Units Available:   ",background="#2D4754",fg="#FFFFFF")
stock.grid(row=7,column=0,sticky=W)
input_stock = Entry(left,font=("times new roman",10,"bold"),bd=5,relief=RIDGE,width=20,background="#DFC0CE",textvariable=stock1)
input_stock.grid(row=7,column=1)

cost = Label(left,font=("times new roman",10,"bold"),text="       Price:   ",background="#2D4754",fg="#FFFFFF")
cost.grid(row=0,column=4,sticky=W)
input_cost = Entry(left,font=("times new roman",10,"bold"),bd=5,relief=RIDGE,width=20,background="#DFC0CE",textvariable=price)
input_cost.grid(row=0,column=5)


manuf = Label(left,font=("times new roman",10,"bold"),text="       Manufracturer:   ",background="#2D4754",fg="#FFFFFF")
manuf.grid(row=1,column=4)
input_manuf = Entry(left,font=("times new roman",10,"bold"),bd=5,relief=RIDGE,width=20,background="#DFC0CE",textvariable=manufacturer)
input_manuf.grid(row=1,column=5)





#add medicine button
addmedframe = Frame(left,bd=5,relief=RIDGE)
addmedframe.place(x=310,y=100,width=145,height=60)
addbtn = Button(addmedframe,text="ADD MEDICINE",bd=5,font=("times new roman",11,"bold"),width=13,height=2,padx=3,background="#689483",command=add_medicine)
addbtn.grid(row=0,column=0)


#frame for update,delete and clear buttons
lframe=Frame(left,bd=5,relief=RIDGE)
lframe.place(x=500,y=75,width=147,height=118)

#update button
ubtn = Button(lframe,text="UPDATE",bd=5,font=("times new roman",11,"bold"),width=13,height=1,padx=3,background="#83A3A0",command=upadte_medicine)
ubtn.grid(row=0,column=0)

#DELETE BUTTON
Dbtn = Button(lframe,text="DELETE",bd=5,font=("times new roman",11,"bold"),width=13,height=1,padx=3,background="#914955",fg="#FFFFFF",command=delete_medicine)
Dbtn.grid(row=1,column=0)

#clear button
cbtn = Button(lframe,text="CLEAR",bd=5,font=("times new roman",11,"bold"),width=13,height=1,padx=3,background="#D5C1B9",command=clear)
cbtn.grid(row=2,column=0)

#x----------------------------------medical info------------------------------------------x

#x----------------------------------search bar------------------------------------------x

search = Label(right,font=("times new roman",10,"bold"),text="Search By:   ",background="#537180",foreground="#FFFFFF")
search.grid(row=0,column=0)
input_search = ttk.Combobox(right,state="readonly",font=("times new roman",10,"bold"),width=18)
input_search['values']=("Select Option","Refrence No.","Medicine Type","Prescribed By","Manufracturer","Medicine Name","Lot Number")
input_search.grid(row=0,column=1)
input_search.current(0)  #used to display the first element of the given values when reset/first opened

#search parameter 
data = Label(right,font=("times new roman",10,"bold"),text="Enter Parameter:   ",background="#537180",foreground="#FFFFFF")
data.grid(row=1,column=0)
input_data = Entry(right,font=("times new roman",10,"bold"),bd=5,relief=RIDGE,width=20,background="#DFC0CE")
input_data.grid(row=1,column=1)




#frame for search,showall,clear buttons
rframe=Frame(right,bd=5,relief=RIDGE)
rframe.place(x=280,y=40,width=147,height=118)

#search button
schbtn = Button(rframe,text="SEARCH",bd=5,font=("times new roman",11,"bold"),width=13,height=1,padx=3,background="#5F7160",fg="#FFFFFF",command=search_function)
schbtn.grid(row=0,column=0)

#SHOW ALL BUTTON
showbtn = Button(rframe,text="SHOW ALL",bd=5,font=("times new roman",11,"bold"),width=13,height=1,padx=3,background="#777180",fg="#FFFFFF",command=showall)
showbtn.grid(row=1,column=0)

#clear button
cbtn = Button(rframe,text="CLEAR",bd=5,font=("times new roman",11,"bold"),width=13,height=1,padx=3,background="#D4C2B0",command=clear_search)
cbtn.grid(row=2,column=0)

#x----------------------------------search bar------------------------------------------x



#images 
# Load the image
logo_image = Image.open("C:\\Users\\Deeksha\\OneDrive\\Desktop\\class 12 projects\\cs project\\logo.png")
# Resize the image
logo_image = logo_image.resize((200, 150), Image.LANCZOS)
# Create an ImageTk object
logo = ImageTk.PhotoImage(logo_image)

#defining the logo as a button to place it easily
logo_button = Button(root, image=logo, bd=0, highlightthickness=0)
logo_button.place(x=780, y=200)




root.mainloop()
#for the window to run