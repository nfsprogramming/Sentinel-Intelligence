import numpy as np
from datetime import datetime

class SilenceIntelligence:
    """
    OMEGA TIER: Knows when NOT to speak.
    
    Most AIs try to predict all the time.
    Elite systems know when to stay silent.
    
    Calculates "Signal Worthiness Score" - if below threshold, AI remains silent.
    """
    
    WORTHINESS_THRESHOLD = 0.40  # Minimum score to speak
    
    def __init__(self):
        self.silence_events = []
    
    def assess_worthiness(self, prediction_data, market_data):
        """
        Determine if this prediction is worth making.
        
        Factors:
        - Signal strength
        - Stability
        - Regime clarity
        - Information gain
        - Model agreement
        
        Returns:
            worthy: bool
            score: 0-1
            reason: str
        """
        factors = {}
        
        # Factor 1: Signal Strength (0-1)
        signal_strength = prediction_data.get("signalValue", 0)
        factors["signal_strength"] = signal_strength
        
        # Factor 2: Stability (0-1)
        stability = prediction_data.get("stability", {}).get("score", 0.5)
        factors["stability"] = stability
        
        # Factor 3: Regime Clarity (0-1)
        regime_risk = prediction_data.get("regime", {}).get("risk", "Moderate")
        regime_clarity = {
            "Low": 1.0,
            "Moderate": 0.6,
            "Elevated": 0.3
        }.get(regime_risk, 0.5)
        factors["regime_clarity"] = regime_clarity
        
        # Factor 4: Bayesian Uncertainty (0-1, inverted)
        uncertainty = prediction_data.get("bayesianBeliefs", {}).get("uncertainty", 0.5)
        factors["certainty"] = 1.0 - uncertainty
        
        # Factor 5: Model Agreement (0-1)
        mtf_consensus = prediction_data.get("multiTimeframe", {}).get("consensusScore", 0.5)
        factors["model_agreement"] = mtf_consensus / 100 if mtf_consensus > 1 else mtf_consensus
        
        # Factor 6: Information Gain (0-1)
        # If beliefs are evenly distributed, information gain is low
        beliefs = prediction_data.get("bayesianBeliefs", {}).get("beliefs", {})
        if beliefs:
            max_belief = max(beliefs.values()) if isinstance(beliefs, dict) else 33.3
            if isinstance(max_belief, (int, float)) and max_belief > 1:
                max_belief = max_belief / 100
            information_gain = max_belief  # Dominant belief strength
        else:
            information_gain = 0.5
        factors["information_gain"] = information_gain
        
        # Weighted average
        weights = {
            "signal_strength": 0.25,
            "stability": 0.20,
            "regime_clarity": 0.15,
            "certainty": 0.15,
            "model_agreement": 0.15,
            "information_gain": 0.10
        }
        
        worthiness_score = sum(factors[k] * weights[k] for k in weights)
        
        # Determine if worthy
        is_worthy = worthiness_score >= self.WORTHINESS_THRESHOLD
        
        # Generate reason
        if not is_worthy:
            weak_factors = [k for k, v in factors.items() if v < 0.4]
            reason = f"Insufficient signal quality: {', '.join(weak_factors)}"
        else:
            reason = "Signal meets worthiness threshold"
        
        # Log silence events
        if not is_worthy:
            self.silence_events.append({
                "timestamp": datetime.now().isoformat(),
                "score": worthiness_score,
                "factors": factors,
                "reason": reason
            })
        
        return {
            "worthy": bool(is_worthy),
            "score": round(float(worthiness_score), 3),
            "threshold": float(self.WORTHINESS_THRESHOLD),
            "factors": {k: round(float(v), 3) for k, v in factors.items()},
            "reason": reason,
            "message": "Signal worthy of attention" if is_worthy else "No insight detected - AI remains silent"
        }
    
    def get_silence_rate(self):
        """Calculate how often AI chooses silence"""
        if not self.silence_events:
            return {"available": False}
        
        # Assume total predictions = silence + spoken
        # This is a simplified metric
        return {
            "available": True,
            "silenceCount": len(self.silence_events),
            "message": f"AI chose silence {len(self.silence_events)} times"
        }


