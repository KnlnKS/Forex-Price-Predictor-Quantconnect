import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm

class CalibratedMultidimensionalCompensator(QCAlgorithm):

    def Initialize(self):
        # Set Stuff
        self.SetCash(100000)
        self.SetStartDate(2020,1,1) 
        self.SetEndDate(2020,2,1) 
        self.ticker = "WTICOUSD"
        self.lookback = 4*365 # Lookback window for history request
        self.lookforwardVal = 5 # How many days into the future to predict data for
        self.predVal = 0 # Predicted increase/decrease
        
        self.oil = self.AddCfd("WTICOUSD", Resolution.Daily, Market.Oanda)
        
        
    def getForecast(self):
        oil_data = self.History(["WTICOUSD"], self.lookback, Resolution.Daily)
        model = sm.tsa.ARIMA(oil_data['close'].values, order=(1, 1, 1)).fit()
        prediction = model.forecast()
        return prediction
        
        
    def bullish(self, currentVal, predictedVal):
        return (predictedVal-currentVal)>=0

    
    def OnData(self, data):
        currentPrice = data[self.ticker].Price
        forecast = self.getForecast()
        bullish = self.bullish(currentPrice, forecast[0])
        invested = self.Portfolio["WTICOUSD"].Invested
        currentCash = self.Portfolio.Cash

        if not invested and bullish:
            self.MarketOrder("WTICOUSD", 1000)
        elif invested and bullish:
            self.MarketOrder("WTICOUSD", 1000)
        elif invested and not bullish:
            self.MarketOrder("WTICOUSD", -1000)
        
        self.lookback+=1
