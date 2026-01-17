import yfinance as yf
import pandas as pd
import os
import requests
from dotenv import load_dotenv

load_dotenv()

class StockDataManager:
    def __init__(self):
        self.alpha_key = os.getenv("ALPHA_VANTAGE_KEY")
        
    def fetch_data(self, ticker, start_date="2015-01-01"):
        """
        Fetch OHLCV data from Yahoo Finance, fallback to Alpha Vantage.
        """
        # Try Yahoo Finance first (more history usually available easily)
        print(f"Fetching data for {ticker} via Yahoo Finance...")
        try:
            df = yf.download(ticker, start=start_date, progress=False)
            if not df.empty:
                # Cleanup multi-level columns if any (yf does this sometimes)
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(0)
                
                # Verify we have 'Close'
                if 'Close' in df.columns:
                    print(f"Successfully fetched {len(df)} records from Yahoo.")
                    return df
        except Exception as e:
            print(f"Yahoo fetch failed: {e}")
            
        # Fallback to Alpha Vantage
        print(f"Fallback: Fetching from Alpha Vantage...")
        if self.alpha_key:
            try:
                # Alpha Vantage TIME_SERIES_DAILY
                url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&outputsize=full&apikey={self.alpha_key}&datatype=csv"
                df = pd.read_csv(url)
                df['Date'] = pd.to_datetime(df['timestamp'])
                df.set_index('Date', inplace=True)
                df.sort_index(inplace=True)
                # Filter start date
                df = df[df.index >= start_date]
                
                # AV uses lowercase 'close', rename to Title Case
                df.rename(columns={'close': 'Close', 'open': 'Open', 'high': 'High', 'low': 'Low', 'volume': 'Volume'}, inplace=True)
                
                print(f"Successfully fetched {len(df)} records from Alpha Vantage.")
                return df
            except Exception as e:
                print(f"Alpha Vantage fetch failed: {e}")
        
        return None
