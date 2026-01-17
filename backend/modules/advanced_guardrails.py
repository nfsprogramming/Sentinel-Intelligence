import numpy as np

class SignalStabilityTracker:
    """
    Tracks signal stability to detect flip-flopping.
    Low stability → reduce confidence to prevent overtrading.
    """
    
    def __init__(self, backtest_tracker):
        self.tracker = backtest_tracker
    
    def calculate_stability(self, n=10):
        """
        Analyze last N predictions for consistency.
        
        Returns:
            stability_level: "High" / "Medium" / "Low"
            stability_score: 0.0 - 1.0
            flip_count: Number of direction changes
        """
        recent = self.tracker.get_recent_predictions(n)
        
        if len(recent) < 3:
            return "Unknown", 1.0, 0, "Insufficient prediction history"
        
        # Extract biases
        biases = [p.get('bias', 'Neutral') for p in recent]
        
        # Count directional flips
        flips = 0
        for i in range(1, len(biases)):
            prev_direction = self._get_direction(biases[i-1])
            curr_direction = self._get_direction(biases[i])
            if prev_direction != curr_direction and prev_direction != "Neutral" and curr_direction != "Neutral":
                flips += 1
        
        # Calculate stability score
        max_flips = len(biases) - 1
        stability_score = 1.0 - (flips / max_flips) if max_flips > 0 else 1.0
        
        # Categorize
        if stability_score >= 0.7:
            level = "High"
            message = "Consistent signal direction"
        elif stability_score >= 0.4:
            level = "Medium"
            message = "Moderate signal variance"
        else:
            level = "Low"
            message = "Frequent direction changes - overtrading risk"
        
        return level, round(stability_score, 2), flips, message
    
    def _get_direction(self, bias):
        """Extract directional component from bias"""
        if "Bullish" in bias:
            return "Bullish"
        elif "Bearish" in bias:
            return "Bearish"
        else:
            return "Neutral"
    
    def adjust_confidence_for_stability(self, base_confidence, stability_score):
        """
        Reduce confidence if signal is unstable.
        """
        if stability_score < 0.4:  # Low stability
            penalty = 0.3  # 30% reduction
            adjusted = base_confidence * (1 - penalty)
            warning = "Confidence reduced due to signal instability"
        elif stability_score < 0.7:  # Medium stability
            penalty = 0.15  # 15% reduction
            adjusted = base_confidence * (1 - penalty)
            warning = "Slight confidence reduction due to moderate stability"
        else:
            adjusted = base_confidence
            warning = None
        
        return adjusted, warning


class EthicalGuardrails:
    """
    Implements hard caps and ethical constraints on AI confidence.
    Never show 90%+ confidence - it's unprofessional and misleading.
    """
    
    MAX_CONFIDENCE = 0.70  # Hard cap at 70%
    MIN_CONFIDENCE = 0.05  # Floor at 5%
    
    def apply_guardrails(self, raw_confidence, raw_strength_value):
        """
        Apply ethical caps to confidence metrics.
        
        Returns:
            capped_value: Adjusted confidence value
            strength_category: Recalculated category
            message: Explanation if capped
        """
        # Apply hard cap
        capped_value = min(raw_strength_value, self.MAX_CONFIDENCE)
        capped_value = max(capped_value, self.MIN_CONFIDENCE)
        
        # Determine if capping occurred
        was_capped = capped_value != raw_strength_value
        
        # Recalculate strength category with capped value
        score_distance = abs(capped_value)
        if score_distance >= 0.3:
            strength = "High"
        elif score_distance >= 0.15:
            strength = "Medium"
        else:
            strength = "Low"
        
        # Generate message
        if was_capped and raw_strength_value > self.MAX_CONFIDENCE:
            message = f"Confidence capped at {int(self.MAX_CONFIDENCE * 100)}% by risk policy"
        else:
            message = None
        
        return round(capped_value, 2), strength, message


class ConvictionLanguage:
    """
    Converts numerical confidence into verb-based, human language.
    Replaces sterile numbers with emotional intelligence.
    """
    
    @staticmethod
    def get_conviction_state(signal_strength, fusion_score, stability):
        """
        Generate verb-based conviction descriptor.
        
        Examples:
        - "Cautious"
        - "Conviction Rising"
        - "High Conviction"
        - "Wavering"
        """
        # Check stability first
        if stability == "Low":
            return "Wavering", "Signal unstable"
        
        # Map strength + score to conviction
        if signal_strength == "High":
            if fusion_score > 0.65:
                return "High Conviction", "Strong directional bias"
            else:
                return "Conviction Rising", "Building momentum"
        
        elif signal_strength == "Medium":
            if fusion_score > 0.55:
                return "Moderate Conviction", "Balanced outlook"
            else:
                return "Cautious", "Mixed signals"
        
        else:  # Low
            return "Low Conviction", "Weak signal - consider waiting"
    
    @staticmethod
    def get_action_verb(bias, conviction_state):
        """
        Generate action-oriented language.
        
        Examples:
        - "Leaning Bearish"
        - "Strongly Bullish"
        - "Neutral Stance"
        """
        conviction_map = {
            "High Conviction": "Strongly",
            "Conviction Rising": "Increasingly",
            "Moderate Conviction": "Moderately",
            "Cautious": "Leaning",
            "Low Conviction": "Weakly",
            "Wavering": "Tentatively"
        }
        
        modifier = conviction_map.get(conviction_state, "")
        
        if "Bullish" in bias:
            return f"{modifier} Bullish" if modifier else "Bullish"
        elif "Bearish" in bias:
            return f"{modifier} Bearish" if modifier else "Bearish"
        else:
            return "Neutral Stance"
    
    @staticmethod
    def reframe_terminology(term):
        """
        Professional language reframing.
        """
        reframing_map = {
            "prediction": "probabilistic outlook",
            "accuracy": "decision quality",
            "confidence": "conviction level",
            "target price": "expected range",
            "forecast": "market bias assessment",
            "signal": "directional bias"
        }
        
        return reframing_map.get(term.lower(), term)
