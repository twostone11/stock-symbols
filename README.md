# Stock Symbols
A list of all US stock tickers fetch daily from NASDAQ.

## How it works
Github Action will run nightly to fetch the latest data from NASDAQ and directly commit to this repository.

You can also run the Python script locally to fetch the latest data:

### Quick Setup (推荐)
**Windows:**
```bash
setup_env.bat
```

**Linux/Mac:**
```bash
chmod +x setup_env.sh
./setup_env.sh
```

### Manual Setup
1. 创建虚拟环境:
   ```bash
   python -m venv venv
   ```

2. 激活虚拟环境:
   - **Windows:** `venv\Scripts\activate`
   - **Linux/Mac:** `source venv/bin/activate`

3. 安装依赖:
   ```bash
   pip install -r requirements.txt
   ```

4. 运行脚本:
   ```bash
   python fetch_symbols.py
   ```

## Data source
Stock data is fetch from [NASDAQ](https://www.nasdaq.com/market-activity/stocks/screener). Data from three US Exchanges are available:
* NASDAQ: nasdaq.json
* NYSE: nyse.json
* AMEX: amex.json
