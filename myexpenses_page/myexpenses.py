import tkinter as tk
import sys
import mysql.connector


from tkinter import ttk
from pathlib import Path


path2 = "A:\\Final_Project\\"

    
path = "A:\\Final_Project\\myexpenses_page\\"


class myexpenses (tk.Frame):
    
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
        user_id = myexpenses.read_loggedin_userid()
        
        cursor.execute(
            f"SELECT expense_id, account_id, expense, category, expense_date FROM Expenditure WHERE user_id = '{user_id}' ORDER BY expense_date")

        rows = cursor.fetchall()
        
        for row in rows:
            self.tree.insert('', 'end', text=row[0], values=(row[0],
                                                             row[1], row[2], row[3], row[4]),
                             tags=('larger'))
            
        self.tree.tag_configure('larger', font=(
            'Lexend Deca', 16), background='#195d68', foreground='#ffffff')
        
        mydb.commit()
        mydb.close()

    def update_expenses(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.populate_treeview()

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent, bg='#093545')

        global img0, img1, background_img

        self.controller = controller

        background_img = tk.PhotoImage(file= path + "myexpenses0.png")

        bck_label = tk.Label(self, image=background_img,
                            relief="flat", bg="#093545")

        bck_label.place(x=0, y=0, width=1537, height=864)
        
        img0 = tk.PhotoImage(file=path + "myexpenses1.png")
        
        def b0_clicked():
            controller.show_frame("dashboard")

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
            x=478, y=620,
            width=266,
            height=62)

        img1 = tk.PhotoImage(file=path + "myexpenses2.png")

        def b1_clicked():
            controller.show_frame("addexpense")

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
            x=821, y=620,
            width=266,
            height=62)

        self.tree = ttk.Treeview(self, columns=(
            'Expense ID', 'Debit Account', 'Amount', 'Category', 'Expense Date'), show='headings')
        self.tree.place(x=134, y=215, width=1285, height=384)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure('Treeview', rowheight=35, fieldbackground="#092f40")

        style.configure('Treeview.Heading', font=('Lexend Deca', 20),
                        foreground='white', background="#092f40")

        self.tree.column('Expense ID', width=253,
                         anchor="center", minwidth=253)
        self.tree.heading('Expense ID', text='Expense ID')

        self.tree.column('Debit Account', width=253, anchor="center", minwidth=253)
        self.tree.heading('Debit Account', text='Debit Account')

        self.tree.column('Amount', width=253,
                         anchor="center", minwidth=253)
        self.tree.heading('Amount', text='Amount')

        self.tree.column('Category', width=253, anchor="center", minwidth=253)
        self.tree.heading('Category', text='Category')

        self.tree.column('Expense Date', width=253, anchor="center", minwidth=253)
        self.tree.heading('Expense Date', text='Expense Date')

        scrollbar = ttk.Scrollbar(
            self, orient='vertical', command=self.tree.yview)
        scrollbar.place(x=1399, y=216, height=382, width=20)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.populate_treeview()