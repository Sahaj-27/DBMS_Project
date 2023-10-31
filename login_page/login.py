import tkinter as tk
import ctypes 
import mysql.connector
import tkinter.messagebox


from mysql.connector import Error


path = "A:\\Final_Project\\login_page\\"


class login(tk.Frame):
    
    def check_credentials(username, password):
            
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database = "Personal_Finance_Management"
            )
            cursor = connection.cursor()
            query = "SELECT user_id FROM User WHERE BINARY username = %s AND BINARY password = %s"
            cursor.execute(query, (username, password))
            result = cursor.fetchall()   
            if result :
                loggedin_userid = result[0][0]   
                return loggedin_userid
            else :
                return None

        except Error as e:
            print(f"Error: {e}")
            return False

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()            
                    
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent, bg='#093545')
        self.controller = controller

        global img0, entry0_img, entry1_img, background_img
        
        def clear_entry_fields():
            entry0.delete(0, tk.END)
            entry1.delete(0, tk.END)

        def set_title_bar_color(color):
            hwnd = ctypes.windll.user32.GetForegroundWindow()
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd, 20, ctypes.byref(ctypes.c_ulong(color)), 4)

        self.controller.state("zoomed")
        self.controller.geometry("1537x864")
        self.controller.resizable(False, False)
        self.controller.iconphoto(
            False, tk.PhotoImage(file=path + "icon.png"))
        self.controller.title("Personal Finance Management")

        set_title_bar_color(0x0000FF)

        img0 = tk.PhotoImage(file=path + "login0.png")

        background_img = tk.PhotoImage(file=path + "login3.png")

        bck_label = tk.Label(self, image=background_img,
                             relief="flat", bg="#093545")
        
        bck_label.place(x=0, y=0, width=1537, height=864)

        entry0_img = tk.PhotoImage(file=path + "login1.png")

        entry0_label = tk.Label(self, image=entry0_img,
                                relief="flat", bg="#093545")
        
        entry0_label.place(x=77, y=432, width=481, height=62)

        entry0 = tk.Entry(self, show="*",
                          bd=0,
                          bg="#224957",
                          highlightthickness=0,
                          fg="white",
                          font=("Lexend Deca", 20)
                          )

        entry0.place(
            x=87.0, y=432,
            width=461.0,
            height=60)

        entry1_img = tk.PhotoImage(file=path + "login2.png")

        entry1_label = tk.Label(self, image=entry1_img,
                                relief="flat", bg="#093545")
        
        entry1_label.place(x=77, y=298, width=481, height=62)

        entry1 = tk.Entry(self,
                          bd=0,
                          bg="#224957",
                          highlightthickness=0,
                          fg="white",
                          font=("Lexend Deca", 20),
                          )

        entry1.place(
            x=87.0, y=298,
            width=461.0,
            height=60)

        label_text = "Don't have an Account? "
        link_text = "Click Here!"

        label = tk.Label(self, text=label_text, bg=self.cget(
            'bg'), fg="white", font=("Lexend Deca", 15))
        label.pack()

        link = tk.Label(self, text=link_text, fg="#20DF7F", cursor="hand2",
                        bg=self.cget('bg'), font=("Lexend Deca", 15))
        link.pack()

        def register():
            clear_entry_fields()
            controller.show_frame("signup")

        link.bind("<Button-1>", lambda event: register())

        label.place(x=160, y=650)
        link.place(x=160+210, y=650)

        def btn_clicked():

            username = entry1.get()
            password = entry0.get()

            if not username or not password:
                tk.messagebox.showerror(
                    "Error", "Please enter both username and password.")
                return

            loggedin_userid = login.check_credentials(username, password)
            
            if loggedin_userid is not None:
                tk.messagebox.showinfo("Success", "Logged In successfully!")
                with open('user_id.txt', 'w') as f:
                    f.write(str(loggedin_userid))
                clear_entry_fields()
                controller.show_frame("dashboard")
                
            else:
                tk.messagebox.showerror(
                    "Error", "Incorrect username or password.")
                clear_entry_fields()

        b0 = tk.Button(self,
                       image=img0,
                       command=btn_clicked,
                       relief="flat", cursor="hand2")

        b0.place(
            x=77, y=566,
            width=481,
            height=60)   
        
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root"
            )
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute("CREATE DATABASE IF NOT EXISTS Personal_Finance_Management")
                connection.database = 'Personal_Finance_Management'
                with open(path + 'login.sql') as f:
                    queries = f.read().split(';\n\n')
                for query in queries:
                    cursor.execute(query)
                connection.commit()

        except Error as e:
            print(f"Error: {e}")
            return None

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
