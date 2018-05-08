# application.py - House of June application
#
# This program is for House of June's inventory and expenses
# management.

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mbox
from tkinter import scrolledtext
import os
import csv
import sqlite3
from datetime import date
from tkcalendar import Calendar, DateEntry
from PIL import Image, ImageTk

# Main window of application
class MainWindow(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self,master)
        # set the title and position of the window
        self.master.title("House of June")
        self.master.geometry("+100+100")
        self.master.resizable(0,0)
        self.pack(fill='both', expand=True, padx=5, pady=5)
        self.iconlocation = os.getcwd() + "/hoj.ico"
        try:
            self.master.iconbitmap(self.iconlocation)
        except:
            pass

        # Initialize the database
        database = sqlite3.connect('hojdb.db')
        cur = database.cursor()

        # Create the menu bar for the main window
        self.menubar = tk.Menu(self)
        self.master.config(menu=self.menubar)

        # Create the File menu, Options menu, Help menu
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        self.optionmenu = tk.Menu(self.menubar, tearoff=0)

        # Add the menu items to the Menu bar
        self.menubar.add_cascade(label='File', menu=self.filemenu)
        self.menubar.add_cascade(label='Options', menu=self.optionmenu)
        self.menubar.add_cascade(label='Help', menu=self.helpmenu)

        self.filemenu.add_command(label='Quit', command=self.allmenucommands)
        self.helpmenu.add_command(label='About', command=self.allmenucommands)
        self.optionmenu.add_command(label='My Options', command=self.allmenucommands)

        # Create the three buttons, Take Stock Record,  Create Expense & Record Sales
        self.btn_takeStock = ttk.Button(self, text='Take Stock Record', command=self.stocknsearchCmd)
        self.btn_takeStock.grid(column=0, row=0, padx=10, pady=10, sticky=tk.W)
        self.btn_createExpense = ttk.Button(self, text='Create Expense Record', command=self.expenseCmd)
        self.btn_createExpense.grid(column=1, row=0, padx=10, pady=10, sticky=tk.E)
        self.btn_recordSales = ttk.Button(self, text='Create Sales Record', command=self.recordSalesCmd)
        self.btn_recordSales.grid(column=2, row=0, padx=10, pady=10, sticky=tk.E)

        # Insert HoJ banner in Frame
        hojFrame1 = ttk.LabelFrame(self)
        hojFrame1.grid(column=0, row=1, pady=0, padx=0, columnspan=3)
        render = ImageTk.PhotoImage(file=r"C:\Users\ekwaoffei\PycharmProjects\Home\HoJ\application\hojbanner.jpg")
        img = tk.Label(hojFrame1, image=render)
        img.image = render
        img.grid(column=0, row=0)


    def stocknsearchCmd(self):
        # Call StocknSearch
        StocknSearch(self)

    def allmenucommands(self):
        print('test')

    def expenseCmd(self):
        # Call ExpenseFrame
        ExpenseFrame(self)

    def recordSalesCmd(self):
        recordSales(self)

