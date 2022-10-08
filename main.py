import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import statistics

# Define the Notion columns
title = "Titel"
author = "Autor"
pages = "Seiten"
language = "Sprache"
type_of_book = "Art des Buchs"
medium = "Medium"
start_date = "Beginn"
end_date = "Ende"
rating = "Rating"

category = "Reading Speed"
good_to_bad = True


# Create a class, which holds all our functions and data manipulations
class readingSummarizer():

    # The init-Method creates a Dataframe from the csv-file and processes the data to create new values
    def __init__(self, filename):

        # Dataframe manipulation

        # Edit the Dataframe by converting the date-columns to Pandas-dates to process them in further steps
        self.books = self.convertDates(self.books)

        # Create a new column to get the amount of days, the book was read by subtracting the end date with
        # the start date and add one additional day. Transform it to an integer value after.
        self.books["days_read"] = (self.books[end_date] - self.books[start_date] + pd.to_timedelta(1, unit='d')).dt.days

        # Create a new column to get the pages per day by dividing the pages by the days read value.
        # Round the result to two decimal places.
        self.books["pages_per_day"] = round(self.books[pages] / self.books.days_read, 2)

    # Data manipulation functions

    # Converts the start and end date to the Pandas date format
    def convertDates(self, df):
        df[start_date] = pd.to_datetime(df[start_date], infer_datetime_format=True, format="%d/%m/%Y")
        df[end_date] = pd.to_datetime(df[end_date], infer_datetime_format=True, format="%d/%m/%Y")
        return df

    # View the Dataframe on the "Reading-Speed" aspect by first sorting the values either ascending or descending
    # based on a given boolean value and then plot it afterwards.
    def readingSpeed(self, order_high_to_low):

        # Give the input variable a boolean value for the next step.
        if order_high_to_low == "Good":
            order_high_to_low = True
        elif order_high_to_low == "Bad":
            order_high_to_low = False
        self.books = self.books.sort_values(by="days_read", ascending=order_high_to_low)

        self.barplotFunction(self.books.head(5), "days_read")

    # View the Dataframe on the "Pages-Per-Days" aspect by first sorting the values either ascending or descending
    # based on a given boolean value and then plot it afterwards.
    def pagesPerDay(self, order_high_to_low):

        # Give the input variable a boolean value for the next step.
        if order_high_to_low == "Good":
            order_high_to_low = True
        elif order_high_to_low == "Bad":
            order_high_to_low = False

        self.books = self.books.sort_values(by="pages_per_day", ascending=not order_high_to_low)

        self.barplotFunction(self.books.head(5), "pages_per_day")

    def monthlyPages(self, type_group):
        if type_group == "Type of Book":
            type_group = type_of_book
        elif type_group == "Medium":
            type_group = medium
        elif type_group == "Language":
            type_group = language
        # Function, that calculates the mean pages read per month for each book.
        def pagesInMonth(row):

            # Dictionary, that stores the values of pages read per month.
            month_count = {
                "01": 0,
                "02": 0,
                "03": 0,
                "04": 0,
                "05": 0,
                "06": 0,
                "07": 0,
                "08": 0,
                "09": 0,
                "10": 0,
                "11": 0,
                "12": 0
            }

            # Stores all days the book was read in a single column
            row["period"] = pd.date_range(row[start_date], row[end_date]).date.tolist()

            # For every entry (meaning every day) the month counter is increasing.
            for i in row["period"]:
                month_count[str(i)[5:7]] += 1

            # Iterate over the counter-dict and pass the values != 0 to the specific DataFrame column for each month.
            for key, values in month_count.items():
                if values == 0:
                    pass
                else:
                    row[key] = round(row[pages] * (values / row["days_read"]), 1)

            # Return the row in the end, so that an apply-function on the existing DataFrame works.
            return row

        # Filters the DataFrame based on a selected type
        def filterByType(df):
            # TEMPORÄR - Start
            # Define the type of groups there are for each category
            type_of_groups = {
                "Art des Buchs": ["Roman", "Sachbuch"],
                "Medium": ["Buch", "E-Book"],
                "Sprache": ["Deutsch", "Englisch"]
            }

            # Get the group members of the selected type
            group_member = type_of_groups[type_group]
            # TEMPORÄR - Ende

            # Group the dataframe by the selected type and generate the sum for each column
            df = df.groupby(type_group).sum()

            # Create a list that stores the value of the dictionary (the month name) and the sum for each
            # group member for each month
            output_list = []
            for key, values in month_dict.items():
                output_list.append([values,
                                    round(df.loc[group_member[0]][key], 1),
                                    round(df.loc[group_member[1]][key], 1)])

            # Create a DataFrame out of this list with the month and the group-member names as the column names
            output_df = pd.DataFrame(data=output_list, columns=["Month", group_member[0], group_member[1]])
            output_df = output_df.set_index("Month")

            return output_df

        # This dictionary works as translation, so that we'll get the actual names instead of the number
        # of each month for visualization purposes
        month_dict = {
            "01": "January",
            "02": "February",
            "03": "March",
            "04": "April",
            "05": "May",
            "06": "June",
            "07": "July",
            "08": "August",
            "09": "September",
            "10": "October",
            "11": "November",
            "12": "December"
        }
        # Iterate over the defined dict and create "empty" Dataframe columns
        for key in month_dict.keys():
            self.books[key] = 0

        # Apply the above defined function so that we'll fill the above created month columns
        monthly_pages = self.books.apply(pagesInMonth, axis=1)

        # If there is no type_group specified, then we will create a line plot of the pages per month.
        if type_group is False:
            output_list = []
            for key, value in month_dict.items():
                output_list.append([value, monthly_pages.sum()[key]])
            output_df = pd.DataFrame(output_list, columns=["Month", "Pages"])

            self.lineplotFunction(output_df, x="Month", y="Pages")

        # Else, we will filter the DataFrame by the type of group and create a stacked bar plot.
        else:
            monthly_pages = filterByType(monthly_pages)
            # Choose the stacked bar plot for this type of visualization
            self.stackedBarplotFunction(monthly_pages)

    def getGeneralStyling(self):
        # Style and color specifications
        sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
        colors = ["#4667FA", "#2FD3FA"]
        sns.set_palette(sns.color_palette(colors))

    # Creates a bar plot of a specific Dataframe column
    def barplotFunction(self, df, column):
        self.getGeneralStyling()

        # Calculate the mean value of the column
        mean = statistics.mean(df[column])

        # Create the bar plot with our given column on the y-axis.
        sns.barplot(y=df[column], x=df[title], hue=df[type_of_book], dodge=False)

        # Add a horizontal line to the plot, which symbolizes the mean value.
        plt.axhline(y=mean, color="red")
        plt.show()

    def stackedBarplotFunction(self, df):
        self.getGeneralStyling()

        df.plot(kind="bar", stacked=True)
        plt.show()

    def lineplotFunction(self, df, x, y):
        self.getGeneralStyling()

        # Calculate the mean value of the column
        mean = statistics.mean(df[y])

        # Create the bar plot with our given column on the y-axis.
        sns.lineplot(y=df[y], x=df[x], sort=False)

        # Add a horizontal line to the plot, which symbolizes the mean value.
        plt.axhline(y=mean, color="red")

        plt.show()