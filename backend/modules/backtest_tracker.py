import json
import os
from datetime import datetime
from pathlib import Path

class BacktestTracker:
    """
    Tracks prediction history for backtesting and performance metrics.
    Stores predictions in a simple JSON file.
    """
    
    def __init__(self, storage_path="data/backtest_history.json"):
        self.storage_path = storage_path
        self.history = self._load_history()
    
    def _load_history(self):
        """Load existing prediction history"""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_history(self):
        """Save prediction history to disk"""
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def log_prediction(self, ticker, current_price, predicted_price, bias, 
                      signal_strength, fusion_score, timeframe="7D"):
        """Log a new prediction"""
        prediction = {
            "timestamp": datetime.now().isoformat(),
            "ticker": ticker,
            "currentPrice": current_price,
            "predictedPrice": predicted_price,
            "bias": bias,
            "signalStrength": signal_strength,
            "fusionScore": fusion_score,
            "timeframe": timeframe,
            "actualPrice": None,  # To be filled later
            "error": None,
            "correct": None
        }
        
        self.history.append(prediction)
        
        # Keep only last 100 predictions
        if len(self.history) > 100:
            self.history = self.history[-100:]
        
        self._save_history()
    
    def update_actual_price(self, index, actual_price):
        """Update a prediction with actual price for accuracy calculation"""
        if 0 <= index < len(self.history):
            pred = self.history[index]
            pred['actualPrice'] = actual_price
            
            # Calculate error
            predicted = pred['predictedPrice']
            error_pct = abs(actual_price - predicted) / predicted * 100
            pred['error'] = round(error_pct, 2)
            
            # Determine if prediction was correct (direction)
            current = pred['currentPrice']
            predicted_up = predicted > current
            actual_up = actual_price > current
            pred['correct'] = (predicted_up == actual_up)
            
            self._save_history()
    
    def get_stats(self, last_n=30):
        """
        Calculate performance statistics for last N predictions.
        Returns: dict with win_rate, avg_error, total_predictions
        """
        # Filter predictions with actual prices
        completed = [p for p in self.history[-last_n:] if p['actualPrice'] is not None]
        
        if not completed:
            return {
                "totalPredictions": 0,
                "winRate": 0,
                "avgError": 0,
                "lastUpdated": None
            }
        
        correct_count = sum(1 for p in completed if p['correct'])
        win_rate = (correct_count / len(completed)) * 100
        avg_error = sum(p['error'] for p in completed) / len(completed)
        
        return {
            "totalPredictions": len(completed),
            "winRate": round(win_rate, 1),
            "avgError": round(avg_error, 2),
            "lastUpdated": completed[-1]['timestamp'] if completed else None
        }
    
    def get_recent_predictions(self, n=10):
        """Get last N predictions"""
        return self.history[-n:] if self.history else []
