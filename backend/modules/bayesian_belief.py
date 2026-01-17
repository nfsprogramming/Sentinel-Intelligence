import numpy as np
from scipy.stats import norm

class BayesianBeliefEngine:
    """
    ELITE TIER: Probabilistic belief system instead of hard predictions.
    
    Maintains P(Bullish), P(Neutral), P(Bearish) and updates via Bayes' theorem.
    No flip-flops - smooth belief transitions.
    """
    
    def __init__(self):
        # Prior beliefs (start neutral)
        self.beliefs = {
            "Bullish": 0.33,
            "Neutral": 0.34,
            "Bearish": 0.33
        }
        self.history = []
    
    def update_beliefs(self, lstm_score, sentiment_score, regime_risk, stability_score):
        """
        Bayesian update based on new evidence.
        
        Args:
            lstm_score: -1 to 1 (LSTM prediction)
            sentiment_score: 0 to 1 (FinBERT)
            regime_risk: "Low", "Moderate", "Elevated"
            stability_score: 0 to 1
        
        Returns:
            Updated belief distribution
        """
        # Convert scores to likelihoods
        bullish_likelihood = self._calculate_likelihood(lstm_score, sentiment_score, "Bullish")
        neutral_likelihood = self._calculate_likelihood(lstm_score, sentiment_score, "Neutral")
        bearish_likelihood = self._calculate_likelihood(lstm_score, sentiment_score, "Bearish")
        
        # Apply regime penalty (high risk = more uncertain)
        regime_penalty = {
            "Low": 1.0,
            "Moderate": 0.85,
            "Elevated": 0.6
        }.get(regime_risk, 0.8)
        
        # Apply stability bonus (high stability = more confident)
        stability_bonus = 0.5 + (stability_score * 0.5)  # 0.5 to 1.0
        
        # Bayes update: P(H|E) = P(E|H) * P(H) / P(E)
        unnormalized = {
            "Bullish": bullish_likelihood * self.beliefs["Bullish"] * regime_penalty * stability_bonus,
            "Neutral": neutral_likelihood * self.beliefs["Neutral"] * regime_penalty,
            "Bearish": bearish_likelihood * self.beliefs["Bearish"] * regime_penalty * stability_bonus
        }
        
        # Normalize to sum to 1
        total = sum(unnormalized.values())
        self.beliefs = {k: v / total for k, v in unnormalized.items()}
        
        # Store history
        self.history.append({
            "beliefs": self.beliefs.copy(),
            "evidence": {
                "lstm": lstm_score,
                "sentiment": sentiment_score,
                "regime": regime_risk,
                "stability": stability_score
            }
        })
        
        # Determine dominant belief
        dominant = max(self.beliefs, key=self.beliefs.get)
        confidence = self.beliefs[dominant]
        
        # Calculate entropy (uncertainty measure)
        entropy = -sum(p * np.log2(p) if p > 0 else 0 for p in self.beliefs.values())
        max_entropy = np.log2(3)  # Maximum for 3 states
        uncertainty = entropy / max_entropy  # 0 = certain, 1 = maximum uncertainty
        
        return {
            "beliefs": {k: round(v * 100, 1) for k, v in self.beliefs.items()},
            "dominant": dominant,
            "confidence": round(confidence * 100, 1),
            "uncertainty": round(uncertainty, 2),
            "message": self._generate_message(dominant, confidence, uncertainty)
        }
    
    def _calculate_likelihood(self, lstm_score, sentiment_score, hypothesis):
        """Calculate P(Evidence | Hypothesis)"""
        # Combine LSTM and sentiment
        combined_score = 0.6 * lstm_score + 0.4 * (sentiment_score * 2 - 1)  # Convert sentiment to -1 to 1
        
        if hypothesis == "Bullish":
            # Bullish is more likely when scores are positive
            likelihood = norm.pdf(combined_score, loc=0.5, scale=0.3)
        elif hypothesis == "Bearish":
            # Bearish is more likely when scores are negative
            likelihood = norm.pdf(combined_score, loc=-0.5, scale=0.3)
        else:  # Neutral
            # Neutral is more likely when scores are near zero
            likelihood = norm.pdf(combined_score, loc=0.0, scale=0.2)
        
        return max(likelihood, 0.01)  # Avoid zero
    
    def _generate_message(self, dominant, confidence, uncertainty):
        """Generate human-readable belief statement"""
        if uncertainty > 0.8:
            return f"High uncertainty - beliefs evenly distributed"
        elif confidence > 0.6:
            return f"Strong {dominant} belief ({confidence:.0f}%)"
        elif confidence > 0.45:
            return f"Moderate {dominant} lean ({confidence:.0f}%)"
        else:
            return f"Weak {dominant} tendency - high uncertainty"
    
    def get_belief_trend(self, n=5):
        """Analyze how beliefs have changed over last N updates"""
        if len(self.history) < 2:
            return {"available": False}
        
        recent = self.history[-n:]
        
        # Track dominant belief changes
        dominants = [max(h["beliefs"], key=h["beliefs"].get) for h in recent]
        changes = sum(1 for i in range(1, len(dominants)) if dominants[i] != dominants[i-1])
        
        # Calculate belief volatility
        bullish_vals = [h["beliefs"]["Bullish"] for h in recent]
        volatility = np.std(bullish_vals)
        
        return {
            "available": True,
            "changes": changes,
            "volatility": round(volatility, 3),
            "stable": changes <= 1 and volatility < 0.1,
            "message": f"Belief changed {changes} times (last {len(recent)} updates)"
        }


