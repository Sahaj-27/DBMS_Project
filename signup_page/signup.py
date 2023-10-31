import tkinter as tk
import tkinter.messagebox
import mysql.connector
import re
import random


from email_validator import validate_email, EmailNotValidError
from datetime import datetime
from mysql.connector import Error


path = "A:\\Final_Project\\signup_page\\"


class signup(tk.Frame):
    
    def is_valid_name(name):
        return all(char.isalpha() or char.isspace() for char in name)
    
    def is_valid_date(date_str):
        try:
            input_date = datetime.strptime(date_str, '%d-%m-%Y')
            current_date = datetime.now()
            if input_date > current_date:
                return False
            return True
        except ValueError:
            return False

    def is_valid_mobile_number(mobile_number):
        if len(mobile_number) == 10 and mobile_number.isdigit():
            return True
        else:
            return False

    def is_valid_email(email):
        try:
            valid = validate_email(email)
            return True
        except EmailNotValidError as e:
            return False

    def generate_unique_number():
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="Personal_Finance_Management"
        )

        if connection.is_connected():
            cursor = connection.cursor()
            query = "SELECT user_id FROM User"
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
            
    def check_username(username):
        
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="Personal_Finance_Management"
            )
            if connection.is_connected():
                cursor = connection.cursor()
                query = "SELECT username FROM User WHERE BINARY username = %s"
                cursor.execute(query, (username,))
                if cursor.fetchone() or " " in username or len(username) < 5 or len(username) > 20 :
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
                
    def check_email(email):

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="Personal_Finance_Management"
            )
            if connection.is_connected():
                cursor = connection.cursor()
                query = "SELECT email FROM User WHERE BINARY email = %s"
                cursor.execute(query, (email,))
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

    def insert_user(username, password, name, dob, mobile_number, email):

        try:
            
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="Personal_Finance_Management"
            )
            
            if connection.is_connected():
                cursor = connection.cursor()
                query2 = "SELECT CURDATE();"
                cursor.execute(query2)
                registered_date = cursor.fetchone()[0] 
                dob_datetime = datetime.strptime(dob, '%d-%m-%Y')
                dob_mysql_format = dob_datetime.strftime('%Y-%m-%d')
                query = "INSERT INTO User (user_id, username, password, name, registered_date, dob, mobile_number, email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(query, (signup.generate_unique_number(
                ), username, password, name, registered_date, dob_mysql_format, mobile_number, email))
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
        
        global img0, entry0_img, entry1_img, entry2_img, entry3_img, entry4_img, entry5_img, background_img
        
        def clear_entry_fields():
            entry0.delete(0, tk.END)
            entry1.delete(0, tk.END)
            entry2.delete(0, tk.END)
            entry3.delete(0, tk.END)
            entry4.delete(0, tk.END)
            entry5.delete(0, tk.END)

        self.controller = controller
        
        background_img = tk.PhotoImage(file=path + "signup7.png")

        bck_label = tk.Label(self, image=background_img,
                             relief="flat", bg="#093545")

        bck_label.place(x=0, y=-207, width=1794.63, height=1071)

        entry0_img = tk.PhotoImage(file=path + "signup1.png")

        entry0_label = tk.Label(self, image=entry0_img,
                                relief="flat", bg="#093545")
        
        entry0_label.place(x=141, y=217, width=481, height=62)

        entry0_font = ("Lexend Deca", 20)

        entry0 = tk.Entry(self,
            bd=0,
            bg="#224957",
            highlightthickness=0,
            font=entry0_font,
            fg="white")

        entry0.place(
            x=151.0, y=217,
            width=461.0,
            height=60)

        entry1_img = tk.PhotoImage(file=path + "signup2.png")

        entry1_label = tk.Label(self, image=entry1_img,
                                relief="flat", bg="#093545")
        
        entry1_label.place(x=141, y=341, width=481, height=62)

        entry1_font = ("Lexend Deca", 20)

        entry1 = tk.Entry(self,
            bd=0,
            bg="#224957",
            highlightthickness=0,
            font=entry1_font,
            fg="white")

        entry1.place(
            x=151.0, y=341,
            width=461.0,
            height=60)

        entry2_img = tk.PhotoImage(file=path + "signup3.png")

        entry2_label = tk.Label(self, image=entry2_img,
                                relief="flat", bg="#093545")
        
        entry2_label.place(x=141, y=468, width=481, height=62)

        entry2_font = ("Lexend Deca", 20)

        entry2 = tk.Entry(self,
            bd=0,
            bg="#224957",
            highlightthickness=0,
            font=entry2_font,
            show="*",
            fg="white")

        entry2.place(
            x=151.0, y=468,
            width=461.0,
            height=60)

        entry3_img = tk.PhotoImage(file=path + "signup4.png")

        entry3_label = tk.Label(self, image=entry3_img,
                                relief="flat", bg="#093545")
        
        entry3_label.place(x=807, y=217, width=481, height=62)

        entry3_font = ("Lexend Deca", 20)

        entry3 = tk.Entry(self,
            bd=0,
            bg="#224957",
            highlightthickness=0,
            font=entry3_font,
            fg="white")

        entry3.place(
            x=817.0, y=217,
            width=461.0,
            height=60)

        entry4_img = tk.PhotoImage(file=path + "signup5.png")

        entry4_label = tk.Label(self, image=entry4_img,
                                relief="flat", bg="#093545")
        
        entry4_label.place(x=807, y=341, width=481, height=62)

        entry4_font = ("Lexend Deca", 20)

        entry4 = tk.Entry(self,
            bd=0,
            bg="#224957",
            highlightthickness=0,
            font=entry4_font,
            fg="white")

        entry4.place(
            x=817.0, y=341,
            width=461.0,
            height=60)

        entry5_img = tk.PhotoImage(file=path + "signup6.png")

        entry5_label = tk.Label(self, image=entry5_img,
                                relief="flat", bg="#093545")
        
        entry5_label.place(x=807, y=465, width=481, height=62)

        entry5 = tk.Entry(self,
            bd=0,
            bg="#224957",
            highlightthickness=0,
            font=("Lexend Deca", 20),
            fg="white")

        entry5.place(
            x=817.0, y=465,
            width=461.0,
            height=60)

        label_text = "Already have an Account? "
        link_text = "Click Here!"

        label = tk.Label(self, text=label_text, bg=self.cget(
            'bg'), fg="white", font=("Lexend Deca", 15))
        label.pack()

        link = tk.Label(self, text=link_text, fg="#20DF7F", cursor="hand2",
                        bg=self.cget('bg'), font=("Lexend Deca", 15))
        link.pack()

        def login():
            clear_entry_fields()
            controller.show_frame("login")

        link.bind("<Button-1>", lambda event: login())

        label.place(x=555, y=680)
        link.place(x=555+232, y=680)
        
        img0 = tk.PhotoImage(file=path + "signup0.png")
        
        def btn_clicked():

            name = entry3.get()
            dob = entry4.get()
            mobile_number = entry5.get()
            email = entry0.get()
            username = entry1.get()
            password = entry2.get()

            if not all([name, email, username, password, dob, mobile_number]):
                tk.messagebox.showerror(
                    "Error", "Please fill in all the fields.")
                return
            
            if not signup.check_username(username):
                tk.messagebox.showerror(
                    "Error", "Invalid Username. Please try again.")
                return
            
            if not signup.check_email(email):
                tk.messagebox.showerror(
                    "Error", "Email already exists. Please try again.")
                return

            if not signup.is_valid_name(name):
                tk.messagebox.showerror(
                    "Error", "Name must contain only alphabets.")
                return
            
            if not signup.is_valid_date(dob):
                tk.messagebox.showerror(
                    "Error", "Invalid date of birth.")
                return
            
            if not signup.is_valid_email(email):
                tk.messagebox.showerror("Error", "Invalid email address.")
                return
            
            if not signup.is_valid_mobile_number(mobile_number):
                tk.messagebox.showerror("Error", "Invalid mobile number.")
                return

            password_regex = re.compile(
                r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$'
            )

            if not password_regex.match(password):
                tk.messagebox.showerror(
                    "Error",
                    "Password must be at least 8 characters long, with at least one uppercase letter, one lowercase letter, one digit, and one special character (!@#$%^&*)."
                )
                return

            if signup.insert_user(username, password, name, dob, mobile_number, email):
                tk.messagebox.showinfo(
                    "Success", "Account created successfully!")
                clear_entry_fields()
                controller.show_frame("login")
            else:
                tk.messagebox.showerror(
                    "Error", "Failed to create account. Please try again.")
                clear_entry_fields()

        b0 = tk.Button(self,
                       image=img0,
                       borderwidth=0,
                       highlightthickness=0,
                       command=btn_clicked,
                       relief="flat", cursor="hand2")

        b0.place(
            x=591, y=595,
            width=266,
            height=62)