# Stock and Search Frame
class StocknSearch(tk.Toplevel):

    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.title("Stock and Search")
        self.grab_set()
        self.resizable(0,0)

        # stringVar dateValue
        dateValue = 5

        # Tree line count
        treeLineCount = 0

        # icon not showing - to be fixed
        self.iconlocation = os.getcwd() + "hoj.ico"
        try:
            self.master.iconbitmap(self.iconlocation)
        except:
            pass

        # Create 2 tabs
        tabControl = ttk.Notebook(self)
        tabStockEntry = ttk.Frame(tabControl)
        tabControl.add(tabStockEntry, text='           Stock Entry            ')
        tabSearchStock = ttk.Frame(tabControl)
        tabControl.add(tabSearchStock, text='         Search Stock            ')
        tabControl.pack()

        # Working on the "Stock entry details"
        # Create LabelFrame
        stockEntryFrame = ttk.LabelFrame(tabStockEntry, text='Enter stock details')
        stockEntryFrame.grid(column=0, row=0, pady=5, padx=5)

        # Create date picker button
        btn_pickDate = ttk.Button(stockEntryFrame, text='               Pick Date             ', command=self.pickDateCmd)
        btn_pickDate.grid(column=1, row=1, pady=5, sticky=tk.E)

        # Create stock details entries
        ttk.Label(stockEntryFrame, text='Select item:').grid(column=0, row=2, pady=10, sticky=tk.W)

        # Create item combobox
        self.v_itemSelect = tk.StringVar()
        self.cmb_itemsCombo = ttk.Combobox(stockEntryFrame, textvariable=self.v_itemSelect, width=20, state='readonly')
        self.cmb_itemsCombo['values'] = ("Shoes - Heel Sandal", "Shoes - Flat shoes","Dress - Maxi","Dress - Midi","Perfume","Bag","Deodorant","Watches")
        self.cmb_itemsCombo.grid(column=1, row=2,pady=10, sticky=tk.E)
        self.cmb_itemsCombo.current(0)

        # Entry for total number of items
        self.v_itemsTotal = tk.StringVar()
        ttk.Label(stockEntryFrame, text='Quantity of items:').grid(column=0, row=3, pady=10, sticky=tk.W)
        e_itemsTotal = ttk.Entry(stockEntryFrame, textvariable=self.v_itemsTotal, width=23)
        e_itemsTotal.grid(column=1, row=3, sticky=tk.E)

        # Entry for unit cost of items
        self.v_itemsUnitCost = tk.StringVar()
        ttk.Label(stockEntryFrame, text='Unit Price:').grid(column=0, row=4,pady=10, sticky=tk.W)
        e_itemsUnitCost = ttk.Entry(stockEntryFrame, textvariable=self.v_itemsUnitCost, width=23)
        e_itemsUnitCost.grid(column=1, row=4, pady=10, sticky=tk.E)

        # Entry for total unit cost of items
        self.v_itemsTotalUnitCost = tk.StringVar()
        ttk.Label(stockEntryFrame, text='Total Price:').grid(column=0, row=5, pady=10, sticky=tk.W)
        e_itemsTotalUnitCost = ttk.Entry(stockEntryFrame, textvariable=self.v_itemsTotalUnitCost, width=23)
        e_itemsTotalUnitCost.grid(column=1, row=5, pady=10, sticky=tk.E)


        # Save button
        btn_save = ttk.Button(stockEntryFrame, text='            Save Record           ', command=self.saveRecordCmd)
        btn_save.grid(column=1, row=6, pady=10, sticky=tk.E)

        # Insert HoJ banner in Frame
        hojFrame2 = ttk.LabelFrame(stockEntryFrame)
        hojFrame2.grid(column=0, row=7, pady=0, padx=0, columnspan=2)
        render1 = ImageTk.PhotoImage(file=r"C:\Users\ekwaoffei\PycharmProjects\Home\HoJ\application\hojbanner.jpg")
        img = tk.Label(hojFrame2, image=render1)
        img.image = render1
        img.grid(column=0, row=0)

        # Search Tab, Frame for search
        stockSearchFrame = ttk.LabelFrame(tabSearchStock, text=' Stock Dates List ')
        stockSearchFrame.grid(column=0, row=0, padx=5, pady=5)

        # List box
        self.l_stockDateList = tk.Listbox(stockSearchFrame, height=10)
        self.l_stockDateList.grid(column=0, row=0, sticky=tk.W)
        s_scrollDate = tk.Scrollbar(stockSearchFrame, command=self.l_stockDateList.yview)
        s_scrollDate.grid(column=1, row=0, sticky=tk.NS)
        #self.l_stockDateList.config(yscrollcommand=self.yscroll.set)
        self.l_stockDateList.bind('<Double-Button-1>', self.selectitem)

        # Insert Dates into Listbox
        self.searchstockdates()

        # Edit, Delete, Export buttons frame
        stockSearchButtonFrame = ttk.LabelFrame(tabSearchStock)
        stockSearchButtonFrame.grid(column=1, row=0, padx=5, pady=5)
        # Edit button
        b_stockDateSearch=ttk.Button(stockSearchButtonFrame, text='Edit')
        b_stockDateSearch.grid(column=1, row=2, padx=5, pady=5, sticky=tk.E)
        # Delete button
        b_stockDelete = ttk.Button(stockSearchButtonFrame, text='Delete', command=self.deleteRecordCmd)
        b_stockDelete.grid(column=1, row=4, padx=5, pady=5, sticky=tk.E)
        # Export Button
        b_stockExport = ttk.Button(stockSearchButtonFrame, text='Export')
        b_stockExport.grid(column=1, row=6, padx=5, pady=5, sticky=tk.E)

        # View searched stock tree frame
        self.stockSearchViewFrame = ttk.LabelFrame(tabSearchStock, text='View Searched Stock')
        self.stockSearchViewFrame.grid(column=0, row=1, padx=5, pady=5, columnspan=2)
        #ttk.Label(self.stockSearchViewFrame, text='This is view test').grid(column=0, row=0)
        self.viewtree = ttk.Treeview(self.stockSearchViewFrame)
        self.viewtree.grid(column=0, row=2, columnspan=2)
        self.yscrollviewtree = tk.Scrollbar(self.stockSearchViewFrame, command=self.viewtree.yview)
        self.viewtree.config(yscrollcommand=self.yscrollviewtree.set)
        self.column = ('itemDescription','itemQuantity','itemUnitPrice','itemTotalPrice')
        self.heading = ('Description',
                         'Quantity',
                         'Unit Price',
                         'Total Price'
                         )
        self.viewtree['columns'] = self.column
        for element in self.column:
            if element == 'itemDescription':
                col_width = 110
            elif element == 'itemQuantity':
                col_width = 85
            elif element == 'itemUnitPrice':
                col_width = 90
            else: col_width = 90
            self.viewtree.column(element, width=col_width)
        counter = 0
        self.viewtree.heading('#0', text='No.')
        self.viewtree.column('#0', width=15)
        for element in self.column:
            self.viewtree.heading(element, text=self.heading[counter])
            counter +=1

        # Create tags for treeview
        self.viewtree.tag_configure('evenrow', background='#FFFFFF')
        self.viewtree.tag_configure('oddrow', background='#F2F1E6')

    # Date Picker frame pop-up function
    def pickDateCmd(self):

        def print_sel():
            #print(cal.selection_get())
            global dateValue
            dateValue = cal.selection_get()
            #print(dateValue)

        win = tk.Toplevel(self)
        win.resizable(0,0)

        # Get full day
        today = date.strftime(date.today(), '%Y-%m-%d')
        # Strip year
        fyear = int(today[:4])
        # Strip month
        tmp_month = today[5:7]
        if tmp_month[0] == "0":
            fmonth = int(tmp_month[1])
        else:
            fmonth = int(tmp_month)
        # Strip day
        tmp_day = today[8:10]
        if tmp_day[0] == "0":
            fday = int(tmp_day[1])
        else:
            fday = int(tmp_day)

        cal = Calendar(win, font="Arial 7", selectmode='day', cursor="hand1", year=fyear, month=fmonth, day=fday)
        cal.pack(fill="both", expand=True)
        ttk.Button(win, text="ok", command=print_sel).pack()

    def saveRecordCmd(self):
    # Initialize the database connection
        database = sqlite3.connect('hojdb.db')
        cur = database.cursor()

        #treeLineCount = treeLineCount + 1

        global dateValue
        #print(dateValue)

        itemsTotal = self.v_itemsTotal.get()
        try:
            i_itemsTotal = int(itemsTotal)
        except:
            mbox.showerror('Input Error', 'Enter number as Total items')

        itemsUnitCost =  self.v_itemsUnitCost.get()
        try:
            f_itemsUnitCost = float(itemsUnitCost)
        except:
            mbox.showerror('Input Error', 'Enter number as Items unit cost')

        itemsTotalUnitCost = self.v_itemsTotalUnitCost.get()
        try:
            f_itemsTotalUnitCost = float(itemsTotalUnitCost)
        except:
            mbox.showerror('Input Error', 'Enter number as Items Total cost')

        #print(type(i_itemsTotal))
        itemsCombo = self.v_itemSelect.get()

        # Get Rowcount
        cur.execute("SELECT COUNT(rowid) from t_Stock")
        rowCount = cur.fetchall()[0][0]
        rowCount = rowCount + 1

        if (isinstance(i_itemsTotal, int) and isinstance(f_itemsUnitCost, float) and isinstance(f_itemsTotalUnitCost, float)):
            cur.execute("INSERT INTO t_Stock values (?,?,?,?,?,?)",
                (rowCount, dateValue, itemsCombo, itemsUnitCost, itemsTotal, itemsTotalUnitCost)
                )
            try:
                database.commit()
            except sqlite3.Error:
                database.rollback()

            if database:
                cur.close()
                database.close()
                showRecord = "Item: " + itemsCombo + "\n" + "Item unit cost: " + itemsUnitCost + "\n" + "Item Quantity: " + itemsTotal + "\n" + "Items total cost: :" + itemsTotalUnitCost
                mbox.showinfo('Successful', showRecord)
        else:
            mbox.showerror('Save Error','Could not save the stock record')

    # Function to search stock dates
    def searchstockdates(self):
        # Initialize the database connection
        database = sqlite3.connect('hojdb.db')
        cur = database.cursor()
        query = cur.execute("select distinct c_date from t_Stock")
        rows = query.fetchall()
        for row in rows:
            self.l_stockDateList.insert('end', row[0])

    # Function - double click select list box item
    def selectitem(self, event):
        date_from_list = self.l_stockDateList.get('active')
        #print(date_from_list)

        # Check if there is any data in the tree
        # If so, delete and load the list again
        if len(self.viewtree.get_children()) != 0:
            child = self.viewtree.get_children()
            for item in child:
                self.viewtree.delete(item)

        # Connect to db and query
        database = sqlite3.connect('hojdb.db')
        cur = database.cursor()
        query = cur.execute("select * from t_Stock where c_date like '" + date_from_list + "'")
        rows = query.fetchall()
        #for x in rows:
        #    print(x)
        if database:
            cur.close()
            database.close()

        # Insert fetched data into tree
        counter = 1
        for row in rows:
            if counter % 2 == 0:
                self.viewtree.insert('','end',str(row[0]), text=str(row[0]), tag=('evenrow',))
            else:
                self.viewtree.insert('', 'end', str(row[0]), text=str(row[0]), tag=('oddrow',))

            self.viewtree.set(str(row[0]), self.column[0], str(row[2]))
            self.viewtree.set(str(row[0]), self.column[1], str(row[4]))
            self.viewtree.set(str(row[0]), self.column[2], str(row[3]))
            self.viewtree.set(str(row[0]), self.column[3], str(row[5]))
            counter +=1

    def deleteRecordCmd(self):
        date_from_list_for_delete = self.l_stockDateList.get('active')

        deletemessage = "Really delete stock record for " + date_from_list_for_delete
        answer = mbox.askyesno('Alert!', deletemessage)

        #print(answer)

        if answer:

            # Connect to db and query
            database = sqlite3.connect('hojdb.db')
            cur = database.cursor()
            deletequery = "delete from t_Stock where c_date='" + date_from_list_for_delete + "'"
            query = cur.execute(deletequery)
            #rows = query.fetchall()

            try:
                database.commit()
            except sqlite3.Error:
                database.rollback()


            if database:
                cur.close()
                database.close()
        else:
            mbox.showinfo('Alert','Cancelled')

        #self.refreshList()

    # Refresh List after delete operation
    #def refreshList(self):
    #    # Initialize the database connection
    #    database = sqlite3.connect('hojdb.db')
    #    cur = database.cursor()
    #    query = cur.execute("select distinct c_date from t_Stock")
    #    rows = query.fetchall()
    #    for row in rows:
    #        self.l_stockDateList.insert('end', row[0])

    #def refreshTrees(self):
    #    print()

