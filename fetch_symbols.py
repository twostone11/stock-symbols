import requests
import json
import os

def fetch_and_save_symbols(exchange):
    url = f"https://api.nasdaq.com/api/screener/stocks?exchange={exchange}&download=true"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:85.0) Gecko/20100101 Firefox/85.0'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        
        # Extract 'data.rows' similar to 'jq ".data.rows"'
        rows = data.get('data', {}).get('rows', [])
        
        file_name = f"{exchange.lower()}.json"
        file_path = os.path.join(os.getcwd(), file_name)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(rows, f, ensure_ascii=False, indent=4)
        print(f"Successfully fetched and saved {exchange} symbols to {file_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {exchange} symbols: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON for {exchange}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred for {exchange}: {e}")

def analyze_stock_data():
    """分析下载的股票数据文件，统计每个交易所的股票数量"""
    exchanges = ["nasdaq", "amex", "nyse"]
    total_stocks = 0
    
    print("\n" + "="*50)
    print("股票数据分析报告")
    print("="*50)
    
    for exchange in exchanges:
        file_name = f"{exchange.lower()}.json"
        file_path = os.path.join(os.getcwd(), file_name)
        
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                stock_count = len(data)
                total_stocks += stock_count
                
                print(f"{exchange.upper():>6} 交易所: {stock_count:>5} 只股票")
            else:
                print(f"{exchange.upper():>6} 交易所: 文件不存在")
                
        except json.JSONDecodeError as e:
            print(f"{exchange.upper():>6} 交易所: JSON 解析错误 - {e}")
        except Exception as e:
            print(f"{exchange.upper():>6} 交易所: 读取错误 - {e}")
    
    print("-"*50)
    print(f"{'总计':>6}: {total_stocks:>5} 只股票")
    print("="*50)

if __name__ == "__main__":
    exchanges = ["nasdaq", "amex", "nyse"]
    
    # 下载股票数据
    print("正在下载股票数据...")
    for exchange in exchanges:
        fetch_and_save_symbols(exchange)
    
    # 分析股票数据
    analyze_stock_data()