class ModelHumilityIndex:
    """
    OMEGA TIER: Quantifies and enforces humility.
    
    If AI confidence >> historical accuracy:
    - Force confidence compression
    - Display humility enforcement
    
    Prevents ego-AI behavior.
    """
    
    def __init__(self, backtest_tracker):
        self.tracker = backtest_tracker
    
    def calculate_humility(self, current_confidence):
        """
        Compare current confidence to historical performance.
        
        Returns:
            humility_score: 0-100 (100 = perfectly humble)
            enforcement_needed: bool
            adjusted_confidence: float
        """
        recent = self.tracker.get_recent_predictions(n=20)
        
        if len(recent) < 5:
            return {
                "available": False,
                "score": None,
                "message": "Insufficient history for humility assessment"
            }
        
        # Calculate historical accuracy
        completed = [p for p in recent if p.get('actualPrice')]
        
        if len(completed) < 3:
            return {
                "available": False,
                "score": None,
                "message": "Waiting for predictions to mature"
            }
        
        # Calculate actual accuracy
        correct = sum(1 for p in completed if self._was_correct(p))
        accuracy = correct / len(completed)
        
        # Calculate average historical confidence
        avg_confidence = sum(p.get('signalValue', 0) for p in completed) / len(completed)
        
        # Humility gap = confidence - accuracy
        humility_gap = avg_confidence - accuracy
        
        # Humility score (0-100)
        # Gap < 0 = underconfident (100)
        # Gap = 0 = perfectly calibrated (100)
        # Gap > 0.2 = severely overconfident (0)
        if humility_gap <= 0:
            humility_score = 100
        elif humility_gap <= 0.1:
            humility_score = 80
        elif humility_gap <= 0.2:
            humility_score = 50
        else:
            humility_score = 20
        
        # Determine if enforcement needed
        enforcement_needed = humility_gap > 0.15
        
        # Adjust current confidence if needed
        if enforcement_needed:
            # Compress confidence toward accuracy
            compression_factor = accuracy / avg_confidence if avg_confidence > 0 else 0.5
            adjusted_confidence = current_confidence * compression_factor
            message = f"Humility Enforcement Active - confidence compressed by {int((1 - compression_factor) * 100)}%"
        else:
            adjusted_confidence = current_confidence
            message = "AI humility within acceptable range"
        
        return {
            "available": True,
            "score": round(float(humility_score), 1),
            "humilityGap": round(float(humility_gap), 3),
            "enforcementNeeded": bool(enforcement_needed),
            "adjustedConfidence": round(float(adjusted_confidence), 3),
            "historicalAccuracy": round(float(accuracy), 3),
            "avgConfidence": round(float(avg_confidence), 3),
            "message": message,
            "sampleSize": int(len(completed))
        }
    
    def _was_correct(self, pred):
        """Check if prediction direction was correct"""
        current = pred['currentPrice']
        predicted = pred['predictedPrice']
        actual = pred['actualPrice']
        
        predicted_direction = "up" if predicted > current else "down"
        actual_direction = "up" if actual > current else "down"
        
        return predicted_direction == actual_direction


