import statsmodels.api as sm

class OilyAlgo(QCAlgorithm):

    def Initialize(self):
        # Constants
        self.ticker = "WTICOUSD" # Ticker
        self.lookback = 4*365 # Lookback window for history request
        self.lookforwardVal = 5 # How many days into the future to predict data for
        self.order = (1, 1, 6) # ARIMA model config values
        
        # Algorithm Parameters
        self.SetCash(100000) # Starting Cash
        self.SetStartDate(2020,1,1) # Beginning Date of Algo
        self.SetEndDate(2020,2,1)  # End Date of Algo
        self.oil = self.AddCfd(self.ticker, Resolution.Daily, Market.Oanda)
        
        
    def getForecast(self):
        lfv = self.lookforwardVal
        oil_data = self.History([self.ticker], self.lookback, Resolution.Daily)
        model = sm.tsa.ARIMA(oil_data['close'].values, order=self.order).fit()
        
        if lfv == 1:
            prediction = model.forecast()[0]
        else:
            prediction = model.forecast(lfv)[0][lfv-1]
        
        return prediction
        
        
    def bullish(self, currentVal, predictedVal):
        return (predictedVal-currentVal)>=0

    
    def OnData(self, data):
        currentPrice = data[self.ticker].Price # Current Oil Price
        forecast = self.getForecast() # Get forecast
        bullish = self.bullish(currentPrice, forecast) # Bullish?
        invested = self.Portfolio[self.ticker].Invested # Oil owned?
        currentCash = self.Portfolio.Cash # Current cash on hand
        oilHoldings = self.Portfolio[self.ticker].Quantity # Amount of oil owned

        if bullish:
            self.MarketOrder(self.ticker, 1000)
        elif invested and not bullish:
            self.MarketOrder("WTICOUSD", -1000)
        
        self.lookback+=1
