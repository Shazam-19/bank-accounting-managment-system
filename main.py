"""
This code is written by :

1. 89368  -  AbdEl-Rahman Sayed Shehata     
2. 90844  -  Abd-Ullah Ashraf Mohammed 

"""

## Packages required

import os                  # Provides functions for interacting with the operating system.
from datetime import date  # Supplies classes to work with date and time.
import tkinter as tk       # Provides standard GUI library for Python.
from tkinter import *
import re                  # Provides compile for check_name
import mysql.connector
import pandas as pd
from datetime import date  # Provides today's date to calculate the age of a customer
pd.set_option('display.colheader_justify', 'center')

# Backend python functions code starts

## Validate client accout number in database

def is_valid(customer_account_number):
    """Return True if the account exists in data base, otherwise return False."""
    customer_account_number = str(customer_account_number)
    if customer_account_number == '' or customer_account_number.isdigit() != True:
        return False
    
    # Make sure that account number is int just like in DB
    customer_account_number = int(customer_account_number) 
    
    # Connect to database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="xx8489",
        database="bank"
    )
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT accNo FROM customers WHERE accNo = %s", [customer_account_number])
    myresult = mycursor.fetchone()
    if myresult == None:
        return False
    
    if customer_account_number == myresult[0]:
        return True
    else:
        return False

## Validate admin id in database

def is_valid_admin(admin_id):
    """Return True if the account id exists in data base, otherwise return False."""
    admin_id = str(admin_id)
    
    if admin_id == '' or admin_id == None or len(admin_id) > 5:
        return False
    
    admin_id = str(admin_id)
    
    # Connect to database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="xx8489",
        database="bank"
    )
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT adminID FROM admins WHERE adminID = %s", [admin_id])
    myresult = mycursor.fetchone()
    if myresult == None:
        return False
    
    if admin_id == myresult[0]:
        return True
    else:
        return False

## Functions to handle database and GUI

def check_name(name):
    name_str = str(name)
    """Return True if name is a full string, otherwiser returns false."""
    special_characters = re.compile('[@_!#$%^&*()<>?/\|}{~:]') 
    
    # Check if the string is empty.
    if name_str == "":
        return False
    # Check that the name doesn't contain a number or special character.
    elif (special_characters.search(name_str) == None) and (True not in [char.isdigit() for char in name_str]):
        return True
    else:
        return False # The the string contain a digit or a special character.
    
def check_accType(accType):
    """Return True if account type is Savings or Current, otherwise return False"""
    accType = accType.upper() # Convert accType from small to upper-case
    if accType == 'S' or accType == 'C':
        return True
    
    return False
    

def check_leap(year):
    """Return True if the year is a leap year, otherwise return False."""
    return ((int(year) % 4 == 0) and (int(year) % 100 != 0)) or (int(year) % 400 == 0)


def check_date(date):
    """Return True if the year, month, and day are correct with eachother, otherwise return False."""
    # Number of days in each month in regular year
    days_in_months              = ["31", "28", "31", "30", "31", "30", "31", "31", "30", "31", "30", "31"]
    
    # Number of days in each month in a leap year
    days_in_months_in_leap_year = ["31", "29", "31", "30", "31", "30", "31", "31", "30", "31", "30", "31"]
    
    # If the user didn't type a date, return false
    if date == "":
        return False
    
    # Split the date to day, month, and year into a 3-element list at "/".
    date_elements = date.split("-")
    year  = int(date_elements[0])
    month = int(date_elements[1])
    day   = int(date_elements[2])
    
    # If year and/or month are out of range, return False.
    if (year > 2021 or year < 0) or (month > 12 or month < 1):
        return False
    else:
        # Determine the number of days in the given month by user.
        if check_leap(year):
            numOfDays = days_in_months_in_leap_year[month - 1]
        else:
            numOfDays = days_in_months[month - 1]
        
        # If the day entered by user is within the range of specified month,
        # return Ture, otherwise return Flase.
        return int(numOfDays) >= day >= 1

def check_age(birthdate):
    date_elements = birthdate.split("-")
    yearBorn  = int(date_elements[0])
    monthBorn = int(date_elements[1])
    dayBorn   = int(date_elements[2])
    
    today = date.today()
    
    global age
    age = today.year - yearBorn - ((today.month, today.day) < (monthBorn, dayBorn))
    
    return (age >= 21.0)

def is_valid_mobile(mobile_number):
    """Return True if the number is valid, otherwise return False."""
    if len(mobile_number) == 11 and mobile_number.isnumeric() and mobile_number[0] == "0" and mobile_number[1] == "1":
        return True
    
    return False
    

def check_gender(gender):
    """Return True if gender is Male or Female, otherwise return False."""
    gender = gender.upper() # Convert accType from small to upper-case
    if gender == 'M' or gender == 'F':
        return True
    
    return False
    
def check_nationality(country):
    """Return True if the country name is valid, otherwise return False."""
    if country == "":
        return False
    
    country = country.lower()      # Convert all string to lower-case
    country = country.capitalize() # Make only first letter upper-case
    
    # Connect to database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="xx8489",
        database="bank"
    )
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT name FROM countries WHERE name = %s", [country])
    myresult = mycursor.fetchone()
    
    if myresult[0] == country:
        return True
    
    return False
    
def check_national_ID(national_ID):
    """Return True if national ID is valid, otherwise return False."""
    if national_ID == None:
        return False
    elif len(national_ID) == 14 and national_ID.isnumeric():
        return True
    
    return False

def check_pin(pin):
    """Return True is pin valid, otherwise return False"""
    pin_str = str(pin)
    if pin == None:
        return False
    # Make sure that pin is a 4-digit number.
    elif len(pin_str) == 4 and pin_str.isdigit():
        return True
    
    return False

def check_balance(balance):
    """Return true if the balance is a float or int, otherwise return False."""
    balance_float = float(balance) # Convert the str balance to float.
    if balance_float == None:
        return False
    # Check if the balance is int or float only.
    elif isinstance(balance_float, (int, float)): 
        return True
    
    return False

def check_password(password):
    
    password = str(password)
    
    if password == None or password == '':
        return False
    elif len(password) > 0 and len(password) <= 12:
        return True
    else:
        return False

## Add data to database

def append_data(data):
    """Add data to database(adnin's or customer's)."""
    
    # Connect to database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="xx8489",
        database="bank"
    )
    mycursor = mydb.cursor()
    
    # If the data is 2 field(adminID, password),
    # then it's an admin account.
    try:
        if len(data) == 2:
            sql_query = "INSERT INTO admins (adminID, password) VALUES (%s, %s)"
            mycursor.execute(sql_query, data)
            mydb.commit()
            return True
    except:
        return False
    
    # IF the customer data is 10 fields(without 'account number', 'creation_date'), then it's a customer's account
    # Print the customer account number after
    try:
        if len(data) == 10:
            sql_query = "INSERT INTO customers (name, accType, birthDate, age, phone, gender, country, nationalID \
            , pin, balance) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            mycursor.execute(sql_query, data)
            mydb.commit()
            return True
    except:
        return False
    else:
        # The data was entered incorrectly
        return False

## Display account summary or current balance

def display_account_summary(identity, choice):
    """Reurn a string contains the account's full data if the account number is valid and choice is 1,
    or return the current balance of the account if choice is 2. Otherwise return False."""
    
    identity = str(identity)
    
    if identity == '' or identity.isdigit() != True:
        return False
    
    identity = int(identity)
    
    # Connect to database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="xx8489",
        database="bank"
    )
    
    # Get client summary from DB
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM customers WHERE accNo = %s", [identity])
    myresult = mycursor.fetchall()
    output_message = ""
    if myresult == []:
        return False
    
    else:
        (accNo, name, accType, birthDate, age, phone, gender, nationality, nationalID, pin, balance, cd) = myresult[0]
        if  choice == 1:
            output_message += "Account number: "           + str(accNo)       + "\n"
            output_message += "Name of account holder: "   + str(name)        + "\n"
            output_message += "Current balance: "          + str(balance)     + "\n"
            output_message += "Account type: "             + str(accType)     + "\n"
            output_message += "Date of Birth: "            + str(birthDate)   + "\n"
            output_message += "Age:           "            + str(age)   + "\n"
            output_message += "Mobile number: "            + str(phone)       + "\n"
            output_message += "Gender: "                   + str(gender)      + "\n"
            output_message += "Nationality: "              + str(nationality) + "\n"
            output_message += "National ID: "              + str(nationalID)  + "\n"
            output_message += "Date of account creation: " + str(cd)          + "\n"
            return output_message
        
        elif choice == 2:
            output_message += "Current balance : " + str(balance) + " EGP\n"
            return output_message
        else:
            return False

## Delete a client's account

def delete_customer_account(identity):
    """Return True if clint account was deleted, otherwise return False."""
    
    if identity == '' or identity.isdigit() != True:
        return False
    
    identity = int(identity)
    
    # Connect to database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="xx8489",
        database="bank"
    )

    if is_valid(identity):
        # Delete a record
        mycursor = mydb.cursor()
        mycursor.execute("DELETE FROM customers WHERE accNo = %s", [identity])
        mydb.commit()
        return True
    else:
        return False

