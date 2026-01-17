import requests
import os
import time
from dotenv import load_dotenv

# Load env vars
load_dotenv()

class AlphaVantageSentiment:
    def __init__(self):
        self.api_key = os.getenv("ALPHA_VANTAGE_KEY")
        self.base_url = "https://www.alphavantage.co/query"

    def get_sentiment(self, ticker="BTC"):
        if not self.api_key:
            print("Error: ALPHA_VANTAGE_KEY not found.")
            return 0.0, "Neutral", "No Data"

        # Map to Alpha Vantage format (e.g. CRYPTO:BTC)
        symbol = f"CRYPTO:{ticker}" if ticker in ["BTC", "ETH"] else ticker
        
        params = {
            "function": "NEWS_SENTIMENT",
            "tickers": symbol,
            "apikey": self.api_key,
            "sort": "LATEST",
            "limit": 50
        }

        try:
            response = requests.get(self.base_url, params=params)
            data = response.json()
            
            if "feed" not in data:
                # Handle API limit or error
                print(f"Alpha Vantage API Error or Limit Reached: {data.get('Note', 'Unknown Error')}")
                return 0.0, "Neutral", "API Limit"

            feed = data["feed"]
            if not feed:
                return 0.0, "Neutral", "No News"

            # Calculate average sentiment score
            total_score = 0
            count = 0
            latest_headline = feed[0]["title"]
            
            for article in feed:
                # 'ticker_sentiment' is a list
                for tick in article.get("ticker_sentiment", []):
                    # Simple matching or just take overall sentiment if available
                    # Alpha Vantage gives 'overall_sentiment_score' for the article too
                    # Let's use overall_sentiment_score of the article relevant to this ticker
                    pass
                
                # Use article level sentiment
                score = float(article.get("overall_sentiment_score", 0))
                total_score += score
                count += 1
            
            avg_score = total_score / count if count > 0 else 0
            
            # Label
            if avg_score >= 0.15:
                label = "Bullish"
            elif avg_score >= 0.35:
                label = "Very Bullish"
            elif avg_score <= -0.15:
                label = "Bearish"
            elif avg_score <= -0.35:
                label = "Very Bearish"
            else:
                label = "Neutral"
                
            return avg_score, label, latest_headline

        except Exception as e:
            print(f"Failed to fetch Alpha Vantage sentiment: {e}")
            return 0.0, "Neutral", "Error"

if __name__ == "__main__":
    # Test
    av = AlphaVantageSentiment()
    score, label, headline = av.get_sentiment("BTC")
    print(f"Score: {score}, Label: {label}")
    print(f"Headline: {headline}")
