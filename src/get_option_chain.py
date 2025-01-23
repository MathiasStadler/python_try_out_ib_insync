# FROM HERE
# https://www.pyquantnews.com/the-pyquant-newsletter/download-options-chains-data-ibkr-api

from ib_insync import *
from ibapi.common import TickerId, SetOfFloat, SetOfString, MarketDataTypeEnum


util.startLoop()
ib = IB()
ib.connect('127.0.0.1', 7496, clientId=13)

ib.reqMarketDataType(MarketDataTypeEnum.DELAYED)

nvda = Stock("NVDA", "SMART", "USD")
# nvda = Stock("NVDA", "", "USD")
ib.qualifyContracts(nvda)
[ticker] = ib.reqTickers(nvda)
nvdaValue = ticker.marketPrice()

print('nvdaValue=>' + str(nvdaValue ))

chains = ib.reqSecDefOptParams(nvda.symbol, "", nvda.secType, nvda.conId)

chain = next(c for c in chains if c.tradingClass == "NVDA" and c.exchange == "SMART")

strikes = [
    strike for strike in chain.strikes
    # if strike % 5 == 0
    # and nvdaValue - 20 < strike < nvdaValue + 20
]

expirations = sorted(exp for exp in chain.expirations)[:3]
# rights = ["C", "P"]
rights = [ "P"]

contracts = [
    Option("NVDA", expiration, strike, right, "CBOE", tradingClass="NVDA")
    for right in rights
    for expiration in expirations
    for strike in strikes
]


contracts = ib.qualifyContracts(*contracts)
tickers = ib.reqTickers(*contracts)


contractData = [
    (
        
        t.contract.lastTradeDateOrContractMonth, 
        t.contract.strike, 
        t.contract.right,
        t.time,
        t.close,
        nvdaValue,

    )

    for t in tickers

]


fields = [
    "expiration", 
    "strike", 
    "right", 
    "time", 
    "undPrice",
    "close", 
]


output = util.df([dict(zip(fields, t)) for t in contractData])

print(output)