## Store transactions logs into DB

def store_logs(customer_account_number, transaction_type, amount):
    """Store the transaction(deposit/withdraw) the client made."""
    
    if customer_account_number == '' or customer_account_number.isdigit() != True or amount == '' or amount.isdigit() != True:
        return False
    
    transaction_type = transaction_type.upper()
    amount = float(amount)
    
    # Connect to database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="xx8489",
        database="bank"
    )
    mycursor = mydb.cursor()
    data = [customer_account_number, transaction_type, amount]
    sql_query = "INSERT INTO transactions (accNo, trans_type, amount) VALUES (%s, %s, %s)"
    mycursor.execute(sql_query, data)
    mydb.commit()
    return True

## Show customer logs

def show_customer_logs(customer_account_number):
    """Return a string contains all the customer's logs"""
    
    if customer_account_number == '' or customer_account_number.isdigit() != True:
        return False
    
    customer_account_number = int(customer_account_number)
    
    # Connect to database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="xx8489",
        database="bank"
    )
    mycursor = mydb.cursor()
    
    # Get client logs summary from DB
    df = pd.read_sql('SELECT * FROM transactions WHERE accNo = %s LIMIT 5', con=mydb, params=[customer_account_number])
    df.rename(columns = {'transacion_id':'ID', 'trans_type': 'Type', 'trans_date':'Date', 'amount':'Amount'},
              inplace = True)
    
    if df.empty == True:
        return "This account has no logs yet."
    else:
        del df['accNo']
        df = df.to_string(index=False)
        return df

## Change PIN of a cutomer's account

def change_PIN(identity, old_PIN, new_PIN):
    """Return true if the old pin is correct and pin is updated successfully,
    otherwise return False."""
    
    identity = str(identity)
    
    if identity == '' or identity.isdigit() != True or old_PIN == '' or new_PIN == '':
        return False
    
    identity = int(identity)
    old_PIN  = str(old_PIN)
    new_PIN  = str(new_PIN)
    
    # Connect to database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="xx8489",
        database="bank"
    )
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT pin FROM customers WHERE accNo = %s", [identity])
    myresult = mycursor.fetchone()
    
    if myresult == None:
        return False
    
    if myresult[0] == old_PIN:
        mycursor.execute("UPDATE customers SET pin = %s WHERE accNo = %s", [new_PIN, identity])
        mydb.commit()
        return True
    else:
        return False

## Make a transaction in a customer account

def transaction(identity, amount, choice):  # choice 1 for deposit; choice 2 for withdraw
    
    identity = str(identity)
    amount = str(amount)
    
    if identity == '' or identity.isdigit() != True or amount == '' or amount.isdigit() != True:
        return False
    
    identity     = int(identity)
    amount_float = float(amount)
    
    # Connect to database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="xx8489",
        database="bank"
    )

    # Get existing pin from DB
    mycursor = mydb.cursor()
    mycursor.execute("SELECT accNo FROM customers WHERE accNo = %s", [identity])
    myresult = mycursor.fetchone()
    if myresult == []:
        return None
    else:
        if choice == 1:
            mycursor.execute("UPDATE customers SET balance = balance + %s WHERE accNo = %s", [amount_float, identity])
            mydb.commit()
            
            # Get new balance after deposite to return it
            mycursor.execute("SELECT balance FROM customers WHERE accNo = %s", [identity])
            balance = mycursor.fetchone()
            return balance[0]
        
        elif choice == 2:
            # Get balance before withdraw to check first if the amount exceeds it or not
            mycursor.execute("SELECT balance FROM customers WHERE accNo = %s", [identity])
            balance = mycursor.fetchone()
            
            if balance[0] - float(amount) >= 0:
                mycursor.execute("UPDATE customers SET balance = balance - %s WHERE accNo = %s", [amount_float, identity])
                mydb.commit()
            
                # Get new balance after withdraw to return it
                mycursor.execute("SELECT balance FROM customers WHERE accNo = %s", [identity])
                balance = mycursor.fetchone()
                return balance[0]
            else:
                return -1
        else:
            return None

## Check the ID & Password validity of Admin and Customer

def check_credentials(identity, password, choice):
    
    if identity == '' or password == '':
        return False
    
    password = str(password)
    
    # Connect to database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="xx8489",
        database="bank"
    )
    
    mycursor = mydb.cursor()
    
    if choice == 1:
        identity = str(identity)
        mycursor.execute("SELECT adminID, password FROM admins WHERE adminID = %s AND password = %s", [identity, password])
        admin_credentials = mycursor.fetchall()
        # If admin account number or/and password wasn't found
        if admin_credentials == []:
            return False
        else:
            try:
                (admin_id, admin_pass) = admin_credentials[0]
                if identity == admin_id and password == admin_pass:
                    return True
            except:
                return False
            
    elif choice == 2:
        identity = int(identity)
        mycursor.execute("SELECT accNo, pin FROM customers WHERE accNo = %s AND pin = %s", [identity, password])
        customer_credentials = mycursor.fetchall()
        # If customer account number or/and password wasn't found
        if customer_credentials == []:
            return False
        else:
            try:
                (accNo, pin) = customer_credentials[0]
                if identity == accNo and password == pin:
                    return True
            except:
                return False
    else: # The choice was a wrong number
        return False

## Backend python functions code ends.
# Tkinter GUI code starts
## Welcome Screen window

class welcomeScreen:
    def __init__(self, window=None):
        self.master = window
        window.geometry("600x450+383+106")
        window.minsize(120, 1)
        window.maxsize(1370, 749)
        window.resizable(0, 0)
        window.title("Welcome to MTI BANK")
        p1 = PhotoImage(file='./images/bank1.png')
        window.iconphoto(True, p1)
        window.configure(background="#023047")
        window.configure(cursor="arrow")

        self.Canvas1 = tk.Canvas(window, background="#ffff00", borderwidth="0", insertbackground="black",
                                 relief="ridge",
                                 selectbackground="blue", selectforeground="white")
        self.Canvas1.place(relx=0.190, rely=0.228, relheight=0.496, relwidth=0.622)
        
        # Employee button & label
        self.Button1 = tk.Button(self.Canvas1, command=self.selectEmployee, activebackground="#ececec",
                                 activeforeground="#000000", background="#023047", disabledforeground="#a3a3a3",
                                 foreground="#fbfbfb", borderwidth="0", highlightbackground="#d9d9d9",
                                 highlightcolor="black", pady="0",
                                 text='''ADMIN''')
        self.Button1.configure(font="-family {Segoe UI} -size 10 -weight bold")
        self.Button1.place(relx=0.161, rely=0.583, height=24, width=87)
        
        # Customer button & label
        self.Button2 = tk.Button(self.Canvas1, command=self.selectCustomer, activebackground="#ececec",
                                 activeforeground="#000000", background="#023047", disabledforeground="#a3a3a3",
                                 foreground="#f9f9f9", borderwidth="0", highlightbackground="#d9d9d9",
                                 highlightcolor="black", pady="0",
                                 text='''CUSTOMER''')
        self.Button2.configure(font="-family {Segoe UI} -size 10 -weight bold")
        self.Button2.place(relx=0.617, rely=0.583, height=24, width=87)
        
        # Message label
        self.Label1 = tk.Label(self.Canvas1, background="#ffff00", disabledforeground="#a3a3a3",
                               font="-family {Segoe UI} -size 13 -weight bold", foreground="#000000",
                               text='''Select your role''')
        self.Label1.place(relx=0.241, rely=0.224, height=31, width=194)

    def selectEmployee(self):
        self.master.withdraw()
        adminLogin(Toplevel(self.master))    # Call adminLogin class

    def selectCustomer(self):
        self.master.withdraw()
        CustomerLogin(Toplevel(self.master)) # Call customerLogin class

class Error:
    def __init__(self, window=None):
        global master
        master = window
        window.geometry("411x117+485+248")
        window.minsize(120, 1)
        window.maxsize(1370, 749)
        window.resizable(0, 0)
        window.title("Error")
        window.configure(background="#f2f3f4")

        global Label2
        
        # OK button
        self.Button1 = tk.Button(window, background="#d3d8dc", borderwidth="1", disabledforeground="#a3a3a3",
                                 font="-family {Segoe UI} -size 9", foreground="#000000", highlightbackground="#d9d9d9",
                                 highlightcolor="black", pady="0", text='''OK''', command=self.goback)
        self.Button1.place(relx=0.779, rely=0.598, height=24, width=67)

        global _img0
        _img0 = tk.PhotoImage(file="./images/error_image.png")
        self.Label1 = tk.Label(window, background="#f2f3f4", disabledforeground="#a3a3a3", foreground="#000000",
                               image=_img0, text='''Label''')
        self.Label1.place(relx=0.024, rely=0.0, height=81, width=84)

    def setMessage(self, message_shown):
        Label2 = tk.Label(master, background="#f2f3f4", disabledforeground="#a3a3a3",
                          font="-family {Segoe UI} -size 16", foreground="#000000", highlightcolor="#646464646464",
                          text=message_shown)
        Label2.place(relx=0.210, rely=0.171, height=50, width=300)

    def goback(self):
        master.withdraw()

