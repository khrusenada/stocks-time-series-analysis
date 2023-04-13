import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import date, timedelta
from sklearn.linear_model import LinearRegression

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


# change date from column to index
data["Date"] = data.index
data = data[["Date", "Open", "High", 
             "Low", "Close", "Adj Close", "Volume"]]
data.reset_index(drop=True, inplace=True)

# Convert string to datetime64
data['Date'] = data['Date'].apply(pd.to_datetime)

# to make sure date column is in index column
data.set_index('Date', inplace=True)

# create a dataframe with only the closing price
df = pd.DataFrame({'ds': data.index, 'y': data['Adj Close']})

# fit a linear regression model
X = pd.to_numeric((df['ds'] - df['ds'][0]) / pd.Timedelta(1, unit='D')).values.reshape(-1, 1)
y = df['y'].values.reshape(-1, 1)
model = LinearRegression().fit(X, y)

# make a prediction for the next year
future = pd.DataFrame({'ds': pd.date_range(start=df['ds'].iloc[-1], periods=365, freq='D')})
X_future = pd.to_numeric((future['ds'] - df['ds'][0]) / pd.Timedelta(1, unit='D')).values.reshape(-1, 1)
y_pred = model.predict(X_future)
forecast = pd.DataFrame({'ds': future['ds'], 'y': y_pred.flatten()})

# plot the forecast
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(df['ds'], df['y'], label='Actual')
ax.plot(forecast['ds'], forecast['y'], label='Predicted')
ax.set_xlabel('Date')
ax.set_ylabel('Price ($)')
ax.set_title('Price Forecast for {}'.format(stocks))
ax.legend()
plt.show()



