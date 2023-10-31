import tkinter as tk
import mysql.connector


from tkinter import ttk


path2 = "A:\\Final_Project\\"


path = "A:\\Final_Project\\dashboard_page\\"


class dashboard(tk.Frame):
 
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
    
    def display_info(self) :
        
        mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='Personal_Finance_Management'
        )

        cursor = mydb.cursor()
        user_id = dashboard.read_loggedin_userid()
        
        cursor.execute(f"SELECT SUM(balance) FROM Account WHERE user_id = '{user_id}'")
        
        row = cursor.fetchone()
        
        if row[0] == None:
            label_text = 0.00
        else :    
            label_text = row[0]
            
        label_temp = tk.Label(self, text=label_text, bg = '#010011', fg="white", font=("Lexend Deca", 20))
        label_temp.place(x=500, y=450, width=400)
        
        with open(path + 'dashboard.sql', 'r') as file:
            query2 = file.read()

        query2 = query2.format(user_id=user_id)

        cursor.execute(query2)

        rows = cursor.fetchall()

        for row in rows:   
            self.tree.insert('', 'end', text=row, values = (row), tags=('larger'))
        self.tree.tag_configure('larger', font=(
            'Lexend Deca', 16), background='#114048', foreground='#ffffff')
        mydb.commit()
        mydb.close()
        
    def update_dashboard(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        self.display_info()

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent, bg='#093545')

        global img0, img1, img2, img3, img4, background_img

        self.controller = controller
        
        background_img = tk.PhotoImage(file=path + "dashboard0.png")

        bck_label = tk.Label(self, image=background_img,
                             relief="flat", bg="#093545")

        bck_label.place(x=0, y=0, width=1537, height=864)
        
        img0 = tk.PhotoImage(file= path + "dashboard1.png")
        
        def b0_clicked():
            controller.show_frame("login")

        b0 = tk.Button(self,
                    image=img0,
                    borderwidth=0,
                    highlightthickness=0,
                    command=b0_clicked,
                    bg="#194b4d",
                    background="#194b4d",
                    activebackground="#194b4d",
                    cursor="hand2",
                    relief="flat")

        b0.place(
            x=0, y=764,
            width=383,
            height=80)

        img1 = tk.PhotoImage(file=path + "dashboard2.png")
        
        def b1_clicked():
            controller.show_frame("myinvestments")
        
        b1 = tk.Button(self,
                    image=img1,
                    borderwidth=0,
                    highlightthickness=0,
                    command=b1_clicked,
                    bg="#194b4d",
                    background="#194b4d",
                    activebackground="#194b4d",
                    cursor="hand2",
                    relief="flat")

        b1.place(
            x=49, y=344,
            width=290,
            height=49)

        img2 = tk.PhotoImage(file= path + "dashboard3.png")
        
        def b2_clicked():
            controller.show_frame("myexpenses")
        
        b2 = tk.Button(self,
                    image=img2,
                    borderwidth=0,
                    highlightthickness=0,
                    command=b2_clicked,
                    bg="#194b4d",
                    background="#194b4d",
                    activebackground="#194b4d",
                    cursor="hand2",
                    relief="flat")

        b2.place(
            x=49, y=245,
            width=290,
            height=49)

        img3 = tk.PhotoImage(file=path + "dashboard4.png")
        
        def b3_clicked():
            controller.show_frame("myrevenues")
        
        b3 = tk.Button(self,
                    image=img3,
                    borderwidth=0,
                    highlightthickness=0,
                    command=b3_clicked,
                    bg="#194b4d",
                    background="#194b4d",
                    activebackground="#194b4d",
                    cursor="hand2",
                    relief="flat")

        b3.place(
            x=49, y=146,
            width=290,
            height=49)

        img4 = tk.PhotoImage(file= path + "dashboard5.png")
        
        def b4_clicked():
            controller.show_frame("myaccounts")
        
        b4 = tk.Button(self,
                    image=img4,
                    borderwidth=0,
                    highlightthickness=0,
                    command=b4_clicked,
                    bg="#194b4d",
                    background="#194b4d",
                    activebackground="#194b4d",
                    cursor="hand2",
                    relief="flat")

        b4.place(
            x=45, y=46,
            width=294,
            height=50)
        
        self.tree = ttk.Treeview(self, columns=(
            'Details'), show='headings')

        self.tree.place(x=1079, y=253, width=410, height=358)

        style = ttk.Style()
        style.theme_use("clam")

        style.configure('Treeview', rowheight=35, fieldbackground="#092f40")

        style.configure('Treeview.Heading', font=('Lexend Deca', 20),
                        foreground='white', background="#092f40")

        self.tree.column('Details', width=405,
                         anchor="center", minwidth=405, stretch=False)

        self.tree.heading('Details', text='Information')
        
        self.display_info()