# Web requests
import requests


# Data storage and manipulation
import pandas as pd

# Date access and manipulation
import datetime as dt
"https://galea.medium.com/cryptocompare-api-quick-start-guide-ca4430a484d4"





class CryptoData:
    def __init__(self, ticker:str, market:str="USD", exchange="Coinbase") -> None:
        '''
        ticker: The ticker symbol of the crypto asset
        market: The market that the asset is trading in. Ex: In U.S. markets it will use "USD".
        In European markets it will use "EUR".
        exchange: What crypto-exchange to source data from.'''
        self.ticker = ticker.upper()
        self.market = market.upper()
        self.exchange = exchange


        # Dataframes for different time frames.
        self.daily_data = pd.DataFrame()
        self.hourly_data = pd.DataFrame()
        self.minute_data = pd.DataFrame()


    '''------------------------------------'''
    def set_daily_data(self, all_data:bool=True, limit:int=1, aggregate:int=1, exchange:str = ''):
        '''
        all_data: If "True" all data will be requested.
        limit: limit the amount of data retrieved.
        
        exchange: exchange to retrieve data from.
        time_delta: The length of the candle.  '''
        
        
        url = f'https://min-api.cryptocompare.com/data/histoday?fsym={self.ticker}&tsym={self.market}&limit={limit}&aggregate={aggregate}'

        if exchange:
            url += f"&e={exchange}"
        if all_data:
            url += '&allData=true'

        page = requests.get(url)
        data = page.json()['Data']
        df = pd.DataFrame(data)
        df = self.format_dataframe(df=df)
        self.daily_data = df

    '''------------------------------------'''
    def get_daily_data(self, all_data:bool=True, limit:int=1, aggregate:int=1, exchange:str = ''):
        if self.daily_data.empty:
            self.set_daily_data(all_data=all_data, limit=limit, aggregate=aggregate, exchange=exchange)
        return self.daily_data
    '''------------------------------------'''         
    '''------------------------------------'''
    def set_hourly_data(self, limit:int=1, aggregate:int=1, exchange:str='', time_delta:int=1):
        '''
        all_data: If "True" all data will be requested.
        limit: limit the amount of data retrieved.
        
        exchange: exchange to retrieve data from.
        time_delta: The length of the candle.  '''
        time_delta = 1

        url = f"https://min-api.cryptocompare.com/data/histohour?fsym={self.ticker}&tsym={self.market}&limit={limit}&aggregate={aggregate}"

        if exchange:
            url += f"&e={exchange}"
        page = requests.get(url)
        data = page.json()['Data']
        df = pd.DataFrame(data)
        # Format timestamps to dates.
        df = self.format_dataframe(df=df)
        self.hourly_data = df

    '''------------------------------------'''
    def get_hourly_data(self, limit:int=1, aggregate:int=1, exchange:str=''):
        if self.hourly_data.empty:
            self.set_hourly_data(limit=limit, aggregate=aggregate, exchange=exchange)
        return self.hourly_data
    '''------------------------------------'''
    def set_minute_data(self, limit:int, aggregate:int, exchange:str='') -> None:
        url = f"https://min-api.cryptocompare.com/data/histominute?fsym={self.ticker}&tsym={self.market}&limit={limit}&aggregate={aggregate}"
        if exchange:
            url += f"&e={exchange}"
        page = requests.get(url)
        data = page.json()['Data']
        df = pd.DataFrame(data)
        df = self.format_dataframe(df=df)
        self.minute_data = df
        
    '''------------------------------------'''
    def get_minute_data(self, limit:int, aggregate:int, exchange:str=''):
        if self.minute_data.empty:
            self.set_minute_data(limit=limit, aggregate=aggregate, exchange=exchange)
        return self.minute_data

    


    '''------------------------------------ Strategies ------------------------------------'''
    '''------------------------------------'''
    def find_spikes(self, df: pd.DataFrame, spike_sensitivity:float=20) -> pd.DataFrame:
        
        spikes = []
        index = 0 
        for i in df.iterrows():
            if index == 0:
                pass
            else:
                # Get the current row and the previous row.
                cur_candle = df.iloc[index]
                prev_candle = df.iloc[index-1]
                # Compare the percentage change between the closing prices of the current and previous candle. 
                pct_change = ((cur_candle['close'] / prev_candle['close']) - 1) * 100
                # If the percentage change calculated is higher than 'spike_sensitivity' it will be added to the list. 
                if pct_change > spike_sensitivity:
                    spikes.append(i)
                    spikes.append(prev_candle)
                
            index += 1
        
        return spikes
    '''------------------------------------'''
    '''------------------------------------'''
    '''------------------------------------'''
    '''------------------------------------'''
    '''------------------------------------ Utilities ------------------------------------'''
    '''------------------------------------'''
    def format_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        # Convert timestamps to a readable format. 
        df['time'] = [dt.datetime.fromtimestamp(d) for d in df.time]
        #df = df[::-1].reset_index(drop=True)
        return df
    '''------------------------------------'''
    '''------------------------------------'''
    '''------------------------------------'''
    '''------------------------------------'''
    '''------------------------------------'''
