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
start_date = "Beginn"
end_date = "Ende"
rating = "Rating"

# Create a class, which holds all our functions and data manipulations
class readingSummarizer():

    # The init-Method creates a Dataframe from the csv-file and processes the data to create new values
    def __init__(self,filename):
        self.books = pd.read_csv(filename)

        # Dataframe manipulation

        # Edit the Dataframe by converting the date-columns to Pandas-dates to process them in further steps
        self.books = self.convertDates(self.books)


        # Create a new column to get the amount of days, the book was read by subtracting the end date with
        # the start date and add one additional day. Transform it to an integer value after.
        self.books["days_read"] = (self.books[end_date] - self.books[start_date] + pd.to_timedelta(1, unit='d')).dt.days

        # Create a new column to get the pages per day by dividing the pages by the days read value.
        # Round the result to two decimal places.
        self.books["pages_per_day"] = round(self.books[pages] / self.books.days_read,2)

    # Data manipulation functions

    # Converts the start and end date to the Pandas date format
    def convertDates(self,df):
        df[start_date] = pd.to_datetime(df[start_date], infer_datetime_format=True)
        df[end_date] = pd.to_datetime(df[end_date], infer_datetime_format=True)
        return df


    # View the Dataframe on the "Reading-Speed" aspect by first sorting the values either ascending or descending
    # based on a given boolean value and then plot it afterwards.
    def readingSpeed(self,order_high_to_low):
        self.books = self.books.sort_values(by="days_read",ascending=order_high_to_low)
        self.barplotFunction(self.books,"days_read")

    # View the Dataframe on the "Pages-Per-Days" aspect by first sorting the values either ascending or descending
    # based on a given boolean value and then plot it afterwards.
    def pagesPerDay(self,order_high_to_low):
        self.books = self.books.sort_values(by="pages_per_day",ascending=not order_high_to_low)
        self.barplotFunction(self.books,"pages_per_day")


    def monthlyPages(self,type_group):

        def getPeriod(row):
            month_count = {
                            "01":0,
                            "02":0,
                            "03":0,
                            "04":0,
                            "05":0,
                            "06":0,
                            "07":0,
                            "08":0,
                            "09":0,
                            "10":0,
                            "11":0,
                            "12":0
                            }

            # Stores all days the book was read in a single column
            row["period"] = pd.date_range(row[start_date], row[end_date]).date.tolist()

            for i in row["period"]:
                month_count[str(i)[5:7]] += 1

            for key, values in month_count.items():
                if values == 0:
                    pass
                else:
                    row[key] = round(row[pages] * (values / row["days_read"]), 1)

            return row

        month_dict = {
            "01":"January",
            "02":"February",
            "03":"March",
            "04":"April",
            "05":"May",
            "06":"June",
            "07":"July",
            "08":"August",
            "09":"September",
            "10":"October",
            "11":"November",
            "12":"December"
        }

        type_of_groups = {
                            "Art des Buchs": ["Roman","Sachbuch"],
                            "Medium": ["Buch","E-Book"],
                            "Sprache": ["Deutsch", "Englisch"]
                        }

        group_member = type_of_groups[type_group]


        for key in month_dict.keys():
            self.books[key] = 0

        monthly_pages = self.books.apply(getPeriod, axis=1)

        monthly_pages = monthly_pages.groupby(type_group).sum()

        output_list = []
        for key, values in month_dict.items():
            output_list.append([values,
                                round(monthly_pages.loc[group_member[0]][key],1),
                                round(monthly_pages.loc[group_member[1]][key],1)])

        output_df = pd.DataFrame(data=output_list, columns=["Month",group_member[0],group_member[1]])
        output_df = output_df.set_index("Month")

        return output_df



    def getGeneralStyling(self):
        # Style and color specifications
        sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
        colors = ["#4667FA", "#2FD3FA"]
        sns.set_palette(sns.color_palette(colors))


    # Creates a plot of a specific Dataframe column
    def barplotFunction(self,df,column):
        self.getGeneralStyling()

        # Calculate the mean value of the column
        mean = statistics.mean(df[column])

        # Cut the Dataframe by only using the first 5 entries. Remember: It's already sorted beforehand.
        df = df.head(5)

        # Create the bar plot with our given column on the y-axis.
        sns.barplot(y=df[column], x=df[title], hue=df[type_of_book], dodge=False)

        # Add a horizontal line to the plot, which symbolizes the mean value.
        plt.axhline(y=mean, color="red")
        plt.show()

    def stackedBarplotFunction(self,df):
        self.getGeneralStyling()

        df.plot(kind="bar", stacked=True)
        plt.show()




a = readingSummarizer("Buchliste2.csv")
pages_per_month = a.monthlyPages(type_of_book)
a.stackedBarplotFunction(pages_per_month)