# Expenses Frame
class ExpenseFrame(tk.Toplevel):
    # Class init
    def __init__(self, master):
        tk.Toplevel.__init__(self,master)
        self.title("Expenses")
        self.grab_set()
        self.resizable(0,0)
        # stringVar expenseDate in ExpenseFrame
        expenseDate = 5

        # Notebook Frames
        self.tabControl = ttk.Notebook(self)
        self.tabExpenseCreate = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tabExpenseCreate, text='          Create Expense      ')
        self.tabViewExpense = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tabViewExpense, text='         View Expenses     ')
        self.tabControl.pack()

        # Entry variables
        self.v_expenseItemEntry = tk.StringVar()
        self.v_expenseAmountEntry = tk.StringVar()
        self.v_expensePayee = tk.StringVar()
        self.v_expenseCategory = tk.StringVar()
        self.v_expensePayMethod = tk.StringVar()
        self.v_expenseDescr = tk.StringVar()


        # Expense create frame
        self.lf_Frame = ttk.LabelFrame(self.tabExpenseCreate, text='Enter Expense Details             ')
        self.lf_Frame.grid(column=0, row=1, padx=5, pady=5)
        # Date picker
        #cal1 = DateEntry(self.lf_Frame, width=12, background='darkblue',
        #                foreground='white', borderwidth=2)
        #cal1.grid(column=1, row=0, padx=5, pady=5)
        # Create date picker button
        btn_pickDate = ttk.Button(self.lf_Frame, text='     Pick Date     ', command=self.pickDateCmd)
        btn_pickDate.grid(column=1, row=0, pady=5, sticky=tk.E)

        # Expense item entry
        ttk.Label(self.lf_Frame, text='Expense Item: ').grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)
        self.e_expenseItem = ttk.Entry(self.lf_Frame, textvariable=self.v_expenseItemEntry)
        self.e_expenseItem.grid(column=1, row=2, sticky=tk.E)
        # Expense amount entry
        ttk.Label(self.lf_Frame, text='Amount: ').grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)
        self.e_expenseAmount = ttk.Entry(self.lf_Frame, textvariable=self.v_expenseAmountEntry)
        self.e_expenseAmount.grid(column=1, row=3, sticky=tk.E)
        # Payee entry
        ttk.Label(self.lf_Frame, text='Payee:   ').grid(column=0, row=4, padx=5, pady=5, sticky=tk.W)
        self.e_expensePayee = ttk.Entry(self.lf_Frame, textvariable=self.v_expensePayee)
        self.e_expensePayee.grid(column=1, row=4, padx=5, pady=5, sticky=tk.E)
        # Category entry & Combobox
        ttk.Label(self.lf_Frame, text='Category').grid(column=0, row=5, sticky=tk.W, padx=5, pady=5)
        self.cb_expenseCatBox = ttk.Combobox(self.lf_Frame, textvariable=self.v_expenseCategory, width=20, state='readonly')
        self.cb_expenseCatBox['values'] = ("Salaries","Utilites","Money Transfer","Tax","Loans","Transport",
                                           "Personal","Others")
        self.cb_expenseCatBox.grid(column=1, row=5, padx=5, pady=5, sticky=tk.E)
        self.cb_expenseCatBox.current(0)
        # Payment method entry
        ttk.Label(self.lf_Frame, text='Payment Method: ').grid(column=0, row=6, padx=5, pady=5, sticky=tk.W)
        self.e_expensePayMethod = ttk.Entry(self.lf_Frame, textvariable=self.v_expensePayMethod)
        self.e_expensePayMethod.grid(column=1, row=6, padx=5, pady=5, sticky=tk.E)
        # Entry Description
        ttk.Label(self.lf_Frame, text='Description: ').grid(column=0, row=7, padx=5, pady=5, sticky=tk.W)
        self.e_expenseDescription = ttk.Entry(self.lf_Frame, textvariable=self.v_expenseDescr)
        self.e_expenseDescription.grid(column=1, row=7, padx=5, pady=5, sticky=tk.E)
        # Save button
        self.btn_expSave = ttk.Button(self.lf_Frame, text='Save Expense', command=self.expSaveCmd)
        self.btn_expSave.grid(column=1, row=8, padx=5, pady=5, sticky=tk.E)


        