class MetaModelGovernor:
    """
    ELITE TIER: Supervisor AI that watches the main AI.
    
    Monitors for:
    - Prediction drift
    - Error spikes
    - Regime mismatch
    - Overconfidence
    
    Can intervene by forcing Neutral or reducing confidence.
    """
    
    def __init__(self, backtest_tracker):
        self.tracker = backtest_tracker
        self.interventions = []
    
    def assess_and_intervene(self, prediction_data):
        """
        Evaluate if intervention is needed.
        
        Returns:
            intervention_active: bool
            reason: str or None
            action: "force_neutral" | "reduce_confidence" | None
            severity: "low" | "medium" | "high"
        """
        issues = []
        
        # 1. Check for error spike
        recent_errors = self._check_error_spike()
        if recent_errors:
            issues.append(recent_errors)
        
        # 2. Check for regime mismatch
        regime_issue = self._check_regime_mismatch(prediction_data)
        if regime_issue:
            issues.append(regime_issue)
        
        # 3. Check for overconfidence
        overconfidence = self._check_overconfidence(prediction_data)
        if overconfidence:
            issues.append(overconfidence)
        
        # 4. Check for prediction drift
        drift = self._check_prediction_drift()
        if drift:
            issues.append(drift)
        
        if not issues:
            return {
                "active": False,
                "reason": None,
                "action": None,
                "severity": None,
                "message": "Supervisor: All systems nominal"
            }
        
        # Determine most severe issue
        most_severe = max(issues, key=lambda x: {"low": 1, "medium": 2, "high": 3}[x["severity"]])
        
        # Log intervention
        self.interventions.append({
            "timestamp": prediction_data.get("predictionTime"),
            "reason": most_severe["reason"],
            "action": most_severe["action"],
            "severity": most_severe["severity"]
        })
        
        return {
            "active": True,
            "reason": most_severe["reason"],
            "action": most_severe["action"],
            "severity": most_severe["severity"],
            "message": f"⚠️ Supervisor Intervention: {most_severe['reason']}"
        }
    
    def _check_error_spike(self):
        """Detect sudden increase in prediction errors"""
        recent = self.tracker.get_recent_predictions(n=10)
        if len(recent) < 5:
            return None
        
        completed = [p for p in recent if p.get('actualPrice')]
        if len(completed) < 3:
            return None
        
        # Calculate recent error rate
        errors = []
        for pred in completed[-3:]:
            error = abs(pred['predictedPrice'] - pred['actualPrice']) / pred['currentPrice']
            errors.append(error)
        
        avg_error = np.mean(errors)
        
        if avg_error > 0.15:  # 15% average error
            return {
                "reason": "Error spike detected (avg 15%+)",
                "action": "reduce_confidence",
                "severity": "high"
            }
        
        return None
    
    def _check_regime_mismatch(self, prediction_data):
        """Check if model is suited for current regime"""
        regime = prediction_data.get("regime", {}).get("type", "")
        risk = prediction_data.get("regime", {}).get("risk", "")
        
        # High volatility + high confidence = mismatch
        if risk == "Elevated" and prediction_data.get("signalValue", 0) > 0.5:
            return {
                "reason": "High conviction in elevated risk regime",
                "action": "reduce_confidence",
                "severity": "medium"
            }
        
        return None
    
    def _check_overconfidence(self, prediction_data):
        """Detect overconfidence patterns"""
        confidence = prediction_data.get("signalValue", 0)
        stability = prediction_data.get("stability", {}).get("score", 1.0)
        
        # High confidence + low stability = overconfidence
        if confidence > 0.6 and stability < 0.5:
            return {
                "reason": "Overconfidence with low signal stability",
                "action": "reduce_confidence",
                "severity": "high"
            }
        
        return None
    
    def _check_prediction_drift(self):
        """Detect if predictions are drifting from reality"""
        recent = self.tracker.get_recent_predictions(n=10)
        if len(recent) < 5:
            return None
        
        completed = [p for p in recent if p.get('actualPrice')]
        if len(completed) < 3:
            return None
        
        # Check if predictions consistently miss in same direction
        biases = []
        for pred in completed:
            predicted_direction = "up" if pred['predictedPrice'] > pred['currentPrice'] else "down"
            actual_direction = "up" if pred['actualPrice'] > pred['currentPrice'] else "down"
            biases.append(predicted_direction != actual_direction)
        
        # If all recent predictions wrong in same way = drift
        if all(biases):
            return {
                "reason": "Systematic prediction drift detected",
                "action": "force_neutral",
                "severity": "high"
            }
        
        return None
    
    def get_intervention_history(self, n=5):
        """Get recent interventions"""
        return self.interventions[-n:] if self.interventions else []


