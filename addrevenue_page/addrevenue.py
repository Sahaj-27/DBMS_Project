import random
import tkinter as tk
import mysql.connector
import sys


from pathlib import Path
from datetime import datetime
from mysql.connector import Error


path2 = "A:\\Final_Project\\"


path = "A:\\Final_Project\\addrevenue_page\\"


class addrevenue(tk.Frame):
    
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
    
    def is_valid_amount(amount):
        if not amount.isdigit():
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
        
    def is_valid_source(source):
        return all(char.isalpha() or char.isspace() for char in source)
    
    def generate_unique_number():
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="Personal_Finance_Management"
        )

        if connection.is_connected():
            cursor = connection.cursor()
            query = "SELECT user_id FROM Income"
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
    
    def is_valid_credit_account(credit_account):
        
        if not credit_account.isdigit():
            return False
        
        elif len(credit_account) not in [8, 12]:
            return False
        
        else :    
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
                    cursor.execute(query, (credit_account, addrevenue.read_loggedin_userid()))
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
                
    def insert_income(amount, date, source, remarks, credit_account, category):
        
        try:
            
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database='Personal_Finance_Management'
            )

            if connection.is_connected():
                cursor = connection.cursor()
                user_id = addrevenue.read_loggedin_userid()
                account_id = credit_account
                date_datetime = datetime.strptime(date, '%d-%m-%Y')
                date_mysql_format = date_datetime.strftime('%Y-%m-%d')
                income_id = addrevenue.generate_unique_number()
                query = f"INSERT INTO Income (income_id, user_id, account_id, amount, income_date, source, remarks, category) VALUES ('{income_id}', '{user_id}', '{account_id}', '{amount}', '{date_mysql_format}', '{source}', '{remarks}', '{category}')"
                cursor.execute(query)
                update_query = f"UPDATE Account SET balance = balance + {amount} WHERE account_id = '{account_id}' AND user_id = '{user_id}'"
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

    def  is_valid_category(category):
        return all(char.isalpha() or char.isspace() for char in category)
    
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

        background_img = tk.PhotoImage(file = path + "addrevenue0.png")
        
        bck_label = tk.Label(self, image=background_img,
                             relief="flat", bg="#093545")

        bck_label.place(x=0, y=0, width=1537, height=864)
        
        entry0_img = tk.PhotoImage(file=path + "addrevenue1.png")

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

        entry1_img = tk.PhotoImage(file=path + "addrevenue2.png")

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

        entry2_img = tk.PhotoImage(file=path + "addrevenue3.png")

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

        entry3_img = tk.PhotoImage(file=path + "addrevenue4.png")

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

        entry4_img = tk.PhotoImage(file=path + "addrevenue5.png")

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

        entry5_img = tk.PhotoImage(file=path + "addrevenue6.png")

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
            
            amount = entry0.get()
            date = entry4.get()
            source = entry5.get()
            remarks = entry3.get()
            credit_account = entry1.get()
            category = entry2.get()
            
            if not all([amount, date, source, credit_account, category]):
                tk.messagebox.showerror("Error", "All fields except maybe remarks are required")
                return
            
            if not remarks:
                remarks = None
            
            if not addrevenue.is_valid_amount(amount):
                tk.messagebox.showerror("Error", "Invalid amount")
                return
            
            if not addrevenue.is_valid_date(date):
                tk.messagebox.showerror("Error", "Invalid date")
                return
            
            if not addrevenue.is_valid_source(source):
                tk.messagebox.showerror("Error", "Invalid source")
                return
            
            if not addrevenue.is_valid_credit_account(credit_account):
                tk.messagebox.showerror("Error", "Invalid credit account")
                return
            
            if not addrevenue.is_valid_category(category):
                tk.messagebox.showerror("Error", "Invalid category")
                return
            
            if addrevenue.insert_income(amount, date, source, remarks, credit_account, category):
                tk.messagebox.showinfo(
                    "Success", "Revenue added successfully!")
                clear_entry_fields()
                controller.show_frame("myrevenues")
            else:
                tk.messagebox.showerror(
                    "Error", "Failed to add account. Please try again.")
                clear_entry_fields()
            
        img0 = tk.PhotoImage(file=path + "addrevenue7.png")
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
            controller.show_frame("myrevenues")

        img1 = tk.PhotoImage(file=path + "addrevenue8.png")

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
