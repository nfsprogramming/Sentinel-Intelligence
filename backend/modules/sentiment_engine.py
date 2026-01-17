import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FinBERTSentiment:
    def __init__(self):
        self.mode = "UNKNOWN"
        self.nlp = None
        self.analyzer = None
        self.av = None
        
        # Delayed import to avoid crashing if library is missing
        from modules.alpha_conn import AlphaVantageSentiment
        self.av = AlphaVantageSentiment()

        # 1. Try Loading FinBERT (Heavy / Localhost)
        try:
            # Check if we are forced into Lite mode via Env Var
            if os.getenv("SENTINEL_MODE") == "LITE":
                raise ImportError("Forced Lite Mode")

            from transformers import pipeline
            import torch
            
            device = 0 if torch.cuda.is_available() else -1
            logger.info(f"Initializing FinBERT (GPU={'Yes' if device==0 else 'No'})...")
            self.nlp = pipeline("sentiment-analysis", model="ProsusAI/finbert", device=device)
            self.mode = "HEAVY"
            logger.info("FinBERT Loaded Successfully.")
            
        except ImportError:
            # 2. Fallback to VADER (Lite / Cloud)
            logger.info("Transformers/Torch not found. Switching to Lite Mode (VADER)...")
            from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
            self.analyzer = SentimentIntensityAnalyzer()
            self.mode = "LITE"
            logger.info("VADER Loaded Successfully.")
        except Exception as e:
            logger.error(f"Error initializing FinBERT: {e}")
            # Fallback
            from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
            self.analyzer = SentimentIntensityAnalyzer()
            self.mode = "LITE"

    def analyze(self, ticker):
        """
        Analyze sentiment using the available engine (FinBERT or VADER).
        """
        # 1. Fetch Headlines (Common)
        _, _, text = self.av.get_sentiment(ticker)
        
        if text in ["No Data", "Error", "API Limit", "No News"]:
            return 0.5, "Neutral"

        # 2. Analyze based on Mode
        if self.mode == "HEAVY" and self.nlp:
            return self._analyze_finbert(text)
        elif self.mode == "LITE" and self.analyzer:
            return self._analyze_vader(text)
        else:
            return 0.5, "Neutral"

    def _analyze_finbert(self, text):
        print(f"Analysis (FinBERT): {text[:50]}...")
        result = self.nlp(text)[0]
        label = result['label']
        score = result['score']
        
        if label == 'positive':
            final_score = 0.5 + (0.5 * score)
        elif label == 'negative':
            final_score = 0.5 - (0.5 * score)
        else:
            final_score = 0.5
            
        return final_score, label

    def _analyze_vader(self, text):
        print(f"Analysis (VADER): {text[:50]}...")
        scores = self.analyzer.polarity_scores(text)
        compound = scores['compound']
        final_score = (compound + 1) / 2
        
        if compound >= 0.05:
            label = "positive"
        elif compound <= -0.05:
            label = "negative"
        else:
            label = "neutral"
            
        return final_score, label