## Admin login window

class adminLogin:
    def __init__(self, window=None):
        self.master = window
        window.geometry("743x494+338+92")
        window.minsize(120, 1)
        window.maxsize(1370, 749)
        window.resizable(0, 0)
        window.title("Admin")
        window.configure(background="#ffff00")

        global Canvas1
        Canvas1 = tk.Canvas(window, background="#ffffff", insertbackground="black", relief="ridge",
                            selectbackground="blue", selectforeground="white")
        Canvas1.place(relx=0.108, rely=0.142, relheight=0.715, relwidth=0.798)
        
        # 'Admin Login' label
        self.Label1 = tk.Label(Canvas1, background="#ffffff", disabledforeground="#a3a3a3",
                               font="-family {Segoe UI} -size 14 -weight bold", foreground="#00254a",
                               text="Admin Login")
        self.Label1.place(relx=0.135, rely=0.142, height=41, width=154)

        global Label2
        Label2 = tk.Label(Canvas1, background="#ffffff", disabledforeground="#a3a3a3", foreground="#000000")
        Label2.place(relx=0.067, rely=0.283, height=181, width=233)
        
        global _img0
        _img0 = tk.PhotoImage(file="./images/adminLogin1.png")
        Label2.configure(image=_img0)

        self.Entry1 = tk.Entry(Canvas1, background="#e2e2e2", borderwidth="2", disabledforeground="#a3a3a3",
                               font="TkFixedFont", foreground="#000000", highlightbackground="#b6b6b6",
                               highlightcolor="#004080", insertbackground="black")
        self.Entry1.place(relx=0.607, rely=0.453, height=20, relwidth=0.26)

        self.Entry1_1 = tk.Entry(Canvas1, show='*', background="#e2e2e2", borderwidth="2",
                                 disabledforeground="#a3a3a3", font="TkFixedFont", foreground="#000000",
                                 highlightbackground="#d9d9d9", highlightcolor="#004080", insertbackground="black",
                                 selectbackground="blue", selectforeground="white")
        self.Entry1_1.place(relx=0.607, rely=0.623, height=20, relwidth=0.26)

        self.Label3 = tk.Label(Canvas1, background="#ffffff", disabledforeground="#a3a3a3", foreground="#000000")
        self.Label3.place(relx=0.556, rely=0.453, height=21, width=34)
        
        global _img1
        _img1 = tk.PhotoImage(file="./images/user1.png")
        self.Label3.configure(image=_img1)

        self.Label4 = tk.Label(Canvas1, background="#ffffff", disabledforeground="#a3a3a3", foreground="#000000")
        self.Label4.place(relx=0.556, rely=0.623, height=21, width=34)
        
        global _img2
        _img2 = tk.PhotoImage(file="./images/lock1.png")
        self.Label4.configure(image=_img2)

        self.Label5 = tk.Label(Canvas1, background="#ffffff", disabledforeground="#a3a3a3", foreground="#000000")
        self.Label5.place(relx=0.670, rely=0.142, height=71, width=74)
        
        global _img3
        _img3 = tk.PhotoImage(file="./images/bank1.png")
        self.Label5.configure(image=_img3)
        
        # Login Button label
        self.Button = tk.Button(Canvas1, text="Login", borderwidth="0", width=10, background="#ffff00",
                                foreground="#00254a",
                                font="-family {Segoe UI} -size 10 -weight bold",
                                command=lambda: self.login(self.Entry1.get(), self.Entry1_1.get()))
        self.Button.place(relx=0.765, rely=0.755)
        
        # Back Button label
        self.Button_back = tk.Button(Canvas1, text="Back", borderwidth="0", width=10, background="#ffff00",
                                     foreground="#00254a",
                                     font="-family {Segoe UI} -size 10 -weight bold",
                                     command=self.back)
        self.Button_back.place(relx=0.545, rely=0.755)
        
        
        global admin_img
        admin_img = tk.PhotoImage(file="./images/adminLogin1.png")

    def back(self):
        """Go back to welcomescreen window if the user click's 'back'"""
        self.master.withdraw()
        welcomeScreen(Toplevel(self.master))

    @staticmethod
    def setImg():
        Label2 = tk.Label(Canvas1, background="#ffffff", disabledforeground="#a3a3a3", foreground="#000000")
        Label2.place(relx=0.067, rely=0.283, height=181, width=233)
        Label2.configure(image=admin_img)

    def login(self, admin_id, admin_password):
        global admin_idNO
        admin_idNO = admin_id
        if check_credentials(admin_id, admin_password, 1):
            self.master.withdraw()
            adminMenu(Toplevel(self.master))
        else:
            Error(Toplevel(self.master))
            Error.setMessage(self, message_shown="Invalid Credentials!")
            self.setImg()

## Customer login window

class CustomerLogin:
    def __init__(self, window=None):
        self.master = window
        window.geometry("743x494+338+92")
        window.minsize(120, 1)
        window.maxsize(1370, 749)
        window.resizable(0, 0)
        window.title("Customer")
        window.configure(background="#00254a")

        global Canvas1
        Canvas1 = tk.Canvas(window, background="#ffffff", insertbackground="black", relief="ridge",
                            selectbackground="blue", selectforeground="white")
        Canvas1.place(relx=0.108, rely=0.142, relheight=0.715, relwidth=0.798)

        Label1 = tk.Label(Canvas1, background="#ffffff", disabledforeground="#a3a3a3",
                          font="-family {Segoe UI} -size 14 -weight bold", foreground="#00254a",
                          text="Customer Login")
        Label1.place(relx=0.135, rely=0.142, height=41, width=154)

        global Label2
        Label2 = tk.Label(Canvas1, background="#ffffff", disabledforeground="#a3a3a3", foreground="#000000")
        Label2.place(relx=0.067, rely=0.283, height=181, width=233)
        global _img0
        _img0 = tk.PhotoImage(file="./images/customer.png")
        Label2.configure(image=_img0)

        self.Entry1 = tk.Entry(Canvas1, background="#e2e2e2", borderwidth="2", disabledforeground="#a3a3a3",
                               font="TkFixedFont", foreground="#000000", highlightbackground="#b6b6b6",
                               highlightcolor="#004080", insertbackground="black")
        self.Entry1.place(relx=0.607, rely=0.453, height=20, relwidth=0.26)

        self.Entry1_1 = tk.Entry(Canvas1, show='*', background="#e2e2e2", borderwidth="2",
                                 disabledforeground="#a3a3a3", font="TkFixedFont", foreground="#000000",
                                 highlightbackground="#d9d9d9", highlightcolor="#004080", insertbackground="black",
                                 selectbackground="blue", selectforeground="white")
        self.Entry1_1.place(relx=0.607, rely=0.623, height=20, relwidth=0.26)

        self.Label3 = tk.Label(Canvas1, background="#ffffff", disabledforeground="#a3a3a3", foreground="#000000")
        self.Label3.place(relx=0.556, rely=0.453, height=21, width=34)

        global _img1
        _img1 = tk.PhotoImage(file="./images/user1.png")
        self.Label3.configure(image=_img1)

        self.Label4 = tk.Label(Canvas1)
        self.Label4.place(relx=0.556, rely=0.623, height=21, width=34)
        global _img2
        _img2 = tk.PhotoImage(file="./images/lock1.png")
        self.Label4.configure(image=_img2, background="#ffffff")

        self.Label5 = tk.Label(Canvas1, background="#ffffff", disabledforeground="#a3a3a3", foreground="#000000")
        self.Label5.place(relx=0.670, rely=0.142, height=71, width=74)
        global _img3
        _img3 = tk.PhotoImage(file="./images/bank1.png")
        self.Label5.configure(image=_img3)

        self.Button = tk.Button(Canvas1, text="Login", borderwidth="0", width=10, background="#00254a",
                                foreground="#ffffff",
                                font="-family {Segoe UI} -size 10 -weight bold",
                                command=lambda: self.login(self.Entry1.get(), self.Entry1_1.get()))
        self.Button.place(relx=0.765, rely=0.755)

        self.Button_back = tk.Button(Canvas1, text="Back", borderwidth="0", width=10, background="#00254a",
                                     foreground="#ffffff",
                                     font="-family {Segoe UI} -size 10 -weight bold",
                                     command=self.back)
        self.Button_back.place(relx=0.545, rely=0.755)

        global customer_img
        customer_img = tk.PhotoImage(file="./images/customer.png")

    def back(self):
        self.master.withdraw()
        welcomeScreen(Toplevel(self.master))

    @staticmethod
    def setImg():
        settingIMG = tk.Label(Canvas1, background="#ffffff", disabledforeground="#a3a3a3", foreground="#000000")
        settingIMG.place(relx=0.067, rely=0.283, height=181, width=233)
        settingIMG.configure(image=customer_img)

    def login(self, customer_account_number, customer_PIN):
        if check_credentials(customer_account_number, customer_PIN, 2):
            
            global customer_accNO
            customer_accNO = str(customer_account_number)
            
            self.master.withdraw()
            customerMenu(Toplevel(self.master))
        else:
            Error(Toplevel(self.master))
            Error.setMessage(self, message_shown="Invalid Credentials!")
            self.setImg()

