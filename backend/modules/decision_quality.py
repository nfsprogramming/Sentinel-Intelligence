import numpy as np
from datetime import datetime, timedelta

class CounterfactualAnalyzer:
    """
    Compares AI recommendation vs alternative strategies.
    Shows: "AI: +4.2% | Hold: +1.1% | No Action: -0.3%"
    
    This is critical for decision-quality assessment.
    """
    
    def __init__(self, backtest_tracker):
        self.tracker = backtest_tracker
    
    def analyze_alternatives(self, current_price, predicted_price, bias, timeframe_days=7):
        """
        Calculate outcomes for different strategies.
        
        Returns:
            ai_outcome: Expected % change if following AI
            hold_outcome: Expected % change if holding
            no_action_outcome: Expected % change if doing nothing
            best_strategy: Which strategy would have been optimal
        """
        # Calculate AI strategy outcome
        price_change_pct = ((predicted_price - current_price) / current_price) * 100
        
        # AI strategy: Follow the bias
        if "Bullish" in bias:
            # AI says buy → gain if price goes up
            ai_outcome = price_change_pct
        elif "Bearish" in bias:
            # AI says sell/short → gain if price goes down (inverse)
            ai_outcome = -price_change_pct
        else:
            # AI says neutral → no action
            ai_outcome = 0.0
        
        # Hold strategy: Always hold (passive)
        hold_outcome = price_change_pct
        
        # No action strategy: 0% change (cash position)
        no_action_outcome = 0.0
        
        # Determine best strategy
        outcomes = {
            "AI": ai_outcome,
            "Hold": hold_outcome,
            "Cash": no_action_outcome
        }
        best_strategy = max(outcomes, key=outcomes.get)
        
        # Calculate regret (difference from best outcome)
        best_outcome = outcomes[best_strategy]
        ai_regret = best_outcome - ai_outcome
        
        return {
            "ai": round(ai_outcome, 2),
            "hold": round(hold_outcome, 2),
            "cash": round(no_action_outcome, 2),
            "bestStrategy": best_strategy,
            "aiRegret": round(ai_regret, 2),
            "message": self._generate_message(ai_outcome, hold_outcome, best_strategy)
        }
    
    def _generate_message(self, ai_outcome, hold_outcome, best_strategy):
        """Generate human-readable comparison"""
        if best_strategy == "AI":
            if ai_outcome > hold_outcome:
                return f"AI outperforms buy & hold by {abs(ai_outcome - hold_outcome):.1f}%"
            else:
                return "AI recommends optimal strategy"
        elif best_strategy == "Hold":
            return f"Buy & hold outperforms AI by {abs(hold_outcome - ai_outcome):.1f}%"
        else:
            return "Cash position optimal in current conditions"
    
    def get_historical_comparison(self, lookback_days=30):
        """
        Compare AI vs Buy & Hold over historical predictions.
        
        Returns cumulative performance if available.
        """
        recent = self.tracker.get_recent_predictions(n=100)
        
        if len(recent) < 5:
            return {
                "available": False,
                "message": "Insufficient history for comparison"
            }
        
        # Filter predictions with actual outcomes
        completed = [p for p in recent if p.get('actualPrice')]
        
        if len(completed) < 3:
            return {
                "available": False,
                "message": "Waiting for predictions to mature"
            }
        
        # Calculate cumulative returns
        ai_cumulative = 0.0
        hold_cumulative = 0.0
        
        for pred in completed:
            current = pred['currentPrice']
            actual = pred['actualPrice']
            bias = pred['bias']
            
            # Hold return
            hold_return = ((actual - current) / current) * 100
            hold_cumulative += hold_return
            
            # AI return (inverse if bearish)
            if "Bullish" in bias:
                ai_return = hold_return
            elif "Bearish" in bias:
                ai_return = -hold_return
            else:
                ai_return = 0
            
            ai_cumulative += ai_return
        
        # Determine winner
        if ai_cumulative > hold_cumulative:
            winner = "AI"
            outperformance = ai_cumulative - hold_cumulative
        else:
            winner = "Buy & Hold"
            outperformance = hold_cumulative - ai_cumulative
        
        return {
            "available": True,
            "aiCumulative": round(ai_cumulative, 2),
            "holdCumulative": round(hold_cumulative, 2),
            "winner": winner,
            "outperformance": round(outperformance, 2),
            "sampleSize": len(completed),
            "message": f"{winner} leads by {outperformance:.1f}% ({len(completed)} predictions)"
        }


