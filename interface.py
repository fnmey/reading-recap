from main import readingSummarizer
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd


class GUI:
    def __init__(self):
        # Initialize a tkinter main window with fix width and height
        self.window = tk.Tk()
        self.window_width = 500
        self.window_height = 150

        # Get the screen dimension of the current screen
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()

        # Find the center point of the screen
        self.center_x = int(self.screen_width / 2 - self.window_width / 2)
        self.center_y = int(self.screen_height / 2 - self.window_height / 2)

        # Adjust the geometry to place the window right in the center
        self.window.geometry("{width}x{height}+{center_x}+{center_y}".format(
            width=self.window_width,
            height=self.window_height,
            center_x=self.center_x,
            center_y=self.center_y))

        # Define the window title
        self.window.title("Select your choice")

        # Initialize the class out of the main.py file which stores the functions
        self.functions = readingSummarizer("Buchliste.csv")

        # Create a label for the file selection.
        self.label = tk.Label(self.window, text="Select your input csv below.")
        self.label.grid(row=0, column=0, columnspan=3)

        # Create a button, that will select an input file.
        self.file_selection = tk.Button(self.window, text="File not selected.", command=lambda: self.select_file())
        self.file_selection.grid(row=1, column=0, columnspan=3)

        # Create the Pages Per Day button and place it on the main window
        self.ppd_button = tk.Button(self.window, text="Pages Per Day",
                                    command=lambda: self.functions.pagesPerDay(self.good_bad_dropdown.get()))
        self.ppd_button.grid(row=2, column=0)

        # Create the Reading Speed button and place it on the main window
        self.rs_button = tk.Button(self.window, text="Reading Speed",
                                   command=lambda: self.functions.readingSpeed(self.good_bad_dropdown.get()))
        self.rs_button.grid(row=2, column=1)

        # Create a Combobox with two values that are given to the button function.
        self.good_bad_dropdown = ttk.Combobox(self.window,
                                              values=["Good", "Bad"])
        self.good_bad_dropdown.current(0)
        self.good_bad_dropdown.grid(row=3, column=0, columnspan=2)

        # Create the Monthly Pages button and place it on the main window
        self.mp_button = tk.Button(self.window, text="Monthly Pages",
                                   command=lambda: self.functions.monthlyPages(self.mp_dropdown.get()))
        self.mp_button.grid(row=2, column=2)

        # Create a Combobox for filtering the Monthly Pages button and place it
        self.mp_dropdown = ttk.Combobox(self.window,
                                        values=["Type of Book",
                                                "Medium",
                                                "Language"])

        self.mp_dropdown.current(0)
        self.mp_dropdown.grid(row=3, column=2)

        # Run the main window
        self.window.mainloop()

    # Function to select the input file.
    def select_file(self):

        # Assign the csv file type and also a general type.
        filetypes = [("CSV file","*.csv"),
                     ("All files","*.*")]

        # Trigger the open file dialog and assign the selected type to this variable.
        self.filename = fd.askopenfilename(filetypes=filetypes,
                                           initialdir="/")

# Run the class
if __name__ == "__main__":
    a = GUI()
