import tkinter as tk
import re
import mysql.connector
import sys


from tkinter import messagebox
from pathlib import Path
from mysql.connector import Error


path2 = "A:\\Final_Project\\"


path = "A:\\Final_Project\\addaccount_page\\"


class addaccount(tk.Frame):
    
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

    def check_account_number(account_number):

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="Personal_Finance_Management"
            )
            if connection.is_connected():
                cursor = connection.cursor()
                query = "SELECT account_id FROM Account WHERE account_id = %s"
                cursor.execute(query, (account_number,))
                if cursor.fetchone():
                    return False
                else:
                    return True

        except Error as e:
            print(f"Error: {e}")
            return False

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def insert_account(bank_name, ifsc_code, account_type, current_balance, account_number, nominee_name, interest_rate):
        
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database='Personal_Finance_Management'
            )

            if connection.is_connected():
                cursor = connection.cursor()
                user_id = addaccount.read_loggedin_userid()
                query2 = "SELECT CURDATE();"
                cursor.execute(query2)
                open_date = cursor.fetchone()[0]
                query = f"INSERT INTO Account (bank_name, ifsc_code, user_id, account_type, balance, account_id, nominee_name, open_date, interest_rate) VALUES ('{bank_name}', '{ifsc_code}', '{user_id}', '{account_type}', '{current_balance}', '{account_number}', '{nominee_name}', '{open_date}', '{interest_rate}')"
                cursor.execute(query)
                connection.commit()
                return True

        except Error as e:
            print("Error while connecting to MySQL", e)
            return False

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()

    def validate_current_balance(current_balance):
        if not current_balance.isdigit():
            return False
        return True

    def validate_ifsc_code(ifsc_code):
        if not re.match(r'^[A-Z]{4}0\d{6}$', ifsc_code):
            return False
        return True

    def validate_account_number(account_number):
        if not account_number.isdigit():
            return False
        elif len(account_number) not in [8, 12]:
            return False
        return True

    def validate_nominee_name(nominee_name):
        return all(char.isalpha() or char.isspace() for char in nominee_name)

    def is_valid_bank(bank_name):
        return all(char.isalpha() or char.isspace() for char in bank_name)

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

        background_img = tk.PhotoImage(file=path + "addaccount0.png")

        bck_label = tk.Label(self, image=background_img,
                             relief="flat", bg="#093545")

        bck_label.place(x=0, y=0, width=1537, height=864)

        entry0_img = tk.PhotoImage(file=path + "addaccount1.png")

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

        entry1_img = tk.PhotoImage(file=path + "addaccount2.png")

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

        entry2_img = tk.PhotoImage(file=path + "addaccount3.png")

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

        entry3_img = tk.PhotoImage(file=path + "addaccount4.png")

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

        entry4_img = tk.PhotoImage(file=path + "addaccount5.png")

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

        entry5_img = tk.PhotoImage(file=path + "addaccount6.png")

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

            bank_name = entry0.get()
            account_number = entry1.get()
            ifsc_code = entry4.get()
            nominee_name = entry2.get()
            current_balance = entry3.get()
            account_type = entry5.get()
            interest_rate = 0.0

            if (account_type == "Saving Account"):
                interest_rate = 3.5
            elif (account_type == "Salary Account"):
                interest_rate = 3.0
            elif (account_type == "Current Account"):
                interest_rate = 0.0
            else:
                tk.messagebox.showerror("Error", "Invalid Account Type")
                return

            if not all([bank_name, account_number, ifsc_code, nominee_name, current_balance, account_type]):
                tk.messagebox.showerror("Error", "Please fill all the fields")
                return

            if not addaccount.validate_account_number(account_number):
                tk.messagebox.showerror("Error", "Invalid Account Number")
                return

            if not addaccount.validate_ifsc_code(ifsc_code):
                tk.messagebox.showerror("Error", "Invalid IFSC Code")
                return

            if not addaccount.validate_current_balance(current_balance):
                tk.messagebox.showerror("Error", "Invalid Current Balance")
                return

            if not addaccount.is_valid_bank(bank_name):
                tk.messagebox.showerror("Error", "Invalid Bank Name")
                return

            if not addaccount.validate_nominee_name(nominee_name):
                tk.messagebox.showerror("Error", "Invalid Nominee Name")
                return

            if not addaccount.check_account_number(account_number):
                tk.messagebox.showerror("Error", "Account already exists")
                return

            if addaccount.insert_account(bank_name, ifsc_code, account_type, current_balance, account_number, nominee_name, interest_rate):
                tk.messagebox.showinfo(
                    "Success", "Account added successfully!")
                clear_entry_fields()
                controller.show_frame("myaccounts")
            else:
                tk.messagebox.showerror(
                    "Error", "Failed to add account. Please try again.")
                clear_entry_fields()

        img0 = tk.PhotoImage(file=path + "addaccount7.png")
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
            controller.show_frame("myaccounts")

        img1 = tk.PhotoImage(file=path + "addaccount8.png")

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
