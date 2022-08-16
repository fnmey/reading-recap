import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

class readingSummarizer():
    # Read the imported csv-file
    def __init__(self,filename):
        self.books = pd.read_csv(filename)


    def convertDates(self,df):
        df["Beginn"] = pd.to_datetime(df["Beginn"], infer_datetime_format=True)
        df["Ende"] = pd.to_datetime(df["Ende"], infer_datetime_format=True)
        return df

    def getColumnNames(self):
        columns_list = [x for x in self.books.columns]
        return columns_list

    def runIt(self):
        self.books = self.convertDates(self.books)
        print(self.books["Ende"])





class GUI():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Tkinter Open File Dialog')
        self.root.resizable(False, False)
        self.root.geometry('300x150')

    # open button




    def readFile(self):
        filetypes = (
            ('csv files', '*.csv'),
            ('All files', '*.*')
        )

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)

        a = readingSummarizer(filename)
        self.root.destroy()
        PopUpWindow(a.getColumnNames())





    def runIT(self):
        self.open_button = ttk.Button(
            self.root,
            text='Open a File',
            command=self.readFile)

        self.open_button.pack(expand=True)

        # run the application
        self.root.mainloop()




class PopUpWindow:
    def __init__(self, column_names):
        self.popup = tk.Tk()
        self.popup.title('Tkinter Open File Dialog')
        self.popup.resizable(False, False)
        self.popup.geometry('400x150')

        # Title section
        title = tk.StringVar()
        title.set(column_names[0])
        tk.Label(self.popup, text="Titel").grid(row=0,column=0)
        tk.OptionMenu(self.popup, title, *column_names).grid(row=1,column=0)


        # Pages section
        pages = tk.StringVar()
        pages.set(column_names[0])
        tk.Label(self.popup, text="Pages").grid(row=0, column=1)
        tk.OptionMenu(self.popup, pages, *column_names).grid(row=1, column=1)

        # Start date section
        start_date = tk.StringVar()
        start_date.set(column_names[0])
        tk.Label(self.popup, text="Start Date").grid(row=0, column=2)
        tk.OptionMenu(self.popup, start_date, *column_names).grid(row=1, column=2)

        # End date section
        enddate = tk.StringVar()
        enddate.set(column_names[0])
        tk.Label(self.popup, text="End Date").grid(row=0, column=3)
        tk.OptionMenu(self.popup, enddate, *column_names).grid(row=1, column=3)

        self.popup.mainloop()
A = GUI()
A.runIT()
