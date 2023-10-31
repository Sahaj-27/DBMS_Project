import random
import tkinter as tk
import sys
import mysql.connector
import yfinance as yf
import matplotlib.pyplot as plt


from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mysql.connector import Error
from tkinter import messagebox
from pathlib import Path
from tkinter import ttk
from datetime import datetime, timedelta


path2 = "A:\\Final_Project\\"


path = "A:\\Final_Project\\buystocks_page\\"


class buystocks (tk.Frame):
    
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
    
    def get_current_price(symbol):
        stock_info = yf.Ticker(symbol)
        stock_data = stock_info.history(period="1d")
        return stock_data['Close'][0]
    
    def generate_unique_number():
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="Personal_Finance_Management"
        )

        if connection.is_connected():
            cursor = connection.cursor()
            query = "SELECT user_id FROM Investment"
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

    def get_number_of_units(amount, price):
        return amount / price
    
    def is_valid_amount(amount):
        if not amount.isdigit():
            return False
        return True
    
    def is_valid_invest_account(invest_account):

        if not invest_account.isdigit():
            return False

        elif len(invest_account) not in [8, 12]:
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
                    query = "SELECT account_id FROM Account WHERE account_id = %s and user_id = %s"
                    cursor.execute(query, (invest_account, buystocks.read_loggedin_userid()))
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
    
    def insert_investment(symbol, account, amount):
        
        try:

            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database='Personal_Finance_Management'
            )

            if connection.is_connected():
                cursor = connection.cursor()
                user_id = buystocks.read_loggedin_userid()
                investment_id = buystocks.generate_unique_number()
                account_id = account
                balance_query = f"SELECT balance FROM Account WHERE account_id = '{account_id}' AND user_id = '{user_id}'"
                cursor.execute(balance_query)
                current_balance = cursor.fetchone()[0]

                if float(current_balance) < float(amount):
                    return "insufficient_balance"

                amount = float(amount)
                
                if symbol.endswith("-USD"):
                    investment_type = "Crypto Currency"
                    
                elif symbol .startswith("^"):
                    investment_type = "Index Fund"      
                    
                else :
                    investment_type = "Stock"    
                
                try:
                    temp_current_price = buystocks.get_current_price(symbol)
                    if buystocks.get_stock_currency(symbol) == "USD":
                        temp_current_price = temp_current_price * 81.75
                    number_of_units = buystocks.get_number_of_units(
                        amount, temp_current_price)
                    current_price = temp_current_price * number_of_units
                    return_rate = 0.0

                except:
                    return "invalid_investment_name"
                
                query = f"INSERT INTO Investment (investment_id, user_id, account_id, investment_type, investment_name, purchase_date, purchase_price, current_value, return_rate, remarks, number_of_units) VALUES ('{investment_id}', '{user_id}', '{account_id}', '{investment_type}', '{symbol}', '{datetime.now()}', '{amount}', '{current_price}', '{return_rate}', 'None', '{number_of_units}')"
                cursor.execute(query)

                update_query = f"UPDATE Account SET balance = balance - {amount} WHERE account_id = '{account_id}' AND user_id = '{user_id}'"
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


    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent, bg='#093545')

        global img0, img1, img2, background_img, entry0_img, entry1_img

        def clear_plot():
            fig.clf()
            ax.clear()
            plt.clf()
            canvas.get_tk_widget().destroy()

        def clear_data():
            entry0.delete(0, tk.END)
            entry1.delete(0, tk.END)
            entry2.delete(0, tk.END)
            growth_1d_label.destroy()
            growth_1w_label.destroy()
            growth_1m_label.destroy()
            growth_1y_label.destroy()
            name_label.destroy()
            price_label.destroy()
            clear_plot()
        
        self.controller = controller

        my_canvas = tk.Canvas(self, bd=0, highlightthickness=0)

        my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        my_scrollbar = ttk.Scrollbar(
            self, orient=tk.VERTICAL, command=my_canvas.yview)
        my_scrollbar.place(x=1517, y=0, height=840, width=20)

        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(
            scrollregion=my_canvas.bbox("all")))

        temp_frame = tk.Frame(my_canvas, bg="#093545", height=1517, width=1537)

        my_canvas.create_window((0, 0), window=temp_frame, anchor="nw", width=1537, height=1517)
        
        background_img = tk.PhotoImage(file=path + "buystocks0.png")

        bck_label = tk.Label(temp_frame, image=background_img,
                          relief="flat", bg="#093545")

        bck_label.place(x=0, y=0, width=1537, height=1537)

        img0 = tk.PhotoImage(file=path + "buystocks3.png")

        def b0_clicked():
            
            try: 
                
                if entry0.get() == "":
                    messagebox.showerror("Error", "Please enter a stock symbol.")
                    return
                
                symbol = entry0.get().upper()
                
                # Retrieve the historical stock data for the last year
                end_date = datetime.now().strftime('%Y-%m-%d')
                start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
                history = yf.download(symbol, start=start_date, end=end_date)

                # Calculate the growth percentages for one day, one week, one month, and one year
                price_today = history['Close'][-1]
                price_1d_ago = history['Close'][-2]
                price_1w_ago = history['Close'][-6]
                price_1m_ago = history['Close'][-31]
                price_1y_ago = history['Close'][0]
                
                if buystocks.get_stock_currency(symbol) == 'USD':
                    price_today = price_today * 81.75
                    price_1d_ago = price_1d_ago * 81.75
                    price_1w_ago = price_1w_ago * 81.75
                    price_1m_ago = price_1m_ago * 81.75
                    price_1y_ago = price_1y_ago * 81.75
                
                growth_1d = (price_today - price_1d_ago) / price_1d_ago * 100
                growth_1w = (price_today - price_1w_ago) / price_1w_ago * 100
                growth_1m = (price_today - price_1m_ago) / price_1m_ago * 100
                growth_1y = (price_today - price_1y_ago) / price_1y_ago * 100
                
                entry2_font = ("Lexend Deca", 20)
                
                global growth_1d_label, growth_1w_label, growth_1m_label, growth_1y_label, name_label, price_label, fig, ax, canvas
                
                name_label = tk.Label(temp_frame, text=f"Token ID: {symbol}", bg="#092f40",
                                      highlightthickness=0,
                                      font=entry2_font,
                                      fg="white")
                price_label = tk.Label(temp_frame, text=f"Current Price: {price_today:.2f}/-", bg="#092f40",
                                       highlightthickness=0,
                                       font=entry2_font,
                                       fg="white")
                growth_1d_label = tk.Label(temp_frame, text=f"1 Day Change: {growth_1d:.2f}%", bg="#092f40",
                                           highlightthickness=0,
                                           font=entry2_font,
                                           fg="white")
                growth_1w_label = tk.Label(temp_frame, text=f"1 Week Change: {growth_1w:.2f}%", bg="#092f40",
                                           highlightthickness=0,
                                           font=entry2_font,
                                           fg="white")
                growth_1m_label = tk.Label(temp_frame, text=f"1 Month Change: {growth_1m:.2f}%", bg="#092f40",
                                           highlightthickness=0,
                                           font=entry2_font,
                                           fg="white")
                growth_1y_label = tk.Label(temp_frame, text=f"1 Year Change: {growth_1y:.2f}%", bg="#092f40",
                                           highlightthickness=0,
                                           font=entry2_font,
                                           fg="white")  
                
                name_label.place(x=220, y=212, width=500, height=54)
                price_label.place(x=925, y=212, width=500, height=54)
                growth_1d_label.place(x=220, y=284, width=500, height=54)
                growth_1w_label.place(x=925, y=284, width=500, height=54)
                growth_1m_label.place(x=220, y=356, width=500, height=54)
                growth_1y_label.place(x=925, y=356, width=500, height=54)
                
                # Create the matplotlib figure
                fig = plt.figure(figsize=(13.6, 7), dpi=100)
                fig.patch.set_facecolor("#092f40")
                fig.patch.set_facecolor('#092f40')
                ax = fig.add_subplot(111)
                ax.set_facecolor("#092f40")
                
                # Plot the historical stock data
                ax.plot(history.index, history['Close'], color='#39FF14')

                # Set the plot title and axis labels
                ax.set_title(f"{symbol} Historical Stock Data",
                             color="#FFFF33", fontsize=16, pad=20)
                ax.set_xlabel("Date", color="#FFFF33", fontsize=16, labelpad=20)
                ax.tick_params(axis='x', colors="#87CEEB", labelsize=14)
                ax.tick_params(axis='y', colors='#87CEEB', labelsize=14)
                
                ax.spines['bottom'].set_color('#FFFF33')
                ax.spines['top'].set_color('#FFFF33')
                ax.spines['left'].set_color('#FFFF33')
                ax.spines['right'].set_color('#FFFF33')
                
                if buystocks.get_stock_currency(symbol) == 'USD':
                    ax.set_ylabel("Price (in US Dollars)", color="#FFFF33", fontsize=16, labelpad=20)
                else:
                    ax.set_ylabel("Price (in Indian Ruppees)", color="#FFFF33", fontsize=16, labelpad=20)

                # Create the canvas to embed the plot in the GUI window
                canvas = FigureCanvasTkAgg(fig, master=temp_frame)
                canvas.draw()
                canvas.get_tk_widget().place(x=96, y=424)

                
            except Exception as e:
                messagebox.showerror("Error", "Invalid Stock Symbol") 
                print(f"Error: {e}")

        b0 = tk.Button(temp_frame,
                       image=img0,
                       borderwidth=0,
                       highlightthickness=0,
                       command=b0_clicked,
                       background="#092f40",
                       activebackground="#092f40",
                       cursor="hand2",
                       relief="flat")

        b0.place(
            x=212, y=1306,
            width=210,
            height=54)

        img1 = tk.PhotoImage(file=path + "buystocks4.png")

        def b1_clicked():
            try :
                clear_data()
                controller.show_frame("myinvestments")
            except :
                tk.messagebox.showerror("Error", "You must search for something first!")    
                return

        b1 = tk.Button(temp_frame,
                       image=img1,
                       borderwidth=0,
                       highlightthickness=0,
                       command=b1_clicked,
                       background="#092f40",
                       activebackground="#092f40",
                       cursor="hand2",
                       relief="flat")

        b1.place(
            x=636, y=1298,
            width=266,
            height=62)

        img2 = tk.PhotoImage(file=path + "buystocks5.png")

        def b2_clicked():
            
            symbol = entry0.get().upper()
            amount = entry1.get()
            account = entry2.get()
            
            if not all ([symbol, amount, account]):
                messagebox.showerror("Error", "All fields are required!")
                return
            
            if not buystocks.is_valid_invest_account(account):
                tk.messagebox.showerror("Error", "Invalid Investment Account")
                return
            
            if not buystocks.is_valid_amount(amount):
                tk.messagebox.showerror("Error", "Invalid amount")
                return
            
            result = buystocks.insert_investment(symbol, account, amount)
            
            if result == "insufficient_balance":
                tk.messagebox.showerror(
                    "Error", "Insufficient account balance")
            elif result == "invalid_investment_name":
                tk.messagebox.showerror(
                    "Error", "Invalid Investment Name or Date")
            elif result:
                tk.messagebox.showinfo(
                "Success", "Investment added successfully!, You can view it in My Investments")
                 
            else:
                tk.messagebox.showerror(
                "Error", "Failed to add account. Please try again.")
            
            
        b2 = tk.Button(temp_frame,
                       image=img2,
                       borderwidth=0,
                       highlightthickness=0,
                       command=b2_clicked,
                       background="#092f40",
                       activebackground="#092f40",
                       cursor="hand2",
                       relief="flat")

        b2.place(
            x=1136, y=1306,
            width=210,
            height=54)

        entry0_img = tk.PhotoImage(file=path + "buystocks1.png")

        entry0_label = tk.Label(temp_frame, image=entry0_img,
                                relief="flat", bg="#093A45")

        entry0_label.place(x=96, y=1207, width=441, height=54)

        entry0_font = ("Lexend Deca", 20)

        entry0 = tk.Entry(temp_frame,
                          bd=0,
                          bg="#093A45",
                          highlightthickness=0,
                          font=entry0_font,
                          fg="white")

        entry0.place(
            x=106, y=1207,
            width=421,
            height=52)

        entry1_img = tk.PhotoImage(file=path + "buystocks2.png")

        entry1_label = tk.Label(temp_frame, image=entry1_img,
                                relief="flat", bg="#093A45")

        entry1_label.place(x=1020, y=1207, width=441, height=54)

        entry1_font = ("Lexend Deca", 20)

        entry1 = tk.Entry(temp_frame,
                          bd=0,
                          bg="#093A45",
                          highlightthickness=0,
                          font=entry1_font,
                          fg="white")

        entry1.place(
            x=1030, y=1207,
            width=421,
            height=52)
        
        entry2_img = tk.PhotoImage(file=path + "buystocks2.png")

        entry2_label = tk.Label(temp_frame, image=entry2_img,
                                relief="flat", bg="#093A45")
        
        entry2_label.place(x=558, y=1207, width=441, height=54)

        entry2_font = ("Lexend Deca", 20)

        entry2 = tk.Entry(temp_frame,
                          bd=0,
                          bg="#093A45",
                          highlightthickness=0,
                          font=entry2_font,
                          fg="white")

        entry2.place(
            x=568, y=1207,
            width=421,
            height=52)
        
        