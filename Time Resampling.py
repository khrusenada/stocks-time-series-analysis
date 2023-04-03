import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import date, timedelta

stocks = input("Enter stock symbol: ")
today = date.today()

d1 = today.strftime("%Y-%m-%d")
end_date = d1
d2 = date.today() - timedelta(days=1080)
d2 = d2.strftime("%Y-%m-%d")
start_date = d2

data = yf.download(stocks, 
                      start=start_date, 
                      end=end_date, 
                      progress=False)


#change date from column to index
data["Date"] = data.index

data = data[["Date", "Open", "High", 
             "Low", "Close", "Adj Close", "Volume"]]
data.reset_index(drop=True, inplace=True)


# Convert string to datetime64
data['Date'] = data['Date'].apply(pd.to_datetime)

#to make sure date colum is in index column
data.set_index('Date', inplace=True)

data.resample(rule='A').mean()
data['Adj Close'].resample('A').mean().plot(kind='bar',figsize = (10,4))
plt.title('Yearly Mean Adj Close Price for Amazon')
 
plt.show()

