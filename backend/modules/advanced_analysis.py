import pandas as pd
import numpy as np

class RegimeDetector:
    """
    Detects market regime to adjust prediction confidence.
    Markets behave differently in trending, ranging, high-volatility, and news-driven regimes.
    """
    
    def detect_regime(self, df):
        """
        Analyze price data to determine current market regime.
        Returns: regime_type, risk_level, description
        """
        if len(df) < 20:
            return "Insufficient Data", "Unknown", "Not enough data for regime detection"
        
        # Calculate volatility (20-day rolling std)
        returns = df['Close'].pct_change()
        volatility = returns.rolling(20).std().iloc[-1]
        
        # Calculate trend strength (ADX-like)
        high_low_range = (df['High'] - df['Low']).rolling(14).mean().iloc[-1]
        close_range = df['Close'].rolling(14).std().iloc[-1]
        trend_strength = close_range / high_low_range if high_low_range > 0 else 0
        
        # Detect regime
        if volatility > 0.03:  # High volatility threshold
            regime = "High Volatility"
            risk = "Elevated"
            desc = "Unstable price action - reduce position sizes"
        elif trend_strength > 0.7:
            # Check if trending up or down
            sma_20 = df['Close'].rolling(20).mean().iloc[-1]
            current = df['Close'].iloc[-1]
            if current > sma_20 * 1.02:
                regime = "Strong Uptrend"
                risk = "Moderate"
                desc = "Clear bullish momentum"
            elif current < sma_20 * 0.98:
                regime = "Strong Downtrend"
                risk = "Moderate"
                desc = "Clear bearish momentum"
            else:
                regime = "Trending"
                risk = "Low"
                desc = "Directional price movement"
        elif volatility < 0.015:
            regime = "Ranging"
            risk = "Low"
            desc = "Sideways consolidation - mean reversion likely"
        else:
            regime = "Mixed"
            risk = "Moderate"
            desc = "No clear pattern - exercise caution"
        
        return regime, risk, desc
    
    def adjust_confidence_for_regime(self, base_strength, regime_type):
        """
        Adjust signal strength based on regime.
        High volatility = reduce confidence
        Strong trend = maintain confidence
        """
        adjustments = {
            "High Volatility": -0.1,
            "Strong Uptrend": 0.05,
            "Strong Downtrend": 0.05,
            "Trending": 0.0,
            "Ranging": -0.05,
            "Mixed": -0.05,
            "Insufficient Data": -0.15
        }
        
        adjustment = adjustments.get(regime_type, 0)
        adjusted = base_strength + adjustment
        
        # Clamp between 0 and 1
        return max(0.0, min(1.0, adjusted))


class MultiTimeframeAnalyzer:
    """
    Analyzes multiple timeframes to detect agreement/divergence.
    One timeframe lies - multiple agreeing don't.
    """
    
    def analyze_timeframes(self, df, current_bias, fusion_score):
        """
        Simulate multi-timeframe analysis.
        In production, you'd fetch 1H, 4H, 1D data separately.
        For now, we'll use rolling windows as proxies.
        """
        if len(df) < 100:
            return {
                "1H": "Neutral",
                "4H": "Neutral", 
                "1D": current_bias,
                "consensus": "Weak " + current_bias,
                "agreement": 33
            }
        
        # Simulate timeframes using different window sizes
        # 1H = last 7 days
        # 4H = last 30 days  
        # 1D = last 60 days
        
        def get_bias_from_window(window_days):
            window_data = df.tail(window_days)
            start_price = window_data['Close'].iloc[0]
            end_price = window_data['Close'].iloc[-1]
            change = (end_price - start_price) / start_price
            
            if change > 0.02:
                return "Bullish"
            elif change < -0.02:
                return "Bearish"
            else:
                return "Neutral"
        
        tf_1h = get_bias_from_window(7)
        tf_4h = get_bias_from_window(30)
        tf_1d = current_bias.replace(" Bias", "")
        
        # Calculate agreement
        biases = [tf_1h, tf_4h, tf_1d]
        most_common = max(set(biases), key=biases.count)
        agreement_pct = (biases.count(most_common) / 3) * 100
        
        # Determine consensus
        if agreement_pct >= 66:
            consensus = "Strong " + most_common
        else:
            consensus = "Weak " + most_common
        
        return {
            "1H": tf_1h,
            "4H": tf_4h,
            "1D": tf_1d,
            "consensus": consensus,
            "agreement": int(agreement_pct)
        }


class ExplanationEngine:
    """
    Generates human-readable explanations for predictions.
    Users trust explanations more than numbers.
    """
    
    def generate_explanation(self, df, lstm_score, sent_score, fusion_score, bias):
        """
        Create interpretable explanation of the prediction.
        """
        # Trend direction
        sma_20 = df['Close'].rolling(20).mean().iloc[-1]
        current = df['Close'].iloc[-1]
        
        if current > sma_20 * 1.01:
            trend = "↑ Upward"
        elif current < sma_20 * 0.99:
            trend = "↓ Downward"
        else:
            trend = "→ Sideways"
        
        # Volatility regime
        returns = df['Close'].pct_change()
        volatility = returns.rolling(20).std().iloc[-1]
        
        if volatility > 0.03:
            vol_regime = "High"
        elif volatility < 0.015:
            vol_regime = "Low"
        else:
            vol_regime = "Moderate"
        
        # Dominant factor
        if abs(lstm_score - 0.5) > abs(sent_score - 0.5):
            if lstm_score > 0.5:
                dominant = "Price momentum (bullish)"
            else:
                dominant = "Price momentum (bearish)"
        else:
            if sent_score > 0.5:
                dominant = "Sentiment shift (positive)"
            else:
                dominant = "Sentiment shift (negative)"
        
        # Construct explanation
        explanation = f"{bias} due to {trend.lower()} trend and {dominant.lower()}. "
        explanation += f"Volatility: {vol_regime}."
        
        return {
            "summary": explanation,
            "trend": trend,
            "volatility": vol_regime,
            "dominantFactor": dominant
        }
