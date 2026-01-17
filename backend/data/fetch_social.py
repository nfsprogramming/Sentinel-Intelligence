import os
import praw
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

def fetch_reddit_posts(subreddit_name: str, limit: int = 100, search_query: str = None):
    """
    Fetches hot posts from a subreddit using PRAW.
    Requires REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET in .env
    """
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = os.getenv("REDDIT_USER_AGENT", "my_bot_v1")

    if not client_id or not client_secret or client_id == "your_client_id":
        print("Warning: Reddit API credentials not found. Returning mock data.")
        return get_mock_social_data()

    try:
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
        
        subreddit = reddit.subreddit(subreddit_name)
        posts_data = []

        # Decide whether to search or just get hot posts
        if search_query:
            # searching recent posts
            iterator = subreddit.search(search_query, sort='new', limit=limit)
        else:
            iterator = subreddit.hot(limit=limit)

        for post in iterator:
            posts_data.append({
                "source": "reddit",
                "id": post.id,
                "created_utc": datetime.utcfromtimestamp(post.created_utc),
                "title": post.title,
                "text": post.selftext,
                "score": post.score,
                "num_comments": post.num_comments,
                "url": post.url
            })
            
        return pd.DataFrame(posts_data)
        
    except Exception as e:
        print(f"Error fetching Reddit data: {e}")
        return get_mock_social_data()

def get_mock_social_data():
    """Generates fake social data for testing without API keys."""
    mock_data = [
        {
            "source": "reddit", 
            "id": "mock1", 
            "created_utc": datetime.utcnow(), 
            "title": "Bitcoin is going to the moon!", 
            "text": "I think we are seeing a huge bull run incoming.", 
            "score": 105, 
            "num_comments": 20,
            "url": "http://mock.url"
        },
        {
            "source": "reddit", 
            "id": "mock2", 
            "created_utc": datetime.utcnow(), 
            "title": "Market crash imminent?", 
            "text": "Technical indicators look bearish.", 
            "score": 50, 
            "num_comments": 15,
            "url": "http://mock.url"
        },
        {
            "source": "reddit", 
            "id": "mock3", 
            "created_utc": datetime.utcnow(), 
            "title": "Just bought more ETH", 
            "text": "Ethereum upgrade looks promising.", 
            "score": 300, 
            "num_comments": 50,
            "url": "http://mock.url"
        }
    ]
    return pd.DataFrame(mock_data)

if __name__ == "__main__":
    # Test fetching
    df_reddit = fetch_reddit_posts("CryptoCurrency", limit=10, search_query="Bitcoin")
    print(df_reddit.head())
    df_reddit.to_csv("social_data_test.csv", index=False)
