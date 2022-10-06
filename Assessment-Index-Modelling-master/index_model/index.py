import datetime as dt
import pandas as pd
import numpy as np

class IndexModel:
    def __init__(self) -> None:
        self.df = pd.read_csv("data_sources/stock_prices.csv")
        self.df['Date'] = pd.to_datetime(self.df['Date'], format='%d/%m/%Y')
        self.df.set_index('Date', inplace=True)
        
        self.index_series = None

    def calc_index_level(self, start_date: dt.date, end_date: dt.date) -> None:
        # Result
        index_series = pd.Series(index=self.df.index[self.df.index >= pd.Timestamp(2020,1,1)], dtype=float, name='index_level')
        index_series[pd.Timestamp(2020,1,1)] = 100
    
        # Last day of preceding month
        last_date = pd.Timestamp(2019, 12, 31)
    
        # Current date
        cur_date = pd.Timestamp(2020, 1, 1)
    
        # Initial index level
        index_level = 100
    
        # Selected stocks for current month
        first_stk, second_stk, third_stk = self.df.loc[last_date, :].sort_values(ascending=False).index[:3]
    
        # Price of first, second, and third stock
        first_val, second_val, third_val = self.df.loc[cur_date, [first_stk, second_stk, third_stk]]
    
        for idx in index_series.index[1:]:
            # Determine sample stocks
            if idx.year == cur_date.year and idx.month == cur_date.month:
                # Compute index
                cur_date = idx
                index_series[idx] = index_level * (0.5*self.df.loc[idx, first_stk]/first_val + 0.25*self.df.loc[idx, second_stk]/second_val + 0.25*self.df.loc[idx, third_stk]/third_val)
            else:
                cur_date = idx
                # The first date of new month
                # Compute index
                index_series[idx] = index_level * (0.5*self.df.loc[idx, first_stk]/first_val + 0.25*self.df.loc[idx, second_stk]/second_val + 0.25*self.df.loc[idx, third_stk]/third_val)
                # Update index level
                index_level = index_series[idx]
                
            
                # Update stocks
                last_date = pd.Timestamp(cur_date.year, cur_date.month, 1) - pd.Timedelta(days=1)
                last_date = self.df.loc[self.df.index <= last_date, :].iloc[-1].name
                first_stk, second_stk, third_stk = self.df.loc[last_date, :].sort_values(ascending=False).index[:3]
            
                # Update price of first, second, and third stock
                first_val, second_val, third_val = self.df.loc[cur_date, [first_stk, second_stk, third_stk]]

                
        self.index_series = np.round(index_series,2)

    def export_values(self, file_name: str) -> None:
        self.index_series.to_csv(file_name)