# Date Picker frame pop-up function
    def pickDateCmd(self):

        def print_sel():
            #print(cal.selection_get())
            global expenseDate
            expenseDate = cal.selection_get()
            #print(expenseDate)

        win = tk.Toplevel(self)
        win.resizable(0,0)

        # Get full day
        today = date.strftime(date.today(), '%Y-%m-%d')
        # Strip year
        fyear = int(today[:4])
        # Strip month
        tmp_month = today[5:7]
        if tmp_month[0] == "0":
            fmonth = int(tmp_month[1])
        else:
            fmonth = int(tmp_month)
        # Strip day
        tmp_day = today[8:10]
        if tmp_day[0] == "0":
            fday = int(tmp_day[1])
        else:
            fday = int(tmp_day)

        cal = Calendar(win, font="Arial 7", selectmode='day', cursor="hand1", year=fyear, month=fmonth, day=fday)
        cal.pack(fill="both", expand=True)
        ttk.Button(win, text="ok", command=print_sel).pack()

    def expSaveCmd(self):
        # print()
        # Initialize the database connection
        database = sqlite3.connect('hojdb.db')
        cur = database.cursor()
        # get expenseDate
        global expenseDate
        #   print(expenseDate)

        # Get expense items details
        f_ExpItem = self.e_expenseItem.get()
        ExpAmount = self.e_expenseAmount.get()
        try:
            f_ExpAmount = float(ExpAmount)
        except:
            mbox.showerror('Input Error', 'Enter number as Expense Amount')

        # Get Payee detail
        f_payee = self.e_expensePayee.get()

        # Get Expense Category
        f_expenseCat = self.cb_expenseCatBox.get()

        # Get Payment Method
        f_paymethod = self.e_expensePayMethod.get()

        # Get Expense Description
        f_expDescr = self.e_expenseDescription.get()

        # Get Rowcount
        cur.execute("SELECT COUNT(rowid) from t_Expense")
        rowCount = cur.fetchall()[0][0]
        rowCount = rowCount + 1

        cur.execute("INSERT INTO t_Expense values (?,?,?,?,?,?,?)",
                            (rowCount, expenseDate, f_ExpAmount, f_payee, f_expenseCat, f_paymethod, f_expDescr)
                            )
        try:
            database.commit()
        except sqlite3.Error:
            database.rollback()

        if database:
            cur.close()
            database.close()
            showRecord = "Expense saved!"
            mbox.showinfo('Successful', showRecord)
        else:
            mbox.showinfo('Save Error', 'Could not save the expense record')




















# Sales Frame
class recordSales(tk.Toplevel):
    def __init__(self,master):
        tk.Toplevel.__init__(self,master)
        self.title("Record Sales")
        self.grab_set()
        self.resizable(0,0)

def main():
    app = tk.Tk()
    MainWindow(app)
    app.mainloop()

if __name__ == '__main__':
    main()