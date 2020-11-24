import pandas as pd

class CalibratedMultidimensionalCompensator(QCAlgorithm):

    def Initialize(self):
        # Set Stuff
        #self.SetCash(100000)
        self.SetStartDate(2020, 5, 1)
        self.SetEndDate(2020, 5, 2)
        
        # Data Requests
        self.AddForex("USDCAD", Resolution.Daily, Market.Oanda)
        forex = self.AddForex("USDCAD", Resolution.Daily, Market.Oanda).Symbol
        
        self.AddCfd("WTICOUSD", Resolution.Daily, Market.Oanda)
        oil = self.AddCfd("WTICOUSD", Resolution.Daily, Market.Oanda).Symbol
        
        # Oil History Request
        self.history = self.History(oil, 1095)

    def OnData(self, data):
        """
        self.forexClose = data["USDCAD"].Ask.Close
        self.oilClose = data.Bars["WTICOUSD"].Close
        self.Debug(str(self.forexClose))
        """