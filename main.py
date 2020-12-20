import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm

class CalibratedMultidimensionalCompensator(QCAlgorithm):

class CalibratedMultidimensionalCompensator(QCAlgorithm):

    def Initialize(self):
        # Set Stuff
        self.SetCash(100000)
        self.SetStartDate(2017,1,1) 
        self.lookback = 4*365 # Lookback window for history request
        self.lookforwardVal = 10 # How many days into the future to predict data for
        
        self.oil = self.AddCfd("WTICOUSD", Resolution.Daily, Market.Oanda)
        
        self.Debug(self.GetPrediction())
        
    def lookforward(self):
        return self.lookback+self.lookforwardVal
   
    def GetPrediction(self):
        oil_data = self.History(["WTICOUSD"], self.lookback, Resolution.Daily)
        model = sm.tsa.ARIMA(oil_data['close'].values, order=(1, 1, 1)).fit()
        prediction = model.predict(self.lookback, self.lookforward())
        """
        
        """
        return prediction
        
        
    def bullish():
        return (self.GetPrediction().sum())>=0


    def OnData(self, data):
        """
        self.forexClose = data["USDCAD"].Ask.Close
        self.oilClose = data.Bars["WTICOUSD"].Close
        self.Debug(str(self.forexClose))
        """
        exit()