class TrustDebtLedger:
    """
    OMEGA TIER: Tracks moments where AI overpromised and underperformed.
    
    Trust debt accumulates → AI self-limits.
    
    This is ethical AI in action.
    """
    
    MAX_TRUST_DEBT = 5  # Maximum debt before severe limits
    
    def __init__(self, backtest_tracker):
        self.tracker = backtest_tracker
        self.debt_events = []
        self.current_debt = 0
    
    def assess_trust_debt(self):
        """
        Calculate current trust debt based on recent performance.
        
        Trust debt increases when:
        - High confidence predictions fail
        - Consecutive losses
        - Overconfidence vs accuracy
        
        Returns:
            debt_level: 0-10
            severity: "None" | "Low" | "Medium" | "High" | "Critical"
            action: What AI should do
        """
        recent = self.tracker.get_recent_predictions(n=10)
        
        if len(recent) < 3:
            return {
                "available": False,
                "debt": 0,
                "message": "Building trust history..."
            }
        
        completed = [p for p in recent if p.get('actualPrice')]
        
        if len(completed) < 2:
            return {
                "available": False,
                "debt": 0,
                "message": "Waiting for predictions to mature"
            }
        
        debt_points = 0
        
        # 1. High confidence failures (worst offense)
        for pred in completed:
            confidence = pred.get('signalValue', 0)
            was_correct = self._was_correct(pred)
            
            if not was_correct and confidence > 0.6:
                # High confidence failure = 2 debt points
                debt_points += 2
                self.debt_events.append({
                    "type": "high_confidence_failure",
                    "confidence": confidence,
                    "timestamp": pred.get('timestamp')
                })
            elif not was_correct and confidence > 0.4:
                # Medium confidence failure = 1 debt point
                debt_points += 1
        
        # 2. Consecutive losses
        consecutive_losses = 0
        for pred in reversed(completed):
            if not self._was_correct(pred):
                consecutive_losses += 1
            else:
                break
        
        if consecutive_losses >= 3:
            debt_points += consecutive_losses
        
        # 3. Overconfidence pattern
        avg_confidence = sum(p.get('signalValue', 0) for p in completed) / len(completed)
        accuracy = sum(1 for p in completed if self._was_correct(p)) / len(completed)
        
        if avg_confidence - accuracy > 0.2:
            debt_points += 2
        
        self.current_debt = debt_points
        
        # Determine severity
        if debt_points == 0:
            severity = "None"
            action = "normal_operation"
        elif debt_points <= 2:
            severity = "Low"
            action = "slight_caution"
        elif debt_points <= 4:
            severity = "Medium"
            action = "reduce_confidence"
        elif debt_points <= 6:
            severity = "High"
            action = "suppress_weak_signals"
        else:
            severity = "Critical"
            action = "force_neutral"
        
        return {
            "available": True,
            "debt": debt_points,
            "severity": severity,
            "action": action,
            "message": self._generate_debt_message(severity, debt_points),
            "events": self.debt_events[-5:],  # Recent debt events
            "sampleSize": len(completed)
        }
    
    def _was_correct(self, pred):
        """Check if prediction was correct"""
        current = pred['currentPrice']
        predicted = pred['predictedPrice']
        actual = pred['actualPrice']
        
        predicted_direction = "up" if predicted > current else "down"
        actual_direction = "up" if actual > current else "down"
        
        return predicted_direction == actual_direction
    
    def _generate_debt_message(self, severity, debt):
        """Generate user-facing message"""
        if severity == "None":
            return "Trust account in good standing"
        elif severity == "Low":
            return f"Minor trust debt ({debt} points) - exercising caution"
        elif severity == "Medium":
            return f"Trust debt elevated ({debt} points) - confidence reduced"
        elif severity == "High":
            return f"High trust debt ({debt} points) - weak signals suppressed"
        else:
            return f"Critical trust debt ({debt} points) - AI self-limiting"
    
    def pay_down_debt(self, amount=1):
        """Reduce debt after successful predictions"""
        self.current_debt = max(0, self.current_debt - amount)


class CognitiveBiasDetector:
    """
    OMEGA TIER: Detects known market biases.
    
    Biases detected:
    - FOMO (Fear of Missing Out)
    - Loss Aversion
    - Recency Bias
    - Anchoring
    
    Adjusts signals accordingly.
    """
    
    def __init__(self, backtest_tracker):
        self.tracker = backtest_tracker
    
    def detect_biases(self, prediction_data, market_data):
        """
        Scan for cognitive biases in current market state.
        
        Returns:
            biases_detected: list
            adjustments: dict
        """
        biases = []
        
        # 1. FOMO Detection (rapid price increase + high confidence)
        recent_return = market_data.get("recent_return", 0)
        confidence = prediction_data.get("signalValue", 0)
        
        if recent_return > 0.10 and confidence > 0.6 and "Bullish" in prediction_data.get("recommendation", ""):
            biases.append({
                "type": "FOMO",
                "severity": "High",
                "message": "FOMO detected - chasing recent gains",
                "adjustment": "reduce_bullish_confidence"
            })
        
        # 2. Loss Aversion (after losses, avoid further risk)
        consecutive_losses = prediction_data.get("drawdown", {}).get("consecutiveLosses", 0)
        
        if consecutive_losses >= 2 and confidence > 0.5:
            biases.append({
                "type": "Loss_Aversion",
                "severity": "Medium",
                "message": "Loss aversion - may be too cautious",
                "adjustment": "acknowledge_caution"
            })
        
        # 3. Recency Bias (overweighting recent data)
        stability = prediction_data.get("stability", {}).get("score", 1.0)
        
        if stability < 0.5:
            biases.append({
                "type": "Recency_Bias",
                "severity": "Medium",
                "message": "Recency bias - signal unstable",
                "adjustment": "reduce_confidence"
            })
        
        # 4. Anchoring (stuck on old price levels)
        # Simplified: if prediction is very close to current price
        current_price = prediction_data.get("currentPrice", 0)
        predicted_price = prediction_data.get("predictedPrice", 0)
        
        if current_price > 0:
            price_change_pct = abs(predicted_price - current_price) / current_price
            
            if price_change_pct < 0.02 and confidence > 0.4:  # Less than 2% change
                biases.append({
                    "type": "Anchoring",
                    "severity": "Low",
                    "message": "Anchoring - prediction too close to current price",
                    "adjustment": "flag_low_conviction"
                })
        
        return {
            "detected": bool(len(biases) > 0),
            "biases": biases,
            "count": int(len(biases)),
            "message": self._generate_bias_message(biases)
        }
    
    def _generate_bias_message(self, biases):
        """Generate user-facing message"""
        if not biases:
            return "No cognitive biases detected"
        
        bias_names = [b["type"] for b in biases]
        return f"Cognitive biases detected: {', '.join(bias_names)}"


