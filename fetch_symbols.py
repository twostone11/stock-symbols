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

if __name__ == "__main__":
    exchanges = ["nasdaq", "amex", "nyse"]
    for exchange in exchanges:
        fetch_and_save_symbols(exchange)