## Admin menu login

class adminMenu:
    def __init__(self, window=None):
        self.master = window
        window.geometry("743x494+329+153")
        window.minsize(120, 1)
        window.maxsize(1370, 749)
        window.resizable(0, 0)
        window.title("Admin Section")
        window.configure(background="#ffff00")

        # Main Frame
        self.Labelframe1 = tk.LabelFrame(window, relief='groove', font="-family {Segoe UI} -size 13 -weight bold",
                                         foreground="#001c37", text="Select your option", background="#fffffe")
        self.Labelframe1.place(relx=0.081, rely=0.081, relheight=0.415, relwidth=0.848)
        
        # Close bank account button#1
        self.Button1 = tk.Button(self.Labelframe1, activebackground="#ececec", activeforeground="#000000",
                                 background="#00254a", borderwidth="0", disabledforeground="#a3a3a3",
                                 font="-family {Segoe UI} -size 11", foreground="#fffffe",
                                 highlightbackground="#d9d9d9", highlightcolor="black", pady="0",
                                 text="Close bank account", command=self.closeAccount)
        self.Button1.place(relx=0.667, rely=0.195, height=34, width=181, bordermode='ignore')

        # Create bank account button#2
        self.Button2 = tk.Button(self.Labelframe1, activebackground="#ececec", activeforeground="#000000",
                                 background="#00254a", borderwidth="0", disabledforeground="#a3a3a3",
                                 font="-family {Segoe UI} -size 11", foreground="#fffffe",
                                 highlightbackground="#d9d9d9", highlightcolor="black", pady="0",
                                 text="Create bank account", command=self.createCustaccount)
        self.Button2.place(relx=0.04, rely=0.195, height=34, width=181, bordermode='ignore')
        
        # Show account logs button#3
        self.Button3 = tk.Button(self.Labelframe1, activebackground="#ececec", activeforeground="#000000",
                                 background="#00254a", borderwidth="0", disabledforeground="#a3a3a3",
                                 font="-family {Segoe UI} -size 11", foreground="#fffffe",
                                 highlightbackground="#d9d9d9", highlightcolor="black", pady="0",
                                 text="Show account logs", command=self.clientLogs)
        self.Button3.place(relx=0.667, rely=0.439, height=34, width=181, bordermode='ignore')
        
        # Create admin account button#4
        self.Button4 = tk.Button(self.Labelframe1, activebackground="#ececec", activeforeground="#000000",
                                 background="#00254a", borderwidth="0", disabledforeground="#a3a3a3",
                                 font="-family {Segoe UI} -size 11", foreground="#fffffe",
                                 highlightbackground="#d9d9d9", highlightcolor="black", pady="0",
                                 text="Create admin account", command=self.createAdmin)
        self.Button4.place(relx=0.04, rely=0.439, height=34, width=181, bordermode='ignore')
        
        # Check account summary button#6
        self.Button6 = tk.Button(self.Labelframe1, activebackground="#ececec", activeforeground="#000000",
                                 background="#00254a", foreground="#fffffe", borderwidth="0",
                                 disabledforeground="#a3a3a3", font="-family {Segoe UI} -size 11",
                                 highlightbackground="#d9d9d9", highlightcolor="black", pady="0",
                                 text="Check account summary", command=self.showAccountSummary)
        self.Button6.place(relx=0.04, rely=0.683, height=34, width=181, bordermode='ignore')

        # Logout bank account button#5
        self.Button5 = tk.Button(self.Labelframe1, activebackground="#ececec", activeforeground="#000000",
                                 background="#00254a", borderwidth="0", disabledforeground="#a3a3a3",
                                 font="-family {Segoe UI} -size 11", foreground="#fffffe",
                                 highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text="Logout",
                                 command=self.exit)
        self.Button5.place(relx=0.667, rely=0.683, height=34, width=181, bordermode='ignore')
        
        
        global Frame1
        Frame1 = tk.Frame(window, relief='groove', borderwidth="2", background="#fffffe")
        Frame1.place(relx=0.081, rely=0.547, relheight=0.415, relwidth=0.848)

    def closeAccount(self):
        CloseAccountByAdmin(Toplevel(self.master))   # Call class CloseAccountByAdmin

    def createCustaccount(self):
        createCustomerAccount(Toplevel(self.master)) # Call class createCustaccount 
        
    def clientLogs(self):
        clientLogs(Toplevel(self.master))           # Call class clientLogs
        
    def createAdmin(self):                           # Call class createAdmin
        createAdmin(Toplevel(self.master))

    def exit(self):                                  # Call class exit
        self.master.withdraw()
        adminLogin(Toplevel(self.master))

    def showAccountSummary(self):                    # Call class showAccountSummary
        checkAccountSummary(Toplevel(self.master))

    def printAccountSummary(identity):
        # clearing the frame
        for widget in Frame1.winfo_children():
            widget.destroy()
            
        # getting output_message and displaying it in the frame
        output = display_account_summary(identity, 1)
        output_message = Label(Frame1, text=output, background="#fffffe")
        output_message.pack(pady=20)

    def printMessage_outside(output):
        # Clearing the frame
        for widget in Frame1.winfo_children():
            widget.destroy()
            
        # Getting output_message and displaying it in the frame
        output_message = Label(Frame1, text=output, background="#fffffe")
        output_message.pack(pady=20)
        

## Close customer account by admin   

class CloseAccountByAdmin:
    def __init__(self, window=None):
        self.master = window
        window.geometry("411x117+498+261")
        window.minsize(120, 1)
        window.maxsize(1370, 749)
        window.resizable(0, 0)
        window.title("Close customer account")
        window.configure(background="#f2f3f4")
        
        # Enter account number label
        self.Label1 = tk.Label(window, background="#f2f3f4", disabledforeground="#a3a3a3",
                               text='''Enter account number:''')
        self.Label1.place(relx=0.232, rely=0.220, height=20, width=120)
        
        # Entery text box
        self.Entry1 = tk.Entry(window, background="#cae4ff", disabledforeground="#a3a3a3", font="TkFixedFont",
                               foreground="#000000", insertbackground="black")
        self.Entry1.place(relx=0.536, rely=0.220, height=20, relwidth=0.232)
        
        # Back button
        self.Button1 = tk.Button(window, activebackground="#ececec", activeforeground="#000000", borderwidth="0",
                                 background="#004080", disabledforeground="#a3a3a3", foreground="#ffffff",
                                 highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text="Back",
                                 command=self.back)
        self.Button1.place(relx=0.230, rely=0.598, height=24, width=67)

        # Proceed button
        self.Button2 = tk.Button(window, activebackground="#ececec", activeforeground="#000000", background="#004080",
                                 borderwidth="0", disabledforeground="#a3a3a3", foreground="#ffffff",
                                 highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text="Proceed",
                                 command=lambda: self.submit(self.Entry1.get()))
        self.Button2.place(relx=0.598, rely=0.598, height=24, width=67)

    def back(self):
        self.master.withdraw()

    def submit(self, identity):
        if is_valid(identity):
            delete_customer_account(identity)
            adminMenu.printMessage_outside("Account deleted successfully.")
        else:
            Error(Toplevel(self.master))
            Error.setMessage(self, message_shown="Invalid credentials!")
            return
        self.master.withdraw()

## Create a cutomer account by admin

