# Pandas related imports
import pandas as pd





class TechnicalAnalysis:
    def __init__(self, ticker: str) -> None:
        self.ticker = ticker

    '''------------------------------------'''
    '''------------------------------------ Indicators ------------------------------------'''
    '''------------------------------------'''
    def get_RSI(self, df:pd.DataFrame=pd.DataFrame() , period_length:int=14) -> pd.DataFrame:
        '''
        df: Pandas dataframe containing candle data of various intervals (daily/hourly/minute)
        period_length: The period represents the number of candles to use for the calculation. RSI typically uses 14 periods. 
                       If working with minute data, it will take 14 1-minute candles. If working with hourly data, it will take 14 1-hour candles, and so on. 


        RSI Guide:
        - >70 = Overbought (sell)
        - <30 = Oversold (buy)
        '''

        

        # Calculate the price change between the close of each candle.
        delta = df['close'].diff(1) 
        
        # Make a copy of delta and store positive changes in 'positive' and negative changes in 'negative'
        positive = delta.copy()
        negative = delta.copy()

        # Set values of negative changes to 0 within 'positive' dataframe. 
        # This is because in the positive dataframe, we are only concerned with positive changes. 
        positive[positive < 0] = 0
        # Set values of positive changes to 0 within 'negative' dataframe. 
        negative[negative > 0] = 0

        # Calculate the average gain.
        average_gain = positive.rolling(window=period_length).mean()
        # Calculate the average loss. Take absolute value since we do not want negative numbers when calculating the relative strength. 
        average_loss = abs(negative.rolling(window=period_length).mean())

        relative_strength = average_gain / average_loss
        # Formula for relative strength index. 
        rsi = 100.0 - (100.0 / (1.0 + relative_strength))

        df['RSI'] = rsi

        return df         
    '''------------------------------------'''
    def get_MACD(self, df:pd.DataFrame, short_period=12, long_period=26, macd_period=9) -> pd.DataFrame:
        '''
        short_period: Number of candles to use for the short term exponential moving average.
        long_period: Number of candles to use for the long term exponential moving average.
        macd_period: Number of periods to use for the MACD exponential moving average.
        '''
        
        # Get the exponential moving average (ema) for both short and long term periods. 
        short_ema = df.close.ewm(span=short_period, adjust=False).mean()
        long_ema = df.close.ewm(span=long_period, adjust=False).mean()

        # The macd is calculated by taking the difference between the short ema and long ema. 
        macd = short_ema - long_ema
        signal_line = macd.ewm(span=macd_period, adjust=False).mean()

        # Calculate historgram
        histogram = macd - signal_line

        df['MACD'] = macd
        df['Signal'] = signal_line 
        df['Histogram'] = histogram
        return df

    '''------------------------------------'''         
    '''------------------------------------'''
    '''------------------------------------'''         
    '''------------------------------------'''
    '''------------------------------------'''         
    '''------------------------------------'''
    '''------------------------------------'''         
    '''------------------------------------'''
    '''------------------------------------'''         
    '''------------------------------------'''
    '''------------------------------------'''         
    '''------------------------------------'''
    '''------------------------------------'''         
    '''------------------------------------'''
