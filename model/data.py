
import pandas as pd
import pandas_datareader as web
import datetime
import matplotlib.pyplot as plt
import io



class data():
    
    def __init__(self, symbol, from_str, to_str, variable):
        self.symbol = symbol
        self.from_str = from_str
        self.to_str = to_str
        self.variable = variable
        
    
    def get_dates(self):
        self.from_dt = datetime.datetime.strptime(self.from_str, '%Y-%m-%d')
        
        if len(self.to_str) > 1:
            self.to_dt = datetime.datetime.strptime(self.to_str, '%Y-%m-%d')
        else:
            self.to_dt = datetime.datetime.now()
    
    
    def get_data(self):
        dtf = web.DataReader(name=self.symbol, data_source="yahoo", 
                             start=self.from_dt, end=self.to_dt, 
                             retry_count=10)
        self.ts = dtf[self.variable]
    
    
    def plot_ts(self, plot_ma=True, plot_intervals=True, window=30, figsize=(20,13)):
        rolling_mean = self.ts.rolling(window=window).mean()
        rolling_std = self.ts.rolling(window=window).std()
        plt.figure(figsize=figsize)
        plt.title(self.ts.name)
        if plot_ma:
            plt.plot(rolling_mean, 'g', label='MA'+str(window))
        if plot_intervals:
            lower_bound = rolling_mean - (1.96 * rolling_std)
            upper_bound = rolling_mean + (1.96 * rolling_std)
            plt.plot(upper_bound, 'r--', label='Upper bound / Lower bound')
            plt.plot(lower_bound, 'r--')
        plt.plot(self.ts[window:], label='Actual values', linewidth=3)
        plt.legend(loc='best')
        plt.grid(True)
        bytes_image = io.BytesIO()
        plt.savefig(bytes_image, format='png')
        bytes_image.seek(0)
        return bytes_image