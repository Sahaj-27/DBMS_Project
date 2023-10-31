from mysql.connector import Error
from tkinter import *
from datetime import datetime, timedelta
from tkinter import messagebox


import yfinance as yf
import random
import mysql.connector
import tkinter as tk
import sys


path2 = "A:\\Final_Project\\"


path = "A:\\Final_Project\\addinvestment_page\\"


class addinvestment(tk.Frame):
    
    def read_loggedin_userid():
        try:
            with open(path2 + 'user_id.txt', 'r') as f:
                loggedin_userid = int(f.read().strip())
            return loggedin_userid
        except FileNotFoundError:
            print("No user ID file found. Please log in first.")
            return None
        except Exception as e:
            print("Error while reading user ID:", e)
            return None
    
    def get_stock_currency(ticker):
        stock = yf.Ticker(ticker)
        info = stock.info
        return info.get('currency')
    
    def get_stock_price_on_date(ticker, date, days_range = 5):
        stock = yf.Ticker(ticker)
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        start_date = (date_obj - timedelta(days=days_range)).strftime("%Y-%m-%d")
        end_date = (date_obj + timedelta(days=days_range)).strftime("%Y-%m-%d")
        data = stock.history(start=start_date, end=end_date)
        if not data.empty:
            timezone = data.index[0].tzinfo
            date_obj = date_obj.replace(tzinfo=timezone)
            closest_date = min(data.index, key=lambda x: abs(x - date_obj))
            price = data.loc[closest_date]['Close']
            return price
        else:
            print(f"No data available for {ticker} around {date}")
            return None

    def get_current_price(symbol):
        stock_info = yf.Ticker(symbol)
        stock_data = stock_info.history(period="1d")
        return stock_data['Close'][0]

    def get_number_of_units(amount, price):
        return amount / price

    def is_valid_investment_type(investment_type):
        if investment_type not in ["Stock", "Index Fund", "Crypto Currency"]:
            return False
        return True

    def is_valid_date(date_str):
        try:
            input_date = datetime.strptime(date_str, '%d-%m-%Y')
            current_date = datetime.now()
            if input_date > current_date:
                return False
            return True
        except ValueError:
            return False
    
    def is_valid_investment_name(investment_name, investment_type):
        if not investment_name.isupper():
            return False
        if investment_type == "Crypto Currency":
            if not investment_name.endswith("USD"):
                return False
        if investment_type  == "Index Fund":
            if not investment_name.startswith("^"):
                return False    
        return True

    def is_valid_amount(amount):
        if not amount.isdigit():
            return False
        return True

    def generate_unique_number():
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="Personal_Finance_Management"
        )

        if connection.is_connected():
            cursor = connection.cursor()
            query = "SELECT user_id FROM Investment"
            cursor.execute(query)
            user_id_list = cursor.fetchall()

            # Convert the list of tuples to a set of user_ids
            if user_id_list:
                used_numbers = {user_id[0] for user_id in user_id_list}
            else:
                used_numbers = set()
            while True:
                num = random.randint(1000, 9999)
                if num not in used_numbers:
                    return num
    
    def is_valid_invest_account(invest_account):
        
        if not invest_account.isdigit():
            return False

        elif len(invest_account) not in [8, 12]:
            return False

        else:
            try:
                connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="root",
                    database="Personal_Finance_Management"
                )
                if connection.is_connected():
                    cursor = connection.cursor()
                    query = "SELECT account_id FROM Account WHERE account_id = %s and user_id = %s"
                    cursor.execute(query, (invest_account, addinvestment.read_loggedin_userid()))
                    if cursor.fetchall():
                        return True
                    else:
                        return False

            except Error as e:
                print(f"Error: {e}")
                return False

            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()

    def insert_investment(amount, date, investment_name, remarks, invest_account, investment_type):
        
        try:
            
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database='Personal_Finance_Management'
            )
            
            if connection.is_connected():
                
                cursor = connection.cursor()
                user_id = addinvestment.read_loggedin_userid()
                account_id = invest_account
                date_datetime = datetime.strptime(date, '%d-%m-%Y')
                date_mysql_format = date_datetime.strftime('%Y-%m-%d')
                investment_id = addinvestment.generate_unique_number()
                balance_query = f"SELECT balance FROM Account WHERE account_id = '{account_id}' AND user_id = '{user_id}'"
                cursor.execute(balance_query)
                current_balance = cursor.fetchone()[0]
                
                if float(current_balance) < float(amount):
                    return "insufficient_balance"

                amount = float(amount)
                    
                try:
                    temp_current_price = addinvestment.get_current_price(investment_name) 
                    previous_price = addinvestment.get_stock_price_on_date(
                        investment_name, date_mysql_format)
                    if addinvestment.get_stock_currency(investment_name) == "USD":
                        temp_current_price = temp_current_price * 81.75
                        previous_price = previous_price * 81.75
                    number_of_units = addinvestment.get_number_of_units(
                    amount, previous_price)
                    current_price = temp_current_price * number_of_units
                    return_rate = (current_price - amount) / amount * 100
                    
                except:
                    return "invalid_investment_name"    
                    
                query = f"INSERT INTO Investment (investment_id, user_id, account_id, investment_type, investment_name, purchase_date, purchase_price, current_value, return_rate, remarks, number_of_units) VALUES ('{investment_id}', '{user_id}', '{account_id}', '{investment_type}', '{investment_name}', '{date_mysql_format}', '{amount}', '{current_price}', '{return_rate}', '{remarks}', '{number_of_units}')"
                cursor.execute(query)
                
                update_query = f"UPDATE Account SET balance = balance - {amount} WHERE account_id = '{account_id}' AND user_id = '{user_id}'"
                cursor.execute(update_query)

                connection.commit()
                return True

        except Error as e:
            print("Error while connecting to MySQL", e)
            return False

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent, bg='#093545')

        global img0, img1, background_img, entry0_img, entry1_img, entry2_img, entry3_img, entry4_img, entry5_img
        
        def clear_entry_fields():
            entry0.delete(0, tk.END)
            entry1.delete(0, tk.END)
            entry2.delete(0, tk.END)
            entry3.delete(0, tk.END)
            entry4.delete(0, tk.END)
            entry5.delete(0, tk.END)

        self.controller = controller

        background_img = tk.PhotoImage(file=path + "addinvestment0.png")

        bck_label = tk.Label(self, image=background_img,
                             relief="flat", bg="#093545")

        bck_label.place(x=0, y=0, width=1537, height=864)

        entry0_img = tk.PhotoImage(file=path + "addinvestment1.png")

        entry0_label = tk.Label(self, image=entry0_img,
                                relief="flat", bg="#093A45")

        entry0_label.place(x=266, y=273, width=441, height=54)

        entry0_font = ("Lexend Deca", 20)

        entry0 = tk.Entry(self,
                          bd=0,
                          bg="#093A45",
                          highlightthickness=0,
                          font=entry0_font,
                          fg="white")

        entry0.place(x=276, y=273,
                     width=421,
                     height=52)

        entry1_img = tk.PhotoImage(file=path + "addinvestment2.png")

        entry1_label = tk.Label(self, image=entry1_img,
                                relief="flat", bg="#093A45")

        entry1_label.place(x=851, y=405, width=441, height=54)

        entry1_font = ("Lexend Deca", 20)

        entry1 = tk.Entry(self,
                          bd=0,
                          bg="#093A45",
                          highlightthickness=0,
                          font=entry1_font,
                          fg="white")

        entry1.place(
            x=861, y=405,
            width=421,
            height=52)

        entry2_img = tk.PhotoImage(file=path + "addinvestment3.png")

        entry2_label = tk.Label(self, image=entry2_img,
                                relief="flat", bg="#093A45")

        entry2_label.place(x=851, y=536, width=441, height=54)

        entry2_font = ("Lexend Deca", 20)

        entry2 = tk.Entry(self,
                          bd=0,
                          bg="#093A45",
                          highlightthickness=0,
                          font=entry2_font,
                          fg="white")

        entry2.place(
            x=861, y=536,
            width=421,
            height=52)

        entry3_img = tk.PhotoImage(file=path + "addinvestment4.png")

        entry3_label = tk.Label(self, image=entry3_img,
                                relief="flat", bg="#093A45")

        entry3_label.place(x=851, y=273, width=441, height=54)

        entry3_font = ("Lexend Deca", 20)

        entry3 = tk.Entry(self,
                          bd=0,
                          bg="#093A45",
                          highlightthickness=0,
                          font=entry3_font,
                          fg="white")

        entry3.place(
            x=861, y=273,
            width=421,
            height=52)

        entry4_img = tk.PhotoImage(file=path + "addinvestment5.png")

        entry4_label = tk.Label(self, image=entry4_img,
                                relief="flat", bg="#093A45")

        entry4_label.place(x=266, y=405, width=441, height=54)

        entry4_font = ("Lexend Deca", 20)

        entry4 = tk.Entry(self,
                          bd=0,
                          bg="#093A45",
                          highlightthickness=0,
                          font=entry4_font,
                          fg="white")

        entry4.place(
            x=276, y=405,
            width=421,
            height=52)

        entry5_img = tk.PhotoImage(file=path + "addinvestment6.png")

        entry5_label = tk.Label(self, image=entry5_img,
                                relief="flat", bg="#093A45")

        entry5_label.place(x=266, y=536, width=441, height=54)

        entry5_font = ("Lexend Deca", 20)

        entry5 = tk.Entry(self,
                          bd=0,
                          bg="#093A45",
                          highlightthickness=0,
                          font=entry5_font,
                          fg="white")

        entry5.place(
            x=276, y=536,
            width=421,
            height=52)

        def b0_clicked():

            investment_type = entry0.get()
            investment_name = entry4.get()
            date = entry5.get()
            amount = entry3.get()
            invest_account = entry1.get()
            remarks = entry2.get()

            if not all([investment_type, investment_name, date, amount, invest_account]):
                tk.messagebox.showerror("Error", "Please fill all the fields except maybe remarks")
                return
            
            if not remarks:
                remarks = None
                
            if not addinvestment.is_valid_invest_account(invest_account):
                tk.messagebox.showerror("Error", "Invalid Investment Account")
                return

            if not addinvestment.is_valid_date(date):
                tk.messagebox.showerror("Error", "Invalid Investment Date")
                return

            if not addinvestment.is_valid_amount(amount):
                tk.messagebox.showerror("Error", "Invalid amount")
                return

            if not addinvestment.is_valid_investment_type(investment_type):
                tk.messagebox.showerror("Error", "Invalid Investment Type")
                return

            if not addinvestment.is_valid_investment_name(investment_name, investment_type):
                tk.messagebox.showerror("Error", "Invalid Investment Name")
                return

            result = addinvestment.insert_investment(amount, date, investment_name, remarks, invest_account, investment_type)
            
            if result == "insufficient_balance":
                tk.messagebox.showerror(
                    "Error", "Insufficient account balance")
            elif result == "invalid_investment_name":
                tk.messagebox.showerror(
                    "Error", "Invalid Investment Name or Date")
            elif result :
                tk.messagebox.showinfo(
                    "Success", "Investment added successfully!")
                clear_entry_fields()
                controller.show_frame("myinvestments")
            else:
                tk.messagebox.showerror(
                    "Error", "Failed to add account. Please try again.")
                clear_entry_fields()

        img0 = tk.PhotoImage(file=path + "addinvestment7.png")
        b0 = tk.Button(self,
                       image=img0,
                       borderwidth=0,
                       highlightthickness=0,
                       command=b0_clicked,
                       bg="#092f40",
                       background="#092f40",
                       activebackground="#092f40",
                       cursor="hand2",
                       relief="flat")

        b0.place(
            x=796, y=661,
            width=266,
            height=62)

        def b1_clicked():
            clear_entry_fields()
            controller.show_frame("myinvestments")

        img1 = tk.PhotoImage(file=path + "addinvestment8.png")

        b1 = tk.Button(self,
                       image=img1,
                       borderwidth=0,
                       highlightthickness=0,
                       command=b1_clicked,
                       bg="#092f40",
                       background="#092f40",
                       activebackground="#092f40",
                       cursor="hand2",
                       relief="flat")

        b1.place(
            x=477, y=661,
            width=266,
            height=62)
