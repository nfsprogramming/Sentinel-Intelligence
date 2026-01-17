import numpy as np
from datetime import datetime, timedelta

class UncertaintyCalculator:
    """
    Calculates uncertainty bands and scenario analysis.
    AI models are probabilistic - show that with Best/Base/Worst cases.
    """
    
    def calculate_scenarios(self, current_price, predicted_price, volatility, signal_strength):
        """
        Generate Best/Base/Worst case scenarios based on model uncertainty.
        
        Args:
            current_price: Current market price
            predicted_price: Model's point prediction
            volatility: Historical volatility
            signal_strength: Model confidence (0-1)
        
        Returns:
            dict with best, base, worst scenarios
        """
        # Base case is the model prediction
        base_case = predicted_price
        
        # Calculate uncertainty range based on volatility and signal strength
        # Lower signal strength = wider bands
        uncertainty_factor = (1 - signal_strength) * volatility * current_price
        
        # Add asymmetry based on prediction direction
        if predicted_price > current_price:
            # Bullish prediction - wider upside
            best_case = predicted_price + (uncertainty_factor * 1.5)
            worst_case = predicted_price - (uncertainty_factor * 0.8)
        else:
            # Bearish prediction - wider downside
            best_case = predicted_price + (uncertainty_factor * 0.8)
            worst_case = predicted_price - (uncertainty_factor * 1.5)
        
        return {
            "best": round(best_case, 2),
            "base": round(base_case, 2),
            "worst": round(worst_case, 2),
            "uncertainty": round(uncertainty_factor, 2)
        }


class PredictionTimer:
    """
    Manages time-aware confidence decay.
    Predictions should expire - add countdown and auto-decay.
    """
    
    def __init__(self, validity_hours=6):
        self.validity_hours = validity_hours
    
    def get_expiry_info(self, prediction_timestamp=None):
        """
        Calculate expiry time and remaining validity.
        
        Returns:
            dict with expiry_time, remaining_hours, is_expired, decay_factor
        """
        if prediction_timestamp is None:
            prediction_timestamp = datetime.now()
        elif isinstance(prediction_timestamp, str):
            prediction_timestamp = datetime.fromisoformat(prediction_timestamp)
        
        expiry_time = prediction_timestamp + timedelta(hours=self.validity_hours)
        now = datetime.now()
        
        time_elapsed = (now - prediction_timestamp).total_seconds() / 3600  # hours
        remaining = self.validity_hours - time_elapsed
        
        is_expired = remaining <= 0
        
        # Calculate decay factor (linear decay from 1.0 to 0.5)
        if is_expired:
            decay_factor = 0.0
        else:
            decay_factor = max(0.5, 1.0 - (time_elapsed / self.validity_hours) * 0.5)
        
        return {
            "expiryTime": expiry_time.isoformat(),
            "remainingHours": max(0, round(remaining, 1)),
            "isExpired": is_expired,
            "decayFactor": round(decay_factor, 2),
            "validityHours": self.validity_hours
        }


class ModelHealthMonitor:
    """
    Tracks model health and performance degradation.
    Enterprise-level thinking: monitor drift, error, stability.
    """
    
    def __init__(self, backtest_tracker):
        self.tracker = backtest_tracker
    
    def assess_health(self):
        """
        Evaluate model health based on recent performance.
        
        Returns:
            dict with status, error_trend, stability, warnings
        """
        recent = self.tracker.get_recent_predictions(n=10)
        
        if len(recent) < 3:
            return {
                "status": "Initializing",
                "message": "Insufficient data for health assessment",
                "errorTrend": "Unknown",
                "stability": "Unknown",
                "warnings": []
            }
        
        # Calculate recent error trend
        completed = [p for p in recent if p.get('error') is not None]
        
        if len(completed) < 3:
            return {
                "status": "Monitoring",
                "message": "Collecting performance data",
                "errorTrend": "Unknown",
                "stability": "Unknown",
                "warnings": []
            }
        
        errors = [p['error'] for p in completed]
        recent_errors = errors[-5:]  # Last 5
        older_errors = errors[:-5] if len(errors) > 5 else errors
        
        recent_avg = np.mean(recent_errors)
        older_avg = np.mean(older_errors) if older_errors else recent_avg
        
        # Detect error trend
        if recent_avg > older_avg * 1.3:
            error_trend = "Increasing"
            status = "Degraded"
        elif recent_avg < older_avg * 0.7:
            error_trend = "Improving"
            status = "Healthy"
        else:
            error_trend = "Stable"
            status = "Healthy"
        
        # Check stability (variance in predictions)
        fusion_scores = [p.get('fusionScore', 0.5) for p in recent[-5:]]
        stability_variance = np.std(fusion_scores)
        
        if stability_variance > 0.2:
            stability = "Unstable"
            status = "Degraded"
        else:
            stability = "Stable"
        
        # Generate warnings
        warnings = []
        if error_trend == "Increasing":
            warnings.append("Error rate increasing - model may need retraining")
        if stability == "Unstable":
            warnings.append("High prediction variance detected")
        if recent_avg > 10:
            warnings.append("Average error exceeds 10% - use caution")
        
        message = f"Recent avg error: {recent_avg:.1f}% | Trend: {error_trend}"
        
        return {
            "status": status,
            "message": message,
            "errorTrend": error_trend,
            "stability": stability,
            "warnings": warnings,
            "recentAvgError": round(recent_avg, 1)
        }
