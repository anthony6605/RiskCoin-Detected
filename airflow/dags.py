from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta
import json
import os
import sys
project_root = "/Users/anthony/Desktop/Project Storage /RiskCoin-Detected"
if project_root not in sys.path:
    sys.path.insert(0, project_root)

default_args = {
    'owner': 'data-engineering',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'daily_extract',
    default_args=default_args,
    description='Extract raw crypto data from APIs',
    schedule='0 */6 * * *',  # Every 6 hours
    catchup=False,
    tags=['extract', 'crypto'],
)

def extract_coingecko_data(**context):
    """Extract data from CoinGecko API"""
    from source.extract_coingecko import CoinGeckoClient
    import json
    import os
    
    try:
        client = CoinGeckoClient()
        coins = client.fetch_market_data(per_page=25)
        
        if not coins:
            raise ValueError("No data received from CoinGecko API")
        
        # Store raw data locally
        data_dir = "/Users/anthony/Desktop/Project Storage /RiskCoin-Detected/data"
        os.makedirs(f"{data_dir}/raw/coingecko", exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{data_dir}/raw/coingecko/coins_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(coins, f, indent=2)
        
        print(f"✓ Successfully extracted {len(coins)} coins from CoinGecko")
        return len(coins)
        
    except Exception as e:
        print(f"✗ Error extracting CoinGecko data: {e}")
        raise

def extract_binance_data(**context):
    """Extract data from Binance API"""
    from source.extracts_binance import BinanceClient
    import json
    import os
    
    try:
        client = BinanceClient()
        orderbook = client.fetch_orderbook('BTCUSDT', limit=25)
        
        if not orderbook or not orderbook.get('bids') or not orderbook.get('asks'):
            raise ValueError("No valid orderbook data received from Binance API")
        
        # Store raw data locally
        data_dir = "/Users/anthony/Desktop/Project Storage /RiskCoin-Detected/data"
        os.makedirs(f"{data_dir}/raw/binance", exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{data_dir}/raw/binance/orderbook_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(orderbook, f, indent=2)
        
        total_orders = len(orderbook.get('bids', [])) + len(orderbook.get('asks', []))
        print(f"✓ Successfully extracted {total_orders} orders from Binance")
        return total_orders
        
    except Exception as e:
        print(f"✗ Error extracting Binance data: {e}")
        raise

# Define tasks
extract_cg = PythonOperator(
    task_id='extract_coingecko',
    python_callable=extract_coingecko_data,
    dag=dag,
)

extract_binance = PythonOperator(
    task_id='extract_binance',
    python_callable=extract_binance_data,
    dag=dag,
)

# Set task dependencies - CoinGecko runs first, then Binance
extract_cg >> extract_binance

