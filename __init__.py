from DataCollection.cryptodata import CryptoData





def __init__():
    ticker = "BTC"
    market = "USD"
    exchange = "Kraken"

    # Create 'CryptoData' object and assign relevant variables. 
    cd = CryptoData(ticker=ticker, market=market, exchange=exchange)
    
    data = cd.get_hourly_data(limit=1000, aggregate=1)

    cd.find_spikes(data)
    print(f'Data: {data}')

    






__init__()
