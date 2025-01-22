# path step by step for this project

## detect os version

```bash
Debian 12.8 
```

## detect python version


```bash
python3 --version
Python 3.11.2
```


## create venv

[install venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html)

```bash
python3 -m venv .venv
```

## enter .venv

```bash
source .venv//bin/activate
```

## exit/leave venv

```bash
deactivate
```

## install packages - command  inside .venv

```bash
pip3 install ib_insync
```

## show what is already installed inside .venv - command inside .venv

```bash
pip3 list
```


> [!NOTE]
> [Multi line to new files](https://stackoverflow.com/questions/17115664/can-linux-cat-command-be-used-for-writing-text-to-file/57051604#57051604)
>
>```bash
>cat > outfile.txt <<EOF
>some text
>to save
>EOF
>```


## first tws connect

```python
cat > workspace/first_connect_tws.py << EOF
from ib_insync import *
util.startLoop()

ib = IB()
ib.connect('127.0.0.1', 7496, clientId=12)

# python3 workspace/first_connect_tws.py 
EOF
```

## Retrieve the current market price of Nvidia stock

```python
cat > workspace/retrieve_price_nvda.py << EOF
from ib_insync import *
util.startLoop()

ib = IB()
ib.connect('127.0.0.1', 7496, clientId=12)

nvda = Stock("NVDA", "SMART", "USD")
ib.qualifyContracts(nvda)
[ticker] = ib.reqTickers(nvda)
nvdaValue = ticker.marketPrice()

# python3 workspace/retrieve_price_nvda.py
EOF
```

## [better example](https://stackoverflow.com/questions/71040117/part-of-requested-market-data-is-not-subscribed-ib-insync)
```bash
cat >workspace/retrieve_option_chain.py << EOF
# FROM HERE
# https://stackoverflow.com/questions/71040117/part-of-requested-market-data-is-not-subscribed-ib-insync
import time

from ib_insync import *
import pandas as pd
from configparser import ConfigParser
from ibapi.common import TickerId, SetOfFloat, SetOfString, MarketDataTypeEnum

config = ConfigParser()


# TWs 7497, IBGW 4001

def get_chain(ib,ticker, exp_list):
    exps = {}
    df = pd.DataFrame(columns=['strike', 'kind', 'close', 'last'])
    pd.set_option('display.max_rows', None)  # `None` means displaying all rows
    pd.set_option('display.max_columns', None)  # `None` means displaying all columns
    for i in exp_list:
        ib.sleep()

        cds = ib.reqContractDetails(Option(ticker, i, exchange='SMART'))
        options = [cd.contract for cd in cds]
        tickers = [t for i in range(0, len(options), 100)

                   for t in ib.reqTickers(*options[i:i + 100])]

        for x in tickers:
            df = df._append(
                {'strike': x.contract.strike, 'kind': x.contract.right, 'close': x.close, 'last': x.last, 'bid': x.bid,
                 'ask': x.ask, 'mid': (x.bid + x.ask) / 2, 'volume': x.volume}, ignore_index=True)
            exps[i] = df

    return exps


def get_individual(ib,ticker, exp, strike, kind):

    cds = ib.reqContractDetails(Option(ticker, exp, strike, kind, exchange='SMART'))
    options = [cd.contract for cd in cds]
    tickers = [t for i in range(0, len(options), 100) for t in ib.reqTickers(*options[i:i + 100])]

    con = {'strike': tickers[0].contract.strike, 'kind': tickers[0].contract.right, 'close': tickers[0].close,
           'last': tickers[0].last, 'bid': tickers[0].bid, 'ask': tickers[0].ask, 'volume': tickers[0].volume}
    return con


def main():
    with IB().connect('127.0.0.1', 7496) as ib:
        #ib.reqMarketDataType(3)
        ib.reqMarketDataType(MarketDataTypeEnum.DELAYED)
        time.sleep(1)
        print(get_chain(ib,"AAPL", ["20250124"]))


if __name__ == '__main__':
    main()

# python3 workspace/retrieve_option_chain.py
EOF
```
