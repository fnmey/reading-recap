from main import readingSummarizer
import tkinter as tk


class GUI:
    def __init__(self):
        # Initialize a tkinter main window with fix width and height
        self.window = tk.Tk()
        self.window_width = 400
        self.window_height = 400

        # Get the screen dimension of the current screen
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()

        # Find the center point of the screen
        self.center_x = int(self.screen_width / 2 - self.window_width / 2)
        self.center_y = int(self.screen_height / 2 - self.window_height / 2)

        # Adjust the geometry to place the window right in the center
        self.window.geometry(f'{self.window_width}x{self.window_height}+{self.center_x}+{self.center_y}')

        # Define the window title
        self.window.title("Select your choice")

        # Initialize the class out of the main.py file which stores the functions
        self.functions = readingSummarizer("Buchliste.csv")

        # Create the Pages Per Day button and place it on the main window
        self.ppd_button = tk.Button(self.window, text="Pages Per Day",
                                    command=lambda: self.functions.pagesPerDay(True))
        self.ppd_button.grid(row=0, column=0)

        # Create the Reading Speed button and place it on the main window
        self.rs_button = tk.Button(self.window, text="Reading Speed",
                                   command=lambda: self.functions.readingSpeed(True))
        self.rs_button.grid(row=0, column=1)

        # Create the Monthly Pages button and place it on the main window
        self.mp_button = tk.Button(self.window, text="Monthly Pages",
                                   command=lambda: self.functions.monthlyPages("Art des Buchs"))
        self.mp_button.grid(row=0, column=3)

        # Run the main window
        self.window.mainloop()


# a = readingSummarizer("Buchliste.csv")

# Run the class
if __name__ == "__main__":
    a = GUI()