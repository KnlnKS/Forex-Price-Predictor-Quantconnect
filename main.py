import matplotlib.pyplot as plt
import pandas as pd
import statsmodels as sm

class CalibratedMultidimensionalCompensator(QCAlgorithm):

    def Initialize(self):
        # Set Stuff
        #self.SetCash(100000)
        start_time = datetime(2019, 1, 5) # start datetime for history call
        end_time = datetime(2019, 12, 3) # end datetime for history call
        
        oil = self.AddCfd("WTICOUSD", Resolution.Daily, Market.Oanda).Symbol
        oil_data = self.History(self.Symbol('WTICOUSD'), start_time, end_time)
        self.Debug(oil_data.head())
        model = sm.tsa.arima_model.ARIMA(oil_data['Close'].values, order=(1, 1, 5))
        res = model.fit()
        
        start_time = datetime(2019, 12, 4) # start datetime for history call
        end_time = datetime(2019, 12, 17) # end datetime for history call
        
        predction = res.predict(len(oil_data['Close'].values), (len(oil_data['Close'].values)+10))
        
        self.Debug(predction)

    def OnData(self, data):
        """
        self.forexClose = data["USDCAD"].Ask.Close
        self.oilClose = data.Bars["WTICOUSD"].Close
        self.Debug(str(self.forexClose))
        """
        exit()