class SelfScoringHonestyIndex:
    """
    ELITE TIER: AI grades itself publicly.
    
    Tracks:
    - Overconfidence ratio
    - False conviction rate
    - Stability score
    - Calibration quality
    
    Displays an "AI Honesty Score" (0-100).
    """
    
    def __init__(self, backtest_tracker):
        self.tracker = backtest_tracker
    
    def calculate_honesty_score(self):
        """
        Calculate comprehensive honesty metrics.
        
        Returns:
            overall_score: 0-100
            components: breakdown of score
        """
        recent = self.tracker.get_recent_predictions(n=50)
        
        if len(recent) < 10:
            return {
                "available": False,
                "score": None,
                "message": "Insufficient data for honesty assessment"
            }
        
        completed = [p for p in recent if p.get('actualPrice')]
        
        if len(completed) < 5:
            return {
                "available": False,
                "score": None,
                "message": "Waiting for predictions to mature"
            }
        
        # 1. Calibration Score (are high confidence predictions actually more accurate?)
        calibration = self._calculate_calibration(completed)
        
        # 2. Overconfidence Ratio (confidence vs actual accuracy)
        overconfidence = self._calculate_overconfidence(completed)
        
        # 3. Stability Score (consistent behavior)
        stability = self._calculate_stability_score(recent)
        
        # 4. Transparency Score (explainability provided)
        transparency = 100  # Always 100 since we provide explanations
        
        # Weighted average
        overall = (
            calibration * 0.35 +
            overconfidence * 0.35 +
            stability * 0.20 +
            transparency * 0.10
        )
        
        return {
            "available": True,
            "score": round(overall, 1),
            "grade": self._get_grade(overall),
            "components": {
                "calibration": round(calibration, 1),
                "overconfidence": round(overconfidence, 1),
                "stability": round(stability, 1),
                "transparency": transparency
            },
            "message": self._generate_honesty_message(overall),
            "sampleSize": len(completed)
        }
    
    def _calculate_calibration(self, completed):
        """Check if confidence matches accuracy"""
        if not completed:
            return 50
        
        # Group by confidence level
        high_conf = [p for p in completed if p.get('signalValue', 0) > 0.5]
        low_conf = [p for p in completed if p.get('signalValue', 0) <= 0.5]
        
        if not high_conf and not low_conf:
            return 50
        
        # Calculate accuracy for each group
        high_acc = sum(1 for p in high_conf if self._was_correct(p)) / len(high_conf) if high_conf else 0
        low_acc = sum(1 for p in low_conf if self._was_correct(p)) / len(low_conf) if low_conf else 0
        
        # Good calibration = high conf predictions are more accurate
        if high_acc > low_acc:
            return min(100, 50 + (high_acc - low_acc) * 200)
        else:
            return max(0, 50 - (low_acc - high_acc) * 200)
    
    def _calculate_overconfidence(self, completed):
        """Penalize overconfidence"""
        if not completed:
            return 50
        
        total_confidence = sum(p.get('signalValue', 0) for p in completed)
        avg_confidence = total_confidence / len(completed)
        
        accuracy = sum(1 for p in completed if self._was_correct(p)) / len(completed)
        
        # Overconfidence = confidence > accuracy
        diff = avg_confidence - accuracy
        
        if diff > 0.2:  # Severely overconfident
            return 20
        elif diff > 0.1:  # Moderately overconfident
            return 50
        elif diff > 0:  # Slightly overconfident
            return 70
        else:  # Well-calibrated or underconfident
            return 90
    
    def _calculate_stability_score(self, recent):
        """Measure behavioral consistency"""
        if len(recent) < 5:
            return 50
        
        # Check for flip-flops
        biases = [p.get('bias', 'Neutral') for p in recent[-10:]]
        changes = sum(1 for i in range(1, len(biases)) if biases[i] != biases[i-1])
        
        # Fewer changes = more stable
        if changes <= 2:
            return 100
        elif changes <= 4:
            return 75
        elif changes <= 6:
            return 50
        else:
            return 25
    
    def _was_correct(self, pred):
        """Check if prediction direction was correct"""
        current = pred['currentPrice']
        predicted = pred['predictedPrice']
        actual = pred['actualPrice']
        
        predicted_direction = "up" if predicted > current else "down"
        actual_direction = "up" if actual > current else "down"
        
        return predicted_direction == actual_direction
    
    def _get_grade(self, score):
        """Convert score to letter grade"""
        if score >= 90:
            return "A+"
        elif score >= 80:
            return "A"
        elif score >= 70:
            return "B"
        elif score >= 60:
            return "C"
        else:
            return "D"
    
    def _generate_honesty_message(self, score):
        """Generate human-readable assessment"""
        if score >= 85:
            return "Excellent - AI is well-calibrated and honest"
        elif score >= 70:
            return "Good - Minor calibration issues"
        elif score >= 50:
            return "Fair - Some overconfidence detected"
        else:
            return "Poor - Significant calibration problems"