class createCustomerAccount:
    def __init__(self, window=None):
        self.master = window
        window.geometry("411x411")
        window.minsize(120, 1)
        window.maxsize(1370, 749)
        window.resizable(0, 0)
        window.title("Create account")
        window.configure(background="#f2f3f4")
        window.configure(highlightbackground="#d9d9d9")
        window.configure(highlightcolor="black")

        # Full name label
        self.Label2 = tk.Label(window, activebackground="#f9f9f9", activeforeground="black", background="#f2f3f4",
                               disabledforeground="#a3a3a3", foreground="#000000", highlightbackground="#d9d9d9",
                               highlightcolor="black", text='''Full name:''')
        self.Label2.place(relx=0.316, rely=0.050, height=27, width=75)

        # Full name entry text box
        self.Entry2 = tk.Entry(window, background="#cae4ff", disabledforeground="#a3a3a3",
                               font="TkFixedFont", foreground="#000000", highlightbackground="#d9d9d9",
                               highlightcolor="black", insertbackground="black", selectbackground="blue",
                               selectforeground="white")
        self.Entry2.place(relx=0.511, rely=0.050, height=20, relwidth=0.302)
        
        
        # Account type label
        self.Label3 = tk.Label(window, activebackground="#f9f9f9", activeforeground="black", background="#f2f3f4",
                               disabledforeground="#a3a3a3", foreground="#000000", highlightbackground="#d9d9d9",
                               highlightcolor="black", text='''Account type:''')
        self.Label3.place(relx=0.287, rely=0.119, height=26, width=83)

        global acc_type
        acc_type = StringVar()
        
        # Account type entry button#1 (Savings)
        self.Radiobutton1 = tk.Radiobutton(window, activebackground="#ececec", activeforeground="#000000",
                                           background="#f2f3f4", disabledforeground="#a3a3a3", foreground="#000000",
                                           highlightbackground="#d9d9d9", highlightcolor="black", justify='left',
                                           text='''Savings''', variable=acc_type, value="S")
        self.Radiobutton1.place(relx=0.511, rely=0.124, relheight=0.057, relwidth=0.151)
        
        
        # Account type entry button#2 (Current)
        
        self.Radiobutton1_1 = tk.Radiobutton(window, activebackground="#ececec", activeforeground="#000000",
                                             background="#f2f3f4", disabledforeground="#a3a3a3", foreground="#000000",
                                             highlightbackground="#d9d9d9", highlightcolor="black", justify='left',
                                             text='''Current''', variable=acc_type, value="C")
        self.Radiobutton1_1.place(relx=0.706, rely=0.124, relheight=0.057, relwidth=0.175)
       

        self.Radiobutton1.deselect()
        self.Radiobutton1_1.deselect()
        
        # Birthdate label
        self.Label4 = tk.Label(window, activebackground="#f9f9f9", activeforeground="black", background="#f2f3f4",
                               disabledforeground="#a3a3a3", foreground="#000000",
                               highlightcolor="black", text='''Birth date (YYYY-MM-DD):''')
        self.Label4.place(relx=0.090, rely=0.188, height=27, width=175)

        # Birthdate entry text box
        self.Entry4 = tk.Entry(window, background="#cae4ff", disabledforeground="#a3a3a3", font="TkFixedFont",
                               foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black",
                               insertbackground="black", selectbackground="blue", selectforeground="white")
        self.Entry4.place(relx=0.511, rely=0.198, height=20, relwidth=0.302)
        
        
        # Mobile number label
        self.Label5 = tk.Label(window, activebackground="#f9f9f9", activeforeground="black", background="#f2f3f4",
                               disabledforeground="#a3a3a3", foreground="#000000",
                               highlightcolor="black", text='''Mobile number:''')
        self.Label5.place(relx=0.268, rely=0.282, height=22, width=85)
        
        # Mobile number entry text box
        self.Entry5 = tk.Entry(window, background="#cae4ff", disabledforeground="#a3a3a3", font="TkFixedFont",
                               foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black",
                               insertbackground="black", selectbackground="blue", selectforeground="white")
        self.Entry5.place(relx=0.511, rely=0.282, height=20, relwidth=0.302)


        # Gender label
        self.Label6 = tk.Label(window, activebackground="#f9f9f9", activeforeground="black", background="#f2f3f4",
                               disabledforeground="#a3a3a3", foreground="#000000",
                               highlightcolor="black", text='''Gender:''')
        self.Label6.place(relx=0.345, rely=0.347, height=15, width=65)

        global gender
        gender = StringVar()
        
        # Gender type entry button#1 (Male)
        self.Radiobutton3 = tk.Radiobutton(window, activebackground="#ececec", activeforeground="#000000",
                                           background="#f2f3f4", disabledforeground="#a3a3a3", foreground="#000000",
                                           highlightcolor="black", justify='left',
                                           text='''Male''', variable=gender, value="M")
        self.Radiobutton3.place(relx=0.481, rely=0.347, relheight=0.055, relwidth=0.175)
        
        # Gender type entry button#1 (Female)
        self.Radiobutton4 = tk.Radiobutton(window, activebackground="#ececec", activeforeground="#000000",
                                           background="#f2f3f4", disabledforeground="#a3a3a3", foreground="#000000",
                                           highlightbackground="#d9d9d9", highlightcolor="black", justify='left',
                                           text='''Female''', variable=gender, value="F")
        self.Radiobutton4.place(relx=0.706, rely=0.347, relheight=0.055, relwidth=0.175)

        self.Radiobutton3.deselect()
        self.Radiobutton4.deselect()
        
        # Country label
        self.Label7 = tk.Label(window, activebackground="#f9f9f9", activeforeground="black", background="#f2f3f4",
                               disabledforeground="#a3a3a3", foreground="#000000", highlightbackground="#d9d9d9",
                               highlightcolor="black", text='''Country:''')
        self.Label7.place(relx=0.330, rely=0.421, height=21, width=75)
        
        # Country entry text box
        self.Entry7 = tk.Entry(window, background="#cae4ff", disabledforeground="#a3a3a3",
                               font="TkFixedFont", foreground="#000000", highlightbackground="#d9d9d9",
                               highlightcolor="black", insertbackground="black", selectbackground="blue",
                               selectforeground="white")
        self.Entry7.place(relx=0.511, rely=0.421, height=20, relwidth=0.302)
        
        
        # National ID label
        self.Label8 = tk.Label(window, background="#f2f3f4", disabledforeground="#a3a3a3", foreground="#000000",
                               text='''National ID:''')
        self.Label8.place(relx=0.250, rely=0.496, height=24, width=122)
        
        # National ID entry text box
        self.Entry8 = tk.Entry(window, background="#cae4ff", disabledforeground="#a3a3a3", font="TkFixedFont",
                               foreground="#000000", insertbackground="black")
        self.Entry8.place(relx=0.511, rely=0.496, height=20, relwidth=0.302)
        
        
        # PIN label
        self.Label9 = tk.Label(window, activebackground="#f9f9f9", activeforeground="black", background="#f2f3f4",
                               disabledforeground="#a3a3a3", foreground="#000000", highlightbackground="#d9d9d9",
                               highlightcolor="black", text='''PIN:''')
        self.Label9.place(relx=0.399, rely=0.573, height=21, width=35)
        
        # PIN entry text box
        self.Entry9 = tk.Entry(window, show="*", background="#cae4ff", disabledforeground="#a3a3a3", font="TkFixedFont",
                               foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black",
                               insertbackground="black", selectbackground="blue", selectforeground="white")
        self.Entry9.place(relx=0.511, rely=0.573, height=20, relwidth=0.302)

        
        # Re-enter PIN label
        self.Label10 = tk.Label(window, activebackground="#f9f9f9", activeforeground="black", background="#f2f3f4",
                                disabledforeground="#a3a3a3", foreground="#000000", highlightbackground="#d9d9d9",
                                highlightcolor="black", text='''Re-enter PIN:''')
        self.Label10.place(relx=0.292, rely=0.645, height=21, width=75)
        
        # Re-enter PIN entry text box
        self.Entry10 = tk.Entry(window, show="*", background="#cae4ff", disabledforeground="#a3a3a3",
                                font="TkFixedFont",
                                foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black",
                                insertbackground="black", selectbackground="blue", selectforeground="white")
        self.Entry10.place(relx=0.511, rely=0.645, height=20, relwidth=0.302)
        
        
        # Initial balance lable
        self.Label11 = tk.Label(window, activebackground="#f9f9f9", activeforeground="black", background="#f2f3f4",
                                disabledforeground="#a3a3a3", foreground="#000000", highlightbackground="#d9d9d9",
                                highlightcolor="black", text='''Initial balance:''')
        self.Label11.place(relx=0.292, rely=0.729, height=21, width=75)
        
        # Initial balance entry text box
        self.Entry11 = tk.Entry(window, background="#cae4ff", disabledforeground="#a3a3a3", font="TkFixedFont",
                                foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black",
                                insertbackground="black", selectbackground="blue", selectforeground="white")
        self.Entry11.place(relx=0.511, rely=0.727, height=20, relwidth=0.302)
        
        
        # Back button
        self.Button1 = tk.Button(window, activebackground="#ececec", activeforeground="#000000", background="#004080",
                                 borderwidth="0", disabledforeground="#a3a3a3", foreground="#ffffff",
                                 highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text='''Back''',
                                 command=self.back)
        self.Button1.place(relx=0.292, rely=0.845, height=24, width=67)
        
        # Proceed button 
        self.Button2 = tk.Button(window, activebackground="#ececec", activeforeground="#000000", background="#004080",
                                 borderwidth="0", disabledforeground="#a3a3a3", foreground="#ffffff",
                                 highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text='''Proceed''',
                                 command=lambda: self.create_acc(self.Entry2.get() , acc_type.get()    , self.Entry4.get(), 
                                                                 self.Entry5.get() , gender.get()      , self.Entry7.get(), self.Entry8.get() , self.Entry9.get(),
                                                                 self.Entry10.get(), self.Entry11.get() ))
        self.Button2.place(relx=0.633, rely=0.845, height=24, width=67)



    def back(self):
        self.master.withdraw()

    def create_acc(self, name, account_type, date_of_birth, mobile_number, gender, nationality, national_ID, pin, 
                   confirm_PIN, initial_balance):
        
        if check_name(name):
            if check_accType(account_type):
                if check_date(date_of_birth):
                    if is_valid_mobile(mobile_number):
                        if check_gender(gender):
                            if check_nationality(nationality):
                                if check_national_ID(national_ID):
                                    if check_pin(pin):
                                        if confirm_PIN == pin:
                                            if check_balance(initial_balance):
                                                if check_age(date_of_birth):
                                                    adminMenu.printMessage_outside("")
                                                else:
                                                    Error(Toplevel(self.master))
                                                    Error.setMessage(self, message_shown="Age must be above 21 years!")
                                            else:
                                                Error(Toplevel(self.master))
                                                Error.setMessage(self, message_shown="Invalid balance!")
                                                return
                                        else:
                                            Error(Toplevel(self.master))
                                            Error.setMessage(self, message_shown="PIN mismatch!")
                                            return
                                    else:
                                        Error(Toplevel(self.master))
                                        Error.setMessage(self, message_shown="Invalid PIN!")
                                        return
                                else:
                                    Error(Toplevel(self.master))
                                    Error.setMessage(self, message_shown="Wrong National ID format!")
                                    return
                            else:
                                Error(Toplevel(self.master))
                                Error.setMessage(self, message_shown="Invalid Country!")
                                return
                        else:
                            Error(Toplevel(self.master))
                            Error.setMessage(self, message_shown="Select gender!")
                            return
                    else:
                        Error(Toplevel(self.master))
                        Error.setMessage(self, message_shown="Invalid mobile number!")
                        return
                else:
                    Error(Toplevel(self.master))
                    Error.setMessage(self, message_shown="Invalid date!")
                    return
            else:
                Error(Toplevel(self.master))
                Error.setMessage(self, message_shown="Select account type!")
                return
        else:
            Error(Toplevel(self.master))
            Error.setMessage(self, message_shown="Invalid Name!")
            return
    
    
        # adding in database
        data = (name, account_type, date_of_birth, age, mobile_number, gender, nationality, national_ID, pin, initial_balance)
        append_data(data)
        
        # Get the account number for the new clint
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="xx8489",
            database="bank"
        )
        
        mycursor = mydb.cursor()
        mycursor.execute("SELECT accNo FROM customers ORDER BY accNo DESC LIMIT 1;")
        acc_No = mycursor.fetchone()
        output_message = "Customer account created successfully with Account number " + str(acc_No[0]) + "."
        adminMenu.printMessage_outside(output_message)
        self.master.withdraw()

