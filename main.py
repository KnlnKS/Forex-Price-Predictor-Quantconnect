import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm

class CalibratedMultidimensionalCompensator(QCAlgorithm):

    def Initialize(self):
        # Set Stuff
        #self.SetCash(100000)
        self.SetStartDate(2017,1,1) 
        start_time = datetime(2019, 1, 5) # start datetime for history call
        end_time = datetime(2019, 12, 3) # end datetime for history call
        
        oil = self.AddCfd("WTICOUSD", Resolution.Daily, Market.Oanda)
        oil_data = self.History(['WTICOUSD'], 730, Resolution.Daily)
        
        model = sm.tsa.ARIMA(oil_data['close'].values, order=(1, 1, 1))
        prediction = model.fit().predict(730, 740)
        self.Debug(prediction)
        self.Debug(oil_data['close'].values[:10])


    def OnData(self, data):
        """
        self.forexClose = data["USDCAD"].Ask.Close
        self.oilClose = data.Bars["WTICOUSD"].Close
        self.Debug(str(self.forexClose))
        """
        exit()