class DrawdownAwareConfidence:
    """
    Reduces confidence after consecutive losses.
    Prevents overconfidence during losing streaks.
    """
    
    def __init__(self, backtest_tracker):
        self.tracker = backtest_tracker
    
    def calculate_drawdown_penalty(self, n=10):
        """
        Analyze recent prediction accuracy and apply penalty.
        
        Returns:
            penalty_factor: 0.0 - 1.0 (1.0 = no penalty)
            consecutive_losses: Number of recent wrong predictions
            message: Explanation
        """
        recent = self.tracker.get_recent_predictions(n)
        
        if len(recent) < 3:
            return 1.0, 0, None
        
        # Count consecutive losses (predictions with actual outcomes)
        consecutive_losses = 0
        for pred in reversed(recent):
            if not pred.get('actualPrice'):
                continue  # Skip pending predictions
            
            # Check if prediction was correct
            was_correct = self._was_prediction_correct(pred)
            
            if not was_correct:
                consecutive_losses += 1
            else:
                break  # Stop at first win
        
        # Apply penalty based on consecutive losses
        if consecutive_losses >= 5:
            penalty_factor = 0.5  # 50% confidence reduction
            message = "⚠️ High drawdown - confidence reduced by 50%"
        elif consecutive_losses >= 3:
            penalty_factor = 0.7  # 30% reduction
            message = "⚠️ Recent losses - confidence reduced by 30%"
        elif consecutive_losses >= 2:
            penalty_factor = 0.85  # 15% reduction
            message = "Slight confidence reduction after recent misses"
        else:
            penalty_factor = 1.0
            message = None
        
        return penalty_factor, consecutive_losses, message
    
    def _was_prediction_correct(self, pred):
        """Check if prediction direction was correct"""
        current = pred['currentPrice']
        actual = pred['actualPrice']
        bias = pred['bias']
        
        actual_direction = "Bullish" if actual > current else "Bearish" if actual < current else "Neutral"
        
        # Simplified: check if bias matches actual direction
        if "Bullish" in bias and actual_direction == "Bullish":
            return True
        elif "Bearish" in bias and actual_direction == "Bearish":
            return True
        elif "Neutral" in bias and actual_direction == "Neutral":
            return True
        else:
            return False


class NarrativeTimeline:
    """
    Generates a human-readable story of AI decisions.
    Example: "BTC entered high volatility. AI reduced exposure. Capital preserved."
    """
    
    def __init__(self, backtest_tracker):
        self.tracker = backtest_tracker
    
    def generate_timeline(self, n=5):
        """
        Create a narrative from recent predictions.
        
        Returns:
            timeline: List of narrative events
        """
        recent = self.tracker.get_recent_predictions(n)
        
        if len(recent) < 2:
            return {
                "available": False,
                "events": [],
                "message": "Building prediction history..."
            }
        
        events = []
        
        for i, pred in enumerate(recent):
            timestamp = pred.get('timestamp', 'Unknown time')
            bias = pred.get('bias', 'Neutral')
            regime = pred.get('regime', {}).get('type', 'Unknown')
            strength = pred.get('signalStrength', 'Low')
            
            # Generate narrative event
            event = self._create_narrative_event(i, timestamp, bias, regime, strength, recent)
            if event:
                events.append(event)
        
        return {
            "available": True,
            "events": events,
            "message": f"{len(events)} decision points tracked"
        }
    
    def _create_narrative_event(self, index, timestamp, bias, regime, strength, all_preds):
        """Create a single narrative event"""
        # Detect regime changes
        if index > 0:
            prev_regime = all_preds[index - 1].get('regime', {}).get('type', '')
            if regime != prev_regime and regime != 'Unknown':
                return {
                    "timestamp": timestamp,
                    "type": "regime_change",
                    "message": f"Market shifted to {regime}. AI adjusted strategy to {bias}."
                }
        
        # Detect bias changes
        if index > 0:
            prev_bias = all_preds[index - 1].get('bias', '')
            if bias != prev_bias:
                return {
                    "timestamp": timestamp,
                    "type": "bias_change",
                    "message": f"Signal flipped to {bias} ({strength} conviction)."
                }
        
        # High conviction events
        if strength == "High":
            return {
                "timestamp": timestamp,
                "type": "high_conviction",
                "message": f"High conviction {bias} signal in {regime} regime."
            }
        
        return None
