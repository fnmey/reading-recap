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


class readingSummarizer():
    # Read the imported csv-file
    def __init__(self,filename):
        self.books = pd.read_csv(filename)
        self.books = self.convertDates(self.books)
        self.books["days_read"] = (self.books[end_date] - self.books[start_date] + pd.to_timedelta(1, unit='d')).dt.days
        self.books["pages_per_day"] = round(self.books[pages] / self.books.days_read,2)


        def range_between(row):
            return pd.date_range(row[start_date], row[end_date])

        self.books["period"] = self.books.apply(range_between,axis=1)

    def convertDates(self,df):
        df[start_date] = pd.to_datetime(df[start_date], infer_datetime_format=True)
        df[end_date] = pd.to_datetime(df[end_date], infer_datetime_format=True)
        return df

    def readingSpeed(self,order_high_to_low):
        self.books = self.books.sort_values(by="days_read",ascending=order_high_to_low)
        self.plotFunction(self.books,"days_read")

    def pagesPerDay(self,order_high_to_low):
        self.books = self.books.sort_values(by="pages_per_day",ascending=not order_high_to_low)
        self.plotFunction(self.books,"pages_per_day")

    def plotFunction(self,df,column):
        mean = statistics.mean(df[column])
        df = df.head(5)
        sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
        colors = ["#4667FA", "#2FD3FA"]
        sns.set_palette(sns.color_palette(colors))
        sns.barplot(y=df[column], x=df[title], hue=df[type_of_book], dodge=False)
        plt.axhline(y=mean, color="red")
        plt.show()

dictionary = {"January": 1,
              "February":2,
              "March": 3,
              "April": 4,
              "May": 5,
              "June": 6,
              "July": 7,
              "August": 8,
              "September":9,
              "October":10,
              "November":11,
              "December":12}

#for key, value in dictionary:


a = readingSummarizer("Buchliste.csv")
a.pagesPerDay(order_high_to_low=True)