## Create Admin account

class createAdmin:
    def __init__(self, window=None):
        self.master = window
        window.geometry("411x150+512+237")
        window.minsize(120, 1)
        window.maxsize(1370, 749)
        window.resizable(0, 0)
        window.title("Create admin account")
        window.configure(background="#f2f3f4")
        
        # Admin ID label
        self.Label1 = tk.Label(window, background="#f2f3f4", disabledforeground="#a3a3a3", foreground="#000000",
                               text='''Enter admin ID:''')
        self.Label1.place(relx=0.219, rely=0.067, height=27, width=104)
        
        # Admin ID text box
        self.Entry1 = tk.Entry(window, background="#cae4ff", disabledforeground="#a3a3a3", font="TkFixedFont",
                               foreground="#000000", insertbackground="black")
        self.Entry1.place(relx=0.487, rely=0.087, height=20, relwidth=0.326)
        
        # Password label
        self.Label2 = tk.Label(window, background="#f2f3f4", disabledforeground="#a3a3a3", foreground="#000000",
                               text='''Enter password:''')
        self.Label2.place(relx=0.219, rely=0.267, height=27, width=104)
        
        # Password text box
        self.Entry2 = tk.Entry(window, show="*", background="#cae4ff", disabledforeground="#a3a3a3", font="TkFixedFont",
                               foreground="#000000", insertbackground="black")
        self.Entry2.place(relx=0.487, rely=0.287, height=20, relwidth=0.326)

        # Password Confirmation label
        self.Label3 = tk.Label(window, activebackground="#f9f9f9", activeforeground="black", background="#f2f3f4",
                               disabledforeground="#a3a3a3", foreground="#000000", highlightbackground="#d9d9d9",
                               highlightcolor="black", text='''Confirm password:''')
        self.Label3.place(relx=0.195, rely=0.467, height=27, width=104)
        
        # Password confirmation text box
        self.Entry3 = tk.Entry(window, show="*", background="#cae4ff", disabledforeground="#a3a3a3", font="TkFixedFont",
                               foreground="#000000", insertbackground="black")
        self.Entry3.place(relx=0.487, rely=0.487, height=20, relwidth=0.326)

        # Proceed button
        self.Button1 = tk.Button(window, activebackground="#ececec", activeforeground="#000000", background="#004080",
                                 borderwidth="0", disabledforeground="#a3a3a3", foreground="#ffffff",
                                 highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text="Proceed",
                                 command=lambda: self.create_admin_account(self.Entry1.get(), self.Entry2.get(),
                                                                           self.Entry3.get()))
        self.Button1.place(relx=0.598, rely=0.733, height=24, width=67)
        
        # Back button
        self.Button2 = tk.Button(window, activebackground="#ececec", activeforeground="#000000", background="#004080",
                                 borderwidth="0", disabledforeground="#a3a3a3", foreground="#ffffff",
                                 highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text="Back",
                                 command=self.back)
        self.Button2.place(relx=0.230, rely=0.733, height=24, width=67)

    def back(self):
        self.master.withdraw()

    def create_admin_account(self, identity, password, confirm_password):
        # Check ID
        if is_valid_admin(identity) == True or len(str(identity)) > 12 or len(str(identity)) == '':
            Error(Toplevel(self.master))
            Error.setMessage(self, message_shown="ID is unavailable or Invalid!")
        else:
            # Check Password
            if password == confirm_password and check_password(password):
                data = (identity, password)
                if append_data(data):
                    adminMenu.printMessage_outside("Admin account created successfully.")
                    self.master.withdraw()
            else:
                Error(Toplevel(self.master))
                if password != confirm_password:
                    Error.setMessage(self, message_shown="Password Mismatch!")
                else:
                    Error.setMessage(self, message_shown="Invalid password!")

## Show customer logs (withdraw and deposit)

class clientLogs:
    def __init__(self, window=None):
        self.master = window
        window.geometry("411x111")
        window.minsize(120, 1)
        window.maxsize(1370, 749)
        window.resizable(0, 0)
        window.title("Show client logs")
        window.configure(background="#f2f3f4")
        
        # Label1
        self.Label1 = tk.Label(window, background="#f2f3f4", disabledforeground="#a3a3a3", foreground="#000000",
                               text='''Enter account ID:''')
        self.Label1.place(relx=0.219, rely=0.092, height=21, width=104)
        
        # Label1 textbox
        self.Entry1 = tk.Entry(window, background="#cae4ff", disabledforeground="#a3a3a3", font="TkFixedFont",
                               foreground="#000000", insertbackground="black")
        self.Entry1.place(relx=0.487, rely=0.092, height=20, relwidth=0.277)
        
        # Back button
        self.Button1 = tk.Button(window, activebackground="#ececec", activeforeground="#000000", background="#004080",
                                 borderwidth="0", disabledforeground="#a3a3a3", foreground="#ffffff",
                                 highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text='''Back''',
                                 command=self.back)
        self.Button1.place(relx=0.243, rely=0.642, height=24, width=67)
        
        # Proceed button
        self.Button2 = tk.Button(window, activebackground="#ececec", activeforeground="#000000", background="#004080",
                                 borderwidth="0", disabledforeground="#a3a3a3", foreground="#ffffff",
                                 highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text='''Proceed''',
                                 command=lambda: self.show_logs(self.Entry1.get()))
        self.Button2.place(relx=0.608, rely=0.642, height=24, width=67)
    
    def show_logs(self, customer_account_number):
        if is_valid(customer_account_number):
            output = show_customer_logs(customer_account_number)
            adminMenu.printMessage_outside(output)
            
        else:
            Error(Toplevel(self.master))
            Error.setMessage(self, message_shown="Invalid Credentials!")

    def back(self):
        self.master.withdraw()

## Customer menu window

