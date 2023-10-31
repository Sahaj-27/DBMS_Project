import tkinter as tk
import yfinance as yf
import sys
import mysql.connector


from tkinter import ttk


path2 = "A:\\Final_Project\\"


path = "A:\\Final_Project\\myinvestments_page\\"


class myinvestments (tk.Frame):
    
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

    def populate_treeview(self):
        
        mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='Personal_Finance_Management'
        )
        
        cursor = mydb.cursor()
        user_id = myinvestments.read_loggedin_userid()
        
        cursor.execute(
            f"select investment_name from Investment where user_id = '{user_id}'")
        rows_temp = cursor.fetchall()
        
        for row in rows_temp:
            
            stock_info = yf.Ticker(row[0])
            stock_data = stock_info.history(period="1d")
            new_value = stock_data['Close'][0]
            
            if myinvestments.get_stock_currency(row[0]) == 'USD':
                new_value = new_value * 81.75

            cursor.execute(
                'UPDATE Investment SET current_value = %s * number_of_units, return_rate = (((%s * number_of_units) - purchase_price) / purchase_price) * 100 WHERE investment_name = %s',
                (float(new_value), float(new_value), row[0])
            )
        
        cursor.execute(
            f"SELECT investment_id, account_id, investment_type, investment_name, purchase_date, purchase_price, current_value, return_rate, number_of_units FROM Investment WHERE user_id = '{user_id}' ORDER BY purchase_date")

        rows = cursor.fetchall()
        
        for row in rows:
            self.tree.insert('', 'end', text=row[0], values=(row[0],
                                                             row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]),
                             tags=('larger'))
            
        self.tree.tag_configure('larger', font=(
            'Lexend Deca', 14), background='#195d68', foreground='#ffffff')

        mydb.commit()
        mydb.close()

    def update_investments(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.populate_treeview()

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent, bg='#093545')

        global img0, img1, img2, img3, background_img

        self.controller = controller

        background_img = tk.PhotoImage(file=path + "myinvestments0.png")

        bck_label = tk.Label(self, image=background_img,
                             relief="flat", bg="#093545")

        bck_label.place(x=0, y=0, width=1537, height=864)
        
        img0 = tk.PhotoImage(file= path + "myinvestments1.png")
        
        def b0_clicked():
            controller.show_frame("dashboard")

        b0 = tk.Button(self,
                       image=img0,
                       borderwidth=0,
                       highlightthickness=0,
                       command=b0_clicked,
                       background="#26595D",
                       activebackground="#26595D",
                       cursor="hand2",
                       relief="flat")

        b0.place(
            x=163, y=622,
            width=266,
            height=62)

        img1 = tk.PhotoImage(file=path + "myinvestments2.png")
        
        def b1_clicked():
            controller.show_frame("addinvestment")
        
        b1 = tk.Button(self,
                       image=img1,
                       borderwidth=0,
                       highlightthickness=0,
                       command=b1_clicked,
                       background="#26595D",
                       activebackground="#26595D",
                       cursor="hand2",
                       relief="flat")

        b1.place(
            x=457, y=622,
            width=266,
            height=62)

        img2 = tk.PhotoImage(file=path + "myinvestments3.png")
        
        def b2_clicked():
            controller.show_frame("buystocks")
        
        b2 = tk.Button(self,
                       image=img2,
                       borderwidth=0,
                       highlightthickness=0,
                       command=b2_clicked,
                       background="#26595D",
                       activebackground="#26595D",
                       cursor="hand2",
                       relief="flat")

        b2.place(
            x=816, y=622,
            width=266,
            height=62)

        img3 = tk.PhotoImage(file=path + "myinvestments4.png")
        
        def b3_clicked():
            controller.show_frame("sellstocks")
        
        b3 = tk.Button(self,
                       image=img3,
                       borderwidth=0,
                       highlightthickness=0,
                       command=b3_clicked,
                       background="#26595D",
                       activebackground="#26595D",
                       cursor="hand2",
                       relief="flat")

        b3.place(
            x=1109, y=622,
            width=266,
            height=62)
        
        self.tree = ttk.Treeview(self, columns=(
            'INV_ID', 'INV_Account', 'Type', 'Name', 'Purchase Date', 'Purchase Price', 'Current Value', 'Return Rate', 'Units'), show='headings')
        
        self.tree.place(x=100, y=215, width=1353, height=384)

        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure('Treeview', rowheight=35, fieldbackground="#092f40")

        style.configure('Treeview.Heading', font=('Lexend Deca', 16),
                        foreground='white', background="#092f40")

        self.tree.column('INV_ID', width=95,
                         anchor="center", minwidth=95)
        
        self.tree.heading('INV_ID', text='INV_ID')

        self.tree.column('INV_Account', width=168, anchor="center", minwidth=168)
        
        self.tree.heading('INV_Account', text='INV_Account')

        self.tree.column('Type', width=168,
                         anchor="center", minwidth=168)
        
        self.tree.heading('Type', text='Type')

        self.tree.column('Name', width=168, anchor="center", minwidth=168)
        
        self.tree.heading('Name', text='Name')

        self.tree.column('Purchase Date', width=159, anchor="center", minwidth=159)
        
        self.tree.heading('Purchase Date', text='Purchase Date')
        
        self.tree.column('Purchase Price', width=165,
                         anchor="center", minwidth=165)
        
        self.tree.heading('Purchase Price', text='Purchase Price')
        
        self.tree.column('Current Value', width=154,
                         anchor="center", minwidth=154)
        
        self.tree.heading('Current Value', text='Current Value')
        
        self.tree.column('Return Rate', width=134,
                         anchor="center", minwidth=134)
        
        self.tree.heading('Return Rate', text='Return Rate')
        
        self.tree.column('Units', width=126,
                         anchor="center", minwidth=126)
        
        self.tree.heading('Units', text='Units')

        scrollbar = ttk.Scrollbar(
            self, orient='vertical', command=self.tree.yview)
        
        scrollbar.place(x=1433, y=216, height=382, width=20)
        
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.populate_treeview()
