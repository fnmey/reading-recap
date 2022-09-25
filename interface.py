from main import readingSummarizer
import tkinter as tk

class GUI:
    def __init__(self):

        self.window = tk.Tk()
        self.window_width = 400
        self.window_height = 400

        # get the screen dimension
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()

        # find the center point
        self.center_x = int(self.screen_width / 2 - self.window_width / 2)
        self.center_y = int(self.screen_height / 2 - self.window_height / 2)

        self.window.geometry(f'{self.window_width}x{self.window_height}+{self.center_x}+{self.center_y}')
        self.window.title("Select your choice")

        self.functions = readingSummarizer("Buchliste.csv")


        self.ppd_button = tk.Button(self.window,text="Pages Per Day",command=lambda: self.functions.pagesPerDay(True))
        self.ppd_button.grid(row=0,column=0)

        self.rs_button = tk.Button(self.window,text="Reading Speed", command=lambda: self.functions.readingSpeed(True))
        self.rs_button.grid(row=0,column=1)

        self.window.mainloop()


#a = readingSummarizer("Buchliste.csv")

a = GUI()