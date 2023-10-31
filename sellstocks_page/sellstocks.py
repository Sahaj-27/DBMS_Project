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


path = "A:\\Final_Project\\sellstocks_page\\"


class sellstocks(tk.Frame):
    
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
    
    def get_stock_price_on_date(ticker, date, days_range=5):
        stock = yf.Ticker(ticker)
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        start_date = (date_obj - timedelta(days=days_range)
                      ).strftime("%Y-%m-%d")
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
        
    def get_stock_currency(ticker):
        stock = yf.Ticker(ticker)
        info = stock.info
        return info.get('currency')
    
    def is_valid_invest_id(invest_id, invest_name, number_of_units):

        if not invest_id.isdigit():
            return False

        elif len(invest_id) != 4:
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
                    query = f"SELECT investment_id, investment_name, number_of_units, account_id, current_value, purchase_date FROM Investment WHERE investment_id = '{invest_id}' and user_id = '{sellstocks.read_loggedin_userid()}'"
                    cursor.execute(query)

                    row = cursor.fetchone()
                    # Fetch the row once and store it in a variable
                    print(row)
                    if row is None:
                        return False

                    print(row[0] == invest_id)
                    print(row[1] == invest_name)
                    print(number_of_units)
                    if number_of_units == 0 and  row[1] == invest_name:
                        query = f"DELETE FROM Investment WHERE investment_id = '{invest_id}' and user_id = '{sellstocks.read_loggedin_userid()}'"
                        cursor.execute(query)
                        print("Investment deleted successfully")
                        update_balance = f"UPDATE Account SET balance = balance + '{row[4]}' WHERE account_id = '{row[3]}' and user_id = '{sellstocks.read_loggedin_userid()}'"
                        cursor.execute(update_balance)
                        print("Balance updated successfully")
                        connection.commit()
                        return True

                    if row[1] == invest_name and row[2] > number_of_units and number_of_units > 0:

                        query = f"UPDATE Investment SET number_of_units = number_of_units - '{number_of_units}' WHERE investment_id = '{invest_id}' and user_id = '{sellstocks.read_loggedin_userid()}'"
                        cursor.execute(query)
            
                        if sellstocks.get_stock_currency(row[1]) == "USD":
                            temp = number_of_units * sellstocks.get_stock_price_on_date(row[1], (str)(row[5])) * 81.75
                            query2 = f"UPDATE Investment SET purchase_price = purchase_price - '{temp}' WHERE investment_id = '{invest_id}' and user_id = '{sellstocks.read_loggedin_userid()}'"
                            cursor.execute(query2)
                        else :
                            temp = number_of_units * sellstocks.get_stock_price_on_date(row[1], (str)(row[5]))
                            query2 = f"UPDATE Investment SET purchase_price = purchase_price - '{temp}' WHERE investment_id = '{invest_id}' and user_id = '{sellstocks.read_loggedin_userid()}'"
                            cursor.execute(query2)    
                        update_balance = f"UPDATE Account SET balance = balance + '{row[4]}' WHERE account_id = '{row[3]}' and user_id = '{sellstocks.read_loggedin_userid()}'"
                        cursor.execute(update_balance)
                        connection.commit()
                        return True

            except Error as e:
                print(f"Error: {e}")
                return False

            finally:
                if connection.is_connected():
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
        
        background_img = tk.PhotoImage(file=path + "sellstocks0.png")

        bck_label = tk.Label(self, image=background_img,
                             relief="flat", bg="#093545")

        bck_label.place(x=0, y=0, width=1537, height=864)
        
        entry0_img = tk.PhotoImage(file=path + "sellstocks1.png")

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

        entry1_img = tk.PhotoImage(file=path + "sellstocks2.png")

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

        entry2_img = tk.PhotoImage(file=path + "sellstocks3.png")

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

        entry3_img = tk.PhotoImage(file=path + "sellstocks4.png")

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

        entry4_img = tk.PhotoImage(file=path + "sellstocks5.png")

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

        entry5_img = tk.PhotoImage(file=path + "sellstocks6.png")

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
            
            investment_id = entry0.get()
            investment_name = entry4.get()
            category = entry5.get()
            selltype = entry3.get()
            number_of_units = entry1.get()
            remarks = entry2.get()
            
            if not all ([investment_id, selltype, investment_name]):
                tk.messagebox.showerror(
                        "Error", "Please fill Investment ID, Investment Name and Sell Type fields")
                return
                
            if selltype == "Partial" :
                if not number_of_units:
                    tk.messagebox.showerror(
                        "Error", "Please fill all fields except maybe category and remarks")
                    return
            
            elif selltype == "Full" :
                if not number_of_units:
                    number_of_units = 0
                else :
                    tk.messagebox.showerror(
                        "Error", "You have selected Full Sell Type, please leave Number of Units field empty")
                    return    
            
            else:
                tk.messagebox.showerror(
                        "Error", "Invalid Sell Type, please enter either Full or Partial")
                return
            
            if not remarks:
                remarks = "None"
                
            if not category:
                category = "None"
             
            result = sellstocks.is_valid_invest_id(
                investment_id, investment_name, (float)(number_of_units)) 
            
            if result:
                tk.messagebox.showinfo(
                        "Success", "Investment Sold Successfully")
                clear_entry_fields()
                controller.show_frame("myinvestments")
                return
            
            else :
                tk.messagebox.showerror(
                        "Error", "Invalid Investment ID or Investment Name or Number of Units")
                return
        
        img0 = tk.PhotoImage(file=path + "sellstocks7.png")
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

        img1 = tk.PhotoImage(file=path + "sellstocks8.png")

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
        
        