class customerMenu:
    def __init__(self, window=None):
        self.master = window
        window.geometry("743x494+329+153")
        window.minsize(120, 1)
        window.maxsize(1370, 749)
        window.resizable(0, 0)
        window.title("Customer Section")
        window.configure(background="#00254a")

        self.Labelframe1 = tk.LabelFrame(window, relief='groove', font="-family {Segoe UI} -size 13 -weight bold",
                                         foreground="#000000", text='''Select your option''', background="#fffffe")
        self.Labelframe1.place(relx=0.081, rely=0.081, relheight=0.415, relwidth=0.848)

        # Withdeaw button
        self.Button1 = tk.Button(self.Labelframe1, command=self.selectWithdraw, activebackground="#ececec",
                                 activeforeground="#000000", background="#39a9fc", borderwidth="0",
                                 disabledforeground="#a3a3a3", font="-family {Segoe UI} -size 11", foreground="#fffffe",
                                 highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text='''Withdraw''')
        self.Button1.place(relx=0.667, rely=0.195, height=34, width=181, bordermode='ignore')

        # Deposit button
        self.Button2 = tk.Button(self.Labelframe1, command=self.selectDeposit, activebackground="#ececec",
                                 activeforeground="#000000", background="#39a9fc", borderwidth="0",
                                 disabledforeground="#a3a3a3", font="-family {Segoe UI} -size 11", foreground="#fffffe",
                                 highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text='''Deposit''')
        self.Button2.place(relx=0.04, rely=0.195, height=34, width=181, bordermode='ignore')
        
        # Change PIN button
        self.Button4 = tk.Button(self.Labelframe1, command=self.selectChangePIN, activebackground="#ececec",
                                 activeforeground="#000000", background="#39a9fc", borderwidth="0",
                                 disabledforeground="#a3a3a3", font="-family {Segoe UI} -size 11", foreground="#fffffe",
                                 highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text='''Change PIN''')
        self.Button4.place(relx=0.04, rely=0.439, height=34, width=181, bordermode='ignore')

        # Close account button
        self.Button5 = tk.Button(self.Labelframe1, command=self.selectCloseAccount, activebackground="#ececec",
                                 activeforeground="#000000", background="#39a9fc", borderwidth="0",
                                 disabledforeground="#a3a3a3", font="-family {Segoe UI} -size 11", foreground="#fffffe",
                                 highlightbackground="#d9d9d9", highlightcolor="black", pady="0",
                                 text='''Close account''')
        self.Button5.place(relx=0.667, rely=0.439, height=34, width=181, bordermode='ignore')

        # Check balance button
        self.Button6 = tk.Button(self.Labelframe1, activebackground="#ececec", activeforeground="#000000",
                                 background="#39a9fc", borderwidth="0", disabledforeground="#a3a3a3",
                                 font="-family {Segoe UI} -size 11", foreground="#fffffe",
                                 highlightbackground="#d9d9d9", highlightcolor="black", pady="0",
                                 text='''Check balance''', command=self.checkBalance)
        self.Button6.place(relx=0.04, rely=0.683, height=34, width=181, bordermode='ignore')

        # Logout button
        self.Button3 = tk.Button(self.Labelframe1, command=self.exit, activebackground="#ececec",
                                 activeforeground="#000000",
                                 background="#39a9fc",
                                 borderwidth="0", disabledforeground="#a3a3a3", font="-family {Segoe UI} -size 11",
                                 foreground="#fffffe", highlightbackground="#d9d9d9", highlightcolor="black", pady="0",
                                 text='''Logout''')
        self.Button3.place(relx=0.667, rely=0.683, height=34, width=181, bordermode='ignore')

        global Frame1_1_2
        Frame1_1_2 = tk.Frame(window, relief='groove', borderwidth="2", background="#fffffe")
        Frame1_1_2.place(relx=0.081, rely=0.547, relheight=0.415, relwidth=0.848)

    def selectDeposit(self):
        depositMoney(Toplevel(self.master))

    def selectWithdraw(self):
        withdrawMoney(Toplevel(self.master))

    def selectChangePIN(self):
        changePIN(Toplevel(self.master))

    def selectCloseAccount(self):
        self.master.withdraw() # Close the app if the customer entered correct pin
        closeAccount(Toplevel(self.master))

    def exit(self):
        self.master.withdraw()
        CustomerLogin(Toplevel(self.master))

    def checkBalance(self):
        output = display_account_summary(customer_accNO, 2)
        self.printMessage(output)

    def printMessage(self, output):
        # clearing the frame
        for widget in Frame1_1_2.winfo_children():
            widget.destroy()
        # getting output_message and displaying it in the frame
        output_message = Label(Frame1_1_2, text=output, background="#fffffe")
        output_message.pack(pady=20)

    def printMessage_outside(output):
        # clearing the frame
        for widget in Frame1_1_2.winfo_children():
            widget.destroy()
        # getting output_message and displaying it in the frame
        output_message = Label(Frame1_1_2, text=output, background="#fffffe")
        output_message.pack(pady=20)

## Deposit money window

class depositMoney:
    def __init__(self, window=None):
        self.master = window
        window.geometry("411x117+519+278")
        window.minsize(120, 1)
        window.maxsize(1370, 749)
        window.resizable(0, 0)
        window.title("Deposit money")
        p1 = PhotoImage(file='./images/deposit_icon.png')
        window.iconphoto(True, p1)
        window.configure(borderwidth="2")
        window.configure(background="#f2f3f4")
        
        # Label1
        self.Label1 = tk.Label(window, background="#f2f3f4", disabledforeground="#a3a3a3",
                               font="-family {Segoe UI} -size 9", foreground="#000000", borderwidth="0",
                               text='''Enter amount to deposit :''')
        self.Label1.place(relx=0.146, rely=0.171, height=21, width=164)
        
        # Label1 textbox
        self.Entry1 = tk.Entry(window, background="#cae4ff", disabledforeground="#a3a3a3", font="TkFixedFont",
                               foreground="#000000", insertbackground="black", selectforeground="#ffffffffffff")
        self.Entry1.place(relx=0.535, rely=0.171, height=20, relwidth=0.253)
        
        # Proceed button
        self.Button1 = tk.Button(window, activebackground="#ececec", activeforeground="#000000", background="#004080",
                                 disabledforeground="#a3a3a3", borderwidth="0", foreground="#ffffff",
                                 highlightbackground="#000000",
                                 highlightcolor="black", pady="0", text='''Proceed''',
                                 command=lambda: self.submit(self.Entry1.get()))
        self.Button1.place(relx=0.56, rely=0.598, height=24, width=67)
        
        # Back button
        self.Button2 = tk.Button(window, activebackground="#ececec", activeforeground="#000000", background="#004080",
                                 disabledforeground="#a3a3a3", font="-family {Segoe UI} -size 9", foreground="#ffffff",
                                 highlightbackground="#d9d9d9", borderwidth="0", highlightcolor="black", pady="0",
                                 text='''Back''',
                                 command=self.back)
        self.Button2.place(relx=0.268, rely=0.598, height=24, width=67)

    def submit(self, amount):
        if amount.isnumeric():
            if 25000 >= float(amount) > 0:
                output = transaction(customer_accNO, amount, 1)
                store_logs(customer_accNO, 'D', amount)
            else:
                Error(Toplevel(self.master))
                if float(amount) > 25000:
                    Error.setMessage(self, message_shown="Limit exceeded!")
                else:
                    Error.setMessage(self, message_shown="Positive value expected!")
                return
        else:
            Error(Toplevel(self.master))
            Error.setMessage(self, message_shown="Invalid amount!")
            return
        
        #if the deposite failed, print error message. Otherwise print a message
        if output == -1 or output == None:
            Error(Toplevel(self.master))
            Error.setMessage(self, message_shown="Transaction failed!")
            return
        else:
            message = str(amount) + "EGP deposited successfully.\nUpdated balance : " + str(output) + "EGP."
            customerMenu.printMessage_outside(message)
            self.master.withdraw()

    def back(self):
        self.master.withdraw()

## Widthdraw money window

class withdrawMoney:
    def __init__(self, window=None):
        self.master = window
        window.geometry("411x117+519+278")
        window.minsize(120, 1)
        window.maxsize(1370, 749)
        window.resizable(0, 0)
        window.title("Withdraw money")
        p1 = PhotoImage(file='./images/withdraw_icon.png')
        window.iconphoto(True, p1)
        window.configure(borderwidth="2")
        window.configure(background="#f2f3f4")
        
        # Label1
        self.Label1 = tk.Label(window, background="#f2f3f4", disabledforeground="#a3a3a3",
                               font="-family {Segoe UI} -size 9", foreground="#000000",
                               text='''Enter amount to withdraw :''')
        self.Label1.place(relx=0.146, rely=0.171, height=21, width=164)
        
        # Label1 textbox
        self.Entry1 = tk.Entry(window, background="#cae4ff", disabledforeground="#a3a3a3", font="TkFixedFont",
                               foreground="#000000", insertbackground="black", selectforeground="#ffffffffffff")
        self.Entry1.place(relx=0.535, rely=0.171, height=20, relwidth=0.253)
        
        # Proceed button
        self.Button1 = tk.Button(window, activebackground="#ececec", activeforeground="#000000", background="#004080",
                                 disabledforeground="#a3a3a3", borderwidth="0", foreground="#ffffff",
                                 highlightbackground="#000000",
                                 highlightcolor="black", pady="0", text='''Proceed''',
                                 command=lambda: self.submit(self.Entry1.get()))
        self.Button1.place(relx=0.56, rely=0.598, height=24, width=67)
        
        # Back button
        self.Button2 = tk.Button(window, activebackground="#ececec", activeforeground="#000000", background="#004080",
                                 disabledforeground="#a3a3a3", borderwidth="0", font="-family {Segoe UI} -size 9",
                                 foreground="#ffffff",
                                 highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text='''Back''',
                                 command=self.back)
        self.Button2.place(relx=0.268, rely=0.598, height=24, width=67)

    def submit(self, amount):
        if amount.isnumeric():
            if 25000 >= float(amount) > 0:
                output = transaction(customer_accNO, amount, 2)
                store_logs(customer_accNO, 'W', amount)
            else:
                Error(Toplevel(self.master))
                if float(amount) > 25000:
                    Error.setMessage(self, message_shown="Limit exceeded!")
                else:
                    Error.setMessage(self, message_shown="Positive value expected!")
                return
        else:
            Error(Toplevel(self.master))
            Error.setMessage(self, message_shown="Invalid amount!")
            return
        
        # if the widthdraw failed, print error message. Otherwise print a message
        if output == -1:
            Error(Toplevel(self.master))
            Error.setMessage(self, message_shown="Balance not enough!")
            return
        elif output == None:
            Error(Toplevel(self.master))
            Error.setMessage(self, message_shown="Transaction failed!")
            return
        else:
            output = str(amount) + "EGP withdrawn successfully.\nUpdated balance : " + str(output) + "EGP."
            customerMenu.printMessage_outside(output)
            self.master.withdraw()

    def back(self):
        self.master.withdraw()

