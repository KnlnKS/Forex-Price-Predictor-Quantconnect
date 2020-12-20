import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm

class CalibratedMultidimensionalCompensator(QCAlgorithm):

    def Initialize(self):
        # Set Stuff
        self.SetCash(100000)
        self.SetStartDate(2017,1,1) 
        self.SetEndDate(2017,12,1) 
        self.ticker = "WTICOUSD"
        self.lookback = 4*365 # Lookback window for history request
        self.lookforwardVal = 5 # How many days into the future to predict data for
        self.predVal = 0 # Predicted increase/decrease
        
        self.oil = self.AddCfd("WTICOUSD", Resolution.Daily, Market.Oanda)

    
    def lookforward(self):
        return self.lookback+self.lookforwardVal
   
   
    def getPrediction(self):
        oil_data = self.History(["WTICOUSD"], self.lookback, Resolution.Daily)
        model = sm.tsa.ARIMA(oil_data['close'].values, order=(1, 1, 1)).fit()
        prediction = model.predict(self.lookback, self.lookforward())
        return prediction
        
        
    def bullish(self):
        return (self.getPrediction().sum())>=0
        
    
    def increase(self):
        curr = self.getPrediction().sum()
        return True


    def OnData(self, data):
        if not self.Portfolio["WTICOUSD"].Invested and self.bullish():
            self.MarketOrder("WTICOUSD", 100)
        elif self.Portfolio["WTICOUSD"].Invested and not self.bullish():
            self.MarketOrder("WTICOUSD", -100)
        
        self.lookback+=1