class FailureTaxonomy:
    """
    OMEGA TIER: Categorizes failures for learning.
    
    Failure types:
    - Directional (wrong direction)
    - Timing (right direction, wrong timing)
    - Regime (wrong market classification)
    - Magnitude (right direction, wrong size)
    - Overconfidence (too confident)
    
    Failures become learning assets.
    """
    
    def __init__(self, backtest_tracker):
        self.tracker = backtest_tracker
        self.taxonomy = {
            "directional": [],
            "timing": [],
            "regime": [],
            "magnitude": [],
            "overconfidence": []
        }
    
    def classify_failures(self, n=10):
        """
        Analyze recent predictions and classify failures.
        
        Returns:
            taxonomy: dict of failure types
            insights: learning insights
        """
        recent = self.tracker.get_recent_predictions(n)
        completed = [p for p in recent if p.get('actualPrice')]
        
        if len(completed) < 3:
            return {
                "available": False,
                "message": "Insufficient completed predictions"
            }
        
        for pred in completed:
            current = pred['currentPrice']
            predicted = pred['predictedPrice']
            actual = pred['actualPrice']
            confidence = pred.get('signalValue', 0)
            
            # Classify failure type
            predicted_direction = "up" if predicted > current else "down"
            actual_direction = "up" if actual > current else "down"
            
            # 1. Directional failure
            if predicted_direction != actual_direction:
                self.taxonomy["directional"].append(pred)
            
            # 2. Magnitude failure (right direction, wrong size)
            elif predicted_direction == actual_direction:
                predicted_change = abs(predicted - current) / current
                actual_change = abs(actual - current) / current
                
                if abs(predicted_change - actual_change) > 0.05:  # 5% error
                    self.taxonomy["magnitude"].append(pred)
            
            # 3. Overconfidence failure
            if predicted_direction != actual_direction and confidence > 0.6:
                self.taxonomy["overconfidence"].append(pred)
        
        # Generate insights
        insights = self._generate_insights()
        
        return {
            "available": True,
            "taxonomy": {
                "directional": int(len(self.taxonomy["directional"])),
                "timing": int(len(self.taxonomy["timing"])),
                "regime": int(len(self.taxonomy["regime"])),
                "magnitude": int(len(self.taxonomy["magnitude"])),
                "overconfidence": int(len(self.taxonomy["overconfidence"]))
            },
            "insights": insights,
            "totalFailures": int(sum(len(v) for v in self.taxonomy.values())),
            "message": self._generate_taxonomy_message()
        }
    
    def _generate_insights(self):
        """Generate learning insights from failures"""
        insights = []
        
        # Most common failure type
        if any(self.taxonomy.values()):
            most_common = max(self.taxonomy, key=lambda k: len(self.taxonomy[k]))
            if len(self.taxonomy[most_common]) > 0:
                insights.append(f"Primary failure mode: {most_common}")
        
        # Overconfidence pattern
        if len(self.taxonomy["overconfidence"]) >= 2:
            insights.append("Persistent overconfidence detected")
        
        return insights
    
    def _generate_taxonomy_message(self):
        """Generate user-facing message"""
        total = sum(len(v) for v in self.taxonomy.values())
        
        if total == 0:
            return "No failures to classify"
        
        most_common = max(self.taxonomy, key=lambda k: len(self.taxonomy[k]))
        return f"Recent failures: {most_common.capitalize()} ({len(self.taxonomy[most_common])} instances)"
