import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm

class CalibratedMultidimensionalCompensator(QCAlgorithm):

    def Initialize(self):
        # Set Stuff
        self.SetCash(100000)
        self.SetStartDate(2020,1,1) 
        self.SetEndDate(2020,4,1) 
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
        self.Debug(prediction.sum())
        return prediction
        
    def bullish(self):
        return (self.getPrediction().sum())>=0

    
    def increase(self):
        curr = self.getPrediction().sum()
        
        return True
        
        
    def wow(self, pred, bullish):
        if bullish:    
            if pred>0.20:
                return 0.20
            elif pred>0.10:
                return 0.10
        else:
            if pred<-0.20:
                return 0.20
            elif pred<-0.10:
                return 0.10
        return 0.05 

    
    def OnData(self, data):
        pred = self.getPrediction().sum()
        bullish = self.bullish()
        if -0.01<pred<0.01:
            pass
        elif not self.Portfolio["WTICOUSD"].Invested and bullish:
            self.MarketOrder("WTICOUSD", 2000)
        elif self.Portfolio["WTICOUSD"].Invested and bullish:
            multiplier = self.wow(pred, bullish)
            self.MarketOrder("WTICOUSD", 500)
        elif self.Portfolio["WTICOUSD"].Invested and not bullish:
            multiplier = self.wow(pred, bullish)
            self.MarketOrder("WTICOUSD", -1000)
        
        self.lookback+=1
