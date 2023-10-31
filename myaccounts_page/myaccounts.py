import tkinter as tk
import sys
import mysql.connector


from pathlib import Path
from tkinter import ttk


path2 = "A:\\Final_Project\\"    
    
    
path = "A:\\Final_Project\\myaccounts_page\\"


class myaccounts (tk.Frame):
    
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
    
    def populate_treeview(self):
        
        mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='Personal_Finance_Management'
        )
        
        cursor = mydb.cursor()
        user_id = myaccounts.read_loggedin_userid()
        
        cursor.execute(f"SELECT account_id, bank_name, account_type, balance, open_date FROM Account WHERE user_id = '{user_id}' ORDER BY open_date")

        rows = cursor.fetchall()
        
        for row in rows:
            self.tree.insert('', 'end', text=row[0], values=(row[0],
                                                             row[1], row[2], row[3], row[4]),
                             tags=('larger'))
            
        self.tree.tag_configure('larger', font=(
            'Lexend Deca', 16), background='#195d68', foreground='#ffffff')
        
        mydb.commit()
        mydb.close()

    def update_accounts(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.populate_treeview()
    
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent, bg='#093545')

        global img0, img1, img2, background_img

        self.controller = controller

        background_img = tk.PhotoImage(file = path + "myaccounts0.png")

        bck_label = tk.Label(self, image=background_img,
                            relief="flat", bg="#093545")
        
        bck_label.place(x=0, y=0, width=1537, height=864)
        
        img0 = tk.PhotoImage(file=  path  + "myaccounts1.png")
        
        def b0_clicked():
            controller.show_frame("addaccount")

        b0 = tk.Button(self,
                    image=img0,
                    borderwidth=0,
                    highlightthickness=0,
                    command=b0_clicked,
                    background="#092f40",
                    activebackground="#092f40",
                    cursor="hand2",
                    relief="flat")

        b0.place(
            x=950, y=618,
            width=266,
            height=62)
        
        def b1_clicked():
            controller.show_frame("editaccount")

        img1 = tk.PhotoImage(file= path + "myaccounts2.png")

        b1 = tk.Button(self,
            image=img1,
            borderwidth=0,
            highlightthickness=0,
            command=b1_clicked,
            background="#092f40",
            activebackground="#092f40",
            cursor="hand2",
            relief="flat")

        b1.place(
            x=644, y=618,
            width=266,
            height=62)
        
        def b3_clicked():
            controller.show_frame("dashboard")

        img2 = tk.PhotoImage(file= path + "myaccounts3.png")
        
        b2 = tk.Button(self,
            image=img2,
            borderwidth=0,
            highlightthickness=0,
            command=b3_clicked,
            background="#092f40",
            activebackground="#092f40",
            cursor="hand2",
            relief="flat")

        b2.place(
            x=338, y=618,
            width=266,
            height=62)
        
        self.tree = ttk.Treeview(self, columns=(
            'Account Number', 'Bank Name', 'Account Type', 'Balance', 'Open Date'), show='headings')
        
        self.tree.place(x=134, y=215, width=1285, height=384)
        
        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure('Treeview', rowheight=35, fieldbackground="#092f40")

        style.configure('Treeview.Heading', font=('Lexend Deca', 20),
                        foreground='white', background="#092f40")
        
        self.tree.column('Account Number', width=253, anchor="center", minwidth= 253)
        self.tree.heading('Account Number', text='Account Number')
        
        self.tree.column('Bank Name', width=253, anchor="center", minwidth= 253)   
        self.tree.heading('Bank Name', text='Bank Name')
        
        self.tree.column('Account Type', width=253, anchor="center", minwidth= 253)
        self.tree.heading('Account Type', text='Account Type')
        
        self.tree.column('Balance', width=253, anchor="center", minwidth= 253)
        self.tree.heading('Balance', text='Balance')
        
        self.tree.column('Open Date', width=253, anchor="center", minwidth= 253)
        self.tree.heading('Open Date', text='Open Date')
        
        scrollbar = ttk.Scrollbar(
            self, orient='vertical', command=self.tree.yview)
        scrollbar.place(x=1399, y=216, height=382, width=20)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.populate_treeview()
        