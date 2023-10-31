import random
import tkinter as tk
import mysql.connector
import sys


from pathlib import Path
from datetime import datetime
from mysql.connector import Error
from tkinter import messagebox


path2 = "A:\\Final_Project\\"


path = "A:\\Final_Project\\editaccount_page\\"


class editaccount(tk.Frame):
    
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
    
    def is_valid_old_account(old_account, nominee_name):

        if not old_account.isdigit():
            return False

        elif len(old_account) not in [8, 12]:
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
                    loggedin_userid = editaccount.read_loggedin_userid()
                    query = f"SELECT account_id FROM Account WHERE account_id = '{old_account}' and user_id = '{loggedin_userid}'"
                    row  = cursor.execute(query)
                    if cursor.fetchall():
                        query2 = f"UPDATE Account SET nominee_name = '{nominee_name}' WHERE account_id = '{old_account}'"
                        cursor.execute(query2)
                        connection.commit()
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
                    
    def is_valid_new_account(old_account, new_account):

        if not new_account.isdigit():
            return False

        elif len(old_account) not in [8, 12]:
            return False
        
        if not old_account.isdigit():
            return False
        
        if len(new_account) not in [8, 12]:
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
                    loggedin_userid = editaccount.read_loggedin_userid()
                    query = f"SELECT balance FROM Account WHERE account_id = '{old_account}' and user_id = '{loggedin_userid}'"
                    cursor.execute(query)
                    row = cursor.fetchall()
                    query0 = "SELECT account_id FROM Account WHERE account_id = %s and user_id = %s"
                    cursor.execute(query0, (new_account, loggedin_userid))
                    row0 = cursor.fetchall()
                    
                    if row and row0 is not None:
                        q = f"delete from Income where account_id = '{old_account}'"
                        cursor.execute(q)
                        q1 = f"delete from Expenditure where account_id = '{old_account}'"
                        cursor.execute(q1)
                        q2 = f"Update Investment set account_id = '{new_account}' where account_id = '{old_account}'"
                        cursor.execute(q2)
                        query2 = f"delete from Account where account_id = '{old_account}'"
                        cursor.execute(query2)
                        query3 = f"UPDATE Account SET balance = balance + '{row[0][0]}' WHERE account_id = '{new_account}'"
                        cursor.execute(query3)
                        connection.commit()
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

    
    def validate_nominee_name(nominee_name):
        return all(char.isalpha() or char.isspace() for char in nominee_name)
    
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent, bg='#093545')

        global img0, img1, background_img

        def clear_entry_fields():
            entry0.delete(0, tk.END)
            entry1.delete(0, tk.END)
            entry2.delete(0, tk.END)
            entry3.delete(0, tk.END)

        self.controller = controller
        
        background_img = tk.PhotoImage(file=path + "editaccount0.png")

        bck_label = tk.Label(self, image=background_img,
                             relief="flat", bg="#093545")

        bck_label.place(x=0, y=0, width=1537, height=864)
        
        entry0_font = ("Lexend Deca", 20)

        entry0 = tk.Entry(self,
                          bd=0,
                          bg="#093A45",
                          highlightthickness=0,
                          font=entry0_font,
                          fg="white")

        entry0.place(x=305, y=373,
                     width=401,
                     height=52)
        
        entry1_font = ("Lexend Deca", 20)

        entry1 = tk.Entry(self,
                          bd=0,
                          bg="#093A45",
                          highlightthickness=0,
                          font=entry1_font,
                          fg="white")

        entry1.place(
            x=305, y=491,
            width=401,
            height=52)
        
        entry2_font = ("Lexend Deca", 20)

        entry2 = tk.Entry(self,
                          bd=0,
                          bg="#093A45",
                          highlightthickness=0,
                          font=entry2_font,
                          fg="white")

        entry2.place(
            x=1015, y=373,
            width=401,
            height=52)
        
        entry3_font = ("Lexend Deca", 20)

        entry3 = tk.Entry(self,
                          bd=0,
                          bg="#093A45",
                          highlightthickness=0,
                          font=entry3_font,
                          fg="white")

        entry3.place(
            x=1015, y=491,
            width=401,
            height=52)
        
        def b0_clicked():
            
            old_account_nom = entry0.get()
            nominee_name = entry1.get()
            old_account_del = entry2.get()
            new_account = entry3.get()
            
            if editaccount.validate_nominee_name(nominee_name) == False:
                tk.messagebox.showerror("Error", "Invalid Nominee Name")
                return
            
            if all ([old_account_nom, nominee_name]) and not all ([old_account_del, new_account]):
                result = editaccount.is_valid_old_account(old_account_nom, nominee_name)
                if result :
                    tk.messagebox.showinfo("Success", "Nominee name changed successfully")
                    clear_entry_fields()
                    controller.show_frame("myaccounts")
                else :
                    tk.messagebox.showerror("Error", "Invalid Account ID")
                    clear_entry_fields()    
                    
            elif all ([old_account_del, new_account]) and not all ([old_account_nom, nominee_name]):
                result = editaccount.is_valid_new_account(old_account_del, new_account)
                if result :
                    tk.messagebox.showinfo("Success", "Account deleted successfully")
                    clear_entry_fields()
                    controller.show_frame("myaccounts")
                else :
                    tk.messagebox.showerror("Error", "Invalid Account ID")
                    clear_entry_fields()        
                    
            else : 
                tk.messagebox.showerror("Error", "Invalid Input")
                clear_entry_fields()        
        
        img0 = tk.PhotoImage(file=path + "editaccount1.png")
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
        
        img1 = tk.PhotoImage(file=path + "editaccount2.png")

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
