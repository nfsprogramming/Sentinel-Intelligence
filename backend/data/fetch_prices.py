import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def fetch_historical_prices(ticker_symbol: str, period: str = "2y", interval: str = "1d"):
    """
    Fetches historical price data for a given ticker or cryptocurrency.
    
    Args:
        ticker_symbol: The stock or crypto symbol (e.g., 'AAPL', 'BTC-USD').
        period: The data period (e.g., '1y', '2y', 'max').
        interval: The data interval (e.g., '1d', '1h').
    
    Returns:
        DataFrame containing the historical data.
    """
    print(f"Fetching data for {ticker_symbol}...")
    try:
        ticker = yf.Ticker(ticker_symbol)
        history = ticker.history(period=period, interval=interval)
        
        if history.empty:
            print(f"No data found for {ticker_symbol}.")
            return None
            
        # Reset index to make Date a column
        history.reset_index(inplace=True)
        
        # Ensure Date is timezone-naive/normalized if needed, but keeping it simple for now
        print(f"Successfully fetched {len(history)} records for {ticker_symbol}.")
        return history
    except Exception as e:
        print(f"Error fetching data for {ticker_symbol}: {e}")
        return None

if __name__ == "__main__":
    # Test with Bitcoin
    df = fetch_historical_prices("BTC-USD")
    if df is not None:
        print(df.head())
        # Save to CSV for inspection
        df.to_csv("btc_prices_test.csv", index=False)