## Change PIN window

class changePIN:
    def __init__(self, window=None):
        self.master = window
        window.geometry("411x200")
        window.minsize(120, 1)
        window.maxsize(1370, 749)
        window.resizable(0, 0)
        window.title("Change PIN")
        window.configure(background="#f2f3f4")

        # Label1
        self.Label1 = tk.Label(window, background="#f2f3f4", disabledforeground="#a3a3a3", foreground="#000000",
                               text='''Enter current PIN:''')
        self.Label1.place(relx=0.280, rely=0.100, height=21, width=93)
        
        # Label1 textbox
        self.Entry1 = tk.Entry(window, show="*", background="#cae4ff", disabledforeground="#a3a3a3", font="TkFixedFont",
                               foreground="#000000", insertbackground="black")
        self.Entry1.place(relx=0.528, rely=0.100, height=20, relwidth=0.229)
        
        # Label2
        self.Label2 = tk.Label(window, background="#f2f3f4", disabledforeground="#a3a3a3", foreground="#000000",
                               text='''Enter new PIN:''')
        self.Label2.place(relx=0.300, rely=0.264, height=21, width=93)
        
        # Label2 textbox
        self.Entry2 = tk.Entry(window, show="*", background="#cae4ff", disabledforeground="#a3a3a3", font="TkFixedFont",
                               foreground="#000000", insertbackground="black")
        self.Entry2.place(relx=0.528, rely=0.264, height=20, relwidth=0.229)
        
        # Label3
        self.Label3 = tk.Label(window, background="#f2f3f4", disabledforeground="#a3a3a3", foreground="#000000",
                               text='''Confirm PIN:''')
        self.Label3.place(relx=0.320, rely=0.420, height=21, width=82)
        
        # Label3 textbox
        self.Entry3 = tk.Entry(window, show="*", background="#cae4ff", disabledforeground="#a3a3a3", font="TkFixedFont",
                               foreground="#000000", insertbackground="black")
        self.Entry3.place(relx=0.528, rely=0.420, height=20, relwidth=0.229)

        # Proceed button
        self.Button1 = tk.Button(window, activebackground="#ececec", activeforeground="#000000", background="#004080",
                                 disabledforeground="#a3a3a3", foreground="#ffffff", borderwidth="0",
                                 highlightbackground="#d9d9d9",
                                 highlightcolor="black", pady="0", text='''Proceed''',
                                 command=lambda: self.submit(self.Entry1.get(), self.Entry2.get(), self.Entry3.get()))
        self.Button1.place(relx=0.614, rely=0.721, height=24, width=67)

        # Back button
        self.Button2 = tk.Button(window, activebackground="#ececec", activeforeground="#000000", background="#004080",
                                 disabledforeground="#a3a3a3", foreground="#ffffff", borderwidth="0",
                                 highlightbackground="#d9d9d9",
                                 highlightcolor="black", pady="0", text="Back", command=self.back)
        self.Button2.place(relx=0.214, rely=0.721, height=24, width=67)

    def submit(self, old_PIN, new_PIN, confirm_new_PIN):
        if new_PIN == confirm_new_PIN and check_pin(new_PIN) and change_PIN(customer_accNO, old_PIN, new_PIN):
            output = "PIN updated successfully."
            customerMenu.printMessage_outside(output)
            self.master.withdraw()
        else:
            Error(Toplevel(self.master))
            if new_PIN != confirm_new_PIN:
                Error.setMessage(self, message_shown="PIN mismatch!")
            elif str(new_PIN).__len__() != 4:
                Error.setMessage(self, message_shown="PIN length must be 4!")
            else:
                Error.setMessage(self, message_shown="Invalid PIN!")
            return

    def back(self):
        self.master.withdraw()

## Close account by customer window

class closeAccount:
    def __init__(self, window=None):
        self.master = window
        window.geometry("411x117+498+261")
        window.minsize(120, 1)
        window.maxsize(1370, 749)
        window.resizable(0, 0)
        window.title("Close Account")
        window.configure(background="#f2f3f4")
        
        # Label1
        self.Label1 = tk.Label(window, background="#f2f3f4", disabledforeground="#a3a3a3", foreground="#000000",
                               text='''Enter your PIN:''')
        self.Label1.place(relx=0.268, rely=0.256, height=21, width=94)
        
        # Label1 textbox
        self.Entry1 = tk.Entry(window, show="*", background="#cae4ff", disabledforeground="#a3a3a3", font="TkFixedFont",
                               foreground="#000000", insertbackground="black")
        self.Entry1.place(relx=0.511, rely=0.256, height=20, relwidth=0.229)
        
        # Proceed button
        self.Button1 = tk.Button(window, activebackground="#ececec", activeforeground="#000000", background="#004080",
                                 disabledforeground="#a3a3a3", foreground="#ffffff", borderwidth="0",
                                 highlightbackground="#d9d9d9",
                                 highlightcolor="black", pady="0", text='''Proceed''',
                                 command=lambda: self.submit(self.Entry1.get()))
        self.Button1.place(relx=0.614, rely=0.712, height=24, width=67)
        
        # Back button
        self.Button2 = tk.Button(window, activebackground="#ececec", activeforeground="#000000", background="#004080",
                                 disabledforeground="#a3a3a3", foreground="#ffffff", borderwidth="0",
                                 highlightbackground="#d9d9d9",
                                 highlightcolor="black", pady="0", text="Back", command=self.back)
        self.Button2.place(relx=0.214, rely=0.712, height=24, width=67)

    def submit(self, PIN):
        if check_credentials(customer_accNO, PIN, 2):
            delete_customer_account(customer_accNO)
            self.master.withdraw()
            CustomerLogin(Toplevel(self.master))
        else:
            Error(Toplevel(self.master))
            Error.setMessage(self, message_shown="Invalid PIN!")

    def back(self):
        self.master.withdraw()
        customerMenu(Toplevel(self.master))

## Check account summary

class checkAccountSummary:
    def __init__(self, window=None):
        self.master = window
        window.geometry("411x117+498+261")
        window.minsize(120, 1)
        window.maxsize(1370, 749)
        window.resizable(0, 0)
        window.title("Check Account Summary")
        window.configure(background="#f2f3f4")

        self.Label1 = tk.Label(window, background="#f2f3f4", disabledforeground="#a3a3a3", foreground="#000000",
                               text='''Enter ID :''')
        self.Label1.place(relx=0.268, rely=0.256, height=21, width=94)

        self.Entry1 = tk.Entry(window, background="#cae4ff", disabledforeground="#a3a3a3", font="TkFixedFont",
                               foreground="#000000", insertbackground="black")
        self.Entry1.place(relx=0.511, rely=0.256, height=20, relwidth=0.229)

        self.Button1 = tk.Button(window, activebackground="#ececec", activeforeground="#000000", background="#004080",
                                 disabledforeground="#a3a3a3", foreground="#ffffff", borderwidth="0",
                                 highlightbackground="#d9d9d9",
                                 highlightcolor="black", pady="0", text='''Proceed''',
                                 command=lambda: self.submit(self.Entry1.get()))
        self.Button1.place(relx=0.614, rely=0.712, height=24, width=67)

        self.Button2 = tk.Button(window, activebackground="#ececec", activeforeground="#000000", background="#004080",
                                 disabledforeground="#a3a3a3", foreground="#ffffff", borderwidth="0",
                                 highlightbackground="#d9d9d9",
                                 highlightcolor="black", pady="0", text="Back", command=self.back)
        self.Button2.place(relx=0.214, rely=0.712, height=24, width=67)

    def back(self):
        self.master.withdraw()

    def submit(self, identity):
        if is_valid(identity):
            adminMenu.printAccountSummary(identity)
        else:
            Error(Toplevel(self.master))
            Error.setMessage(self, message_shown="Invalid credentials!")
            return
        self.master.withdraw()

root = tk.Tk()
top = welcomeScreen(root)
root.mainloop()