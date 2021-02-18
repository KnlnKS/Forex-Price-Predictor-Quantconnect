import pandas as pd
import statsmodels.api as sm


class CalibratedMultidimensionalCompensator(QCAlgorithm):

    def Initialize(self):
        # Setup
        self.SetCash(100000)
        self.SetStartDate(2020, 1, 30)
        self.SetEndDate(2020, 4, 1)
        self.ticker = "WTICOUSD"
        self.order = (1, 1, 6)  # ARIMA model config values
        self.lookback = 4 * 365  # Lookback window for history request
        # self.lookback = 50
        self.lookforwardVal = 5  # How many days into the future to predict data for
        self.predVal = 0  # Predicted increase/decrease
        self.oil = self.AddCfd("WTICOUSD", Resolution.Daily, Market.Oanda)

    def getForecast(self):
        lfv = self.lookforwardVal
        oil_data = self.History([self.ticker], self.lookback, Resolution.Daily)
        model = sm.tsa.ARIMA(oil_data['close'].values, order=self.order).fit()

        if lfv == 1:
            prediction = model.forecast()[0]
        else:
            prediction = model.forecast(lfv)[0]

        return prediction

    def OnData(self, data):
        currentPrice = data[self.ticker].Price  # Current Oil Price
        invested = self.Portfolio[self.ticker].Invested  # Oil owned
        currentCash = self.Portfolio.Cash  # Current cash on hand
        currentUProfit = self.Portfolio.TotalUnrealizedProfit
        oilHoldings = self.Portfolio[self.ticker].Quantity  # Amount of oil owned
        forecast = self.getForecast()

        maximum = max(forecast[0], forecast[1], forecast[2], forecast[3], forecast[4])
        minimum = min(forecast[0], forecast[1], forecast[2], forecast[3], forecast[4])

        if (maximum - currentPrice) > (currentPrice - minimum):

            if maximum - currentPrice < 0.001 * currentPrice:
                pass
            elif 0.001 * currentPrice <= maximum - currentPrice < 0.003 * currentPrice:
                self.MarketOrder("WTICOUSD", ((0.1 * currentCash) // currentPrice))
            elif 0.003 * currentPrice <= maximum - currentPrice < 0.005 * currentPrice:
                self.MarketOrder("WTICOUSD", ((0.2 * currentCash) // currentPrice))
            else:
                self.MarketOrder("WTICOUSD", ((0.4 * currentCash) // currentPrice))

        else:
            if currentPrice - minimum < 0.001 * currentPrice:
                pass
            elif 0.001 * currentPrice <= currentPrice - minimum < 0.003 * currentPrice:
                self.MarketOrder("WTICOUSD", ((-0.1 * currentCash) // currentPrice))
            elif 0.003 * currentPrice <= currentPrice - minimum < 0.005 * currentPrice:
                self.MarketOrder("WTICOUSD", ((-0.2 * currentCash) // currentPrice))
            else:
                self.MarketOrder("WTICOUSD", ((-0.4 * currentCash) // currentPrice))

        if currentPrice - minimum > (0.01 * currentPrice):
            self.Liquidate("WTICOUSD")

        self.lookback += 1