# Stock Symbols
A list of all US stock tickers fetch daily from NASDAQ.

## How it works
Github Action will run nightly to fetch the latest data from NASDAQ and directly commit to this repository.

## Data source
Stock data is fetch from NASDAQ: Data source: https://www.nasdaq.com/market-activity/stocks/screener
Data from all three major US Exchanges are available:
* NASDAQ: nasdaq.json
* NYSE: nyse.json
* AMEX: amex.json
