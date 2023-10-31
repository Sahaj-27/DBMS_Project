import tkinter as tk

 
from login_page.login import login
from signup_page.signup import signup
from addaccount_page.addaccount import addaccount
from addrevenue_page.addrevenue import addrevenue
from addexpense_page.addexpense import addexpense
from addinvestment_page.addinvestment import addinvestment
from myaccounts_page.myaccounts import myaccounts
from myexpenses_page.myexpenses import myexpenses
from myrevenues_page.myrevenues import myrevenues
from myinvestments_page.myinvestments import myinvestments
from dashboard_page.dashboard import dashboard
from buystocks_page.buystocks import buystocks
from sellstocks_page.sellstocks import sellstocks
from editaccount_page.editaccount import editaccount



class App(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        

        for F in (login, signup, dashboard, myaccounts, addaccount, editaccount, myrevenues, addrevenue, myexpenses, addexpense, myinvestments, addinvestment, buystocks, sellstocks):
            page_name = F.__name__
            frame = F(parent = container, controller = self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.show_frame("login")

    def show_frame(self, page_name):
            frame = self.frames[page_name]
            if page_name == "myaccounts":
                frame.update_accounts()
            if page_name == "myexpenses":
                frame.update_expenses()  
            if page_name == "myrevenues":
                frame.update_revenues()   
            if page_name == "myinvestments":
                frame.update_investments()   
            if page_name == "dashboard":
                frame.update_dashboard()          
            frame.tkraise()

        
if __name__ == "__main__":
    Application = App()
    Application.mainloop()