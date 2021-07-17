# Stock Price Prediction Using LSTM Model
In this project I used a Keras Long Short-Term Memory model to solve a sequence prediction problem - predict the future behavior of stock prices.

I first chose to zoom in on Apple stock data over a 10 year period (from 1 Jan 2011 to 17 July 2021) from Yahoo Finance API.

I'll focus on adjusted close. This price takes into account dividends, stock splits and any rights offerings, as well as any factors that happen after markets close.
As a result, this is the feature which we would attempt to predict as it would be more reliable than the other metrics that are susceptible to non-market forces.

I have trained my model by taking the prices from the previous 30 days and predicting the 31st one.

### Result

![image](https://user-images.githubusercontent.com/69782094/126037314-3f1c182a-247c-4385-b909-0ff85fbeb24d.png)
