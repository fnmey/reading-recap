import pandas as pd


class readingSummarizer():
    # Read the imported csv-file
    def __init__(self,filename):
        self.books = pd.read_csv(filename)
        self.books = self.convertDates(self.books)
        self.books["Tage gelesen"] = self.books.Ende - self.books.Beginn + pd.to_timedelta(1, unit='d')
        self.books["Seiten pro Tag"] = round(self.books["Seiten"] / self.books["Tage gelesen"].dt.days,2)


        def range_between(row):
            return pd.date_range(row["Beginn"], row["Ende"])

        self.books["Zeitraum"] = self.books.apply(range_between,axis=1)

    def convertDates(self,df):
        df["Beginn"] = pd.to_datetime(df["Beginn"], infer_datetime_format=True)
        df["Ende"] = pd.to_datetime(df["Ende"], infer_datetime_format=True)
        return df

    def readingSpeed(self,order_high_to_low):
        self.books = self.books.sort_values(by="Tage gelesen",ascending=order_high_to_low)
        print(self.books[["Titel", "Tage gelesen"]].head(5))

    def pagesPerDay(self,order_high_to_low):
        self.books = self.books.sort_values(by="Seiten pro Tag",ascending=not order_high_to_low)
        print(self.books[["Titel", "Seiten pro Tag"]].head(5))


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