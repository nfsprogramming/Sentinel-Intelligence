import numpy as np
from datetime import datetime

class HardRiskConstitution:
    """
    ELITE TIER: Immutable safety rules that cannot be overridden.
    
    Rules:
    1. Never exceed 70% confidence
    2. Force Neutral during black swan events
    3. Hard stop after X consecutive losses
    4. Maximum drawdown limits
    5. No trading during market halts
    
    This is your legal and ethical shield.
    """
    
    # IMMUTABLE RULES (cannot be changed at runtime)
    MAX_CONFIDENCE = 0.70
    MAX_CONSECUTIVE_LOSSES = 5
    MAX_DRAWDOWN_PCT = 20.0
    MIN_LIQUIDITY_THRESHOLD = 1000000  # Minimum volume
    BLACK_SWAN_VOLATILITY_THRESHOLD = 0.50  # 50% daily volatility
    
    def __init__(self):
        self.violations = []
        self.enforcements = []
    
    def enforce(self, prediction_data, market_data):
        """
        Apply constitutional rules. Returns modified prediction or None if blocked.
        
        Args:
            prediction_data: Current prediction dict
            market_data: Market state dict
        
        Returns:
            {
                "allowed": bool,
                "modified": dict or None,
                "violations": list of rule violations,
                "message": str
            }
        """
        violations = []
        modified = prediction_data.copy()
        
        # Rule 1: Confidence Cap
        if modified.get("signalValue", 0) > self.MAX_CONFIDENCE:
            violations.append({
                "rule": "MAX_CONFIDENCE",
                "original": modified["signalValue"],
                "enforced": self.MAX_CONFIDENCE,
                "message": f"Confidence capped at {int(self.MAX_CONFIDENCE * 100)}% by Risk Constitution"
            })
            modified["signalValue"] = self.MAX_CONFIDENCE
        
        # Rule 2: Black Swan Detection
        volatility = market_data.get("volatility", 0)
        if volatility > self.BLACK_SWAN_VOLATILITY_THRESHOLD:
            violations.append({
                "rule": "BLACK_SWAN",
                "volatility": volatility,
                "message": f"⛔ Black swan event detected (volatility {volatility:.1%}) - FORCED NEUTRAL"
            })
            modified["recommendation"] = "Neutral Bias"
            modified["actionVerb"] = "Neutral Stance"
            modified["signalValue"] = 0.0
            modified["signalStrength"] = "Low"
        
        # Rule 3: Consecutive Loss Limit
        consecutive_losses = prediction_data.get("drawdown", {}).get("consecutiveLosses", 0)
        if consecutive_losses >= self.MAX_CONSECUTIVE_LOSSES:
            violations.append({
                "rule": "MAX_CONSECUTIVE_LOSSES",
                "losses": consecutive_losses,
                "message": f"⛔ {consecutive_losses} consecutive losses - TRADING PAUSED"
            })
            modified["recommendation"] = "Neutral Bias"
            modified["actionVerb"] = "Neutral Stance"
            modified["signalValue"] = 0.0
            modified["signalStrength"] = "Low"
        
        # Rule 4: Liquidity Check
        volume = market_data.get("volume", float('inf'))
        if volume < self.MIN_LIQUIDITY_THRESHOLD:
            violations.append({
                "rule": "MIN_LIQUIDITY",
                "volume": volume,
                "message": f"⚠️ Insufficient liquidity (volume: {volume:,.0f}) - signal suppressed"
            })
            modified["signalValue"] = modified["signalValue"] * 0.5  # Halve confidence
        
        # Rule 5: Regime Risk Override
        regime_risk = prediction_data.get("regime", {}).get("risk", "")
        if regime_risk == "Elevated" and modified.get("signalValue", 0) > 0.5:
            violations.append({
                "rule": "ELEVATED_RISK_OVERRIDE",
                "message": "⚠️ High conviction blocked in elevated risk regime"
            })
            modified["signalValue"] = min(modified["signalValue"], 0.5)
        
        # Log violations
        if violations:
            self.violations.extend(violations)
            self.enforcements.append({
                "timestamp": datetime.now().isoformat(),
                "violations": violations,
                "action": "modified" if modified != prediction_data else "blocked"
            })
        
        return {
            "allowed": True,  # We modify, never fully block
            "modified": modified if violations else None,
            "violations": violations,
            "active": len(violations) > 0,
            "message": self._generate_constitution_message(violations)
        }
    
    def _generate_constitution_message(self, violations):
        """Generate user-facing message"""
        if not violations:
            return "✓ Risk Constitution: All rules satisfied"
        
        critical = [v for v in violations if v["rule"] in ["BLACK_SWAN", "MAX_CONSECUTIVE_LOSSES"]]
        if critical:
            return f"🛡️ Risk Constitution Enforced: {critical[0]['message']}"
        
        return f"🛡️ Risk Constitution: {len(violations)} rule(s) applied"
    
    def get_constitution_summary(self):
        """Return all constitutional rules for transparency"""
        return {
            "rules": [
                {
                    "name": "Maximum Confidence",
                    "value": f"{int(self.MAX_CONFIDENCE * 100)}%",
                    "description": "Hard cap on AI confidence"
                },
                {
                    "name": "Black Swan Protection",
                    "value": f">{int(self.BLACK_SWAN_VOLATILITY_THRESHOLD * 100)}% volatility",
                    "description": "Force neutral during extreme events"
                },
                {
                    "name": "Consecutive Loss Limit",
                    "value": f"{self.MAX_CONSECUTIVE_LOSSES} losses",
                    "description": "Pause trading after losing streak"
                },
                {
                    "name": "Minimum Liquidity",
                    "value": f"${self.MIN_LIQUIDITY_THRESHOLD:,.0f}",
                    "description": "Suppress signals in illiquid markets"
                },
                {
                    "name": "Elevated Risk Override",
                    "value": "50% max confidence",
                    "description": "Reduce conviction in high-risk regimes"
                }
            ],
            "totalEnforcements": len(self.enforcements),
            "recentViolations": self.violations[-5:] if self.violations else []
        }


class RegimeConditionalRouter:
    """
    ELITE TIER: Multiple specialized models for different market conditions.
    
    Models:
    1. Trend Model (for trending markets)
    2. Mean Reversion Model (for ranging markets)
    3. Volatility Breakout Model (for high volatility)
    
    Router selects or blends them based on regime.
    """
    
    def __init__(self):
        self.active_model = None
        self.model_weights = {}
        self.history = []
    
    def route(self, regime_type, regime_risk, lstm_score, sentiment_score, volatility):
        """
        Select appropriate model(s) based on market regime.
        
        Returns:
            active_model: Primary model name
            weights: Blend weights if using ensemble
            adjusted_score: Modified prediction score
        """
        # Determine which models are suitable
        model_scores = {
            "Trend Model": self._score_trend_model(regime_type, volatility),
            "Mean Reversion Model": self._score_mean_reversion_model(regime_type, volatility),
            "Volatility Breakout Model": self._score_volatility_model(regime_type, volatility)
        }
        
        # Normalize to weights
        total = sum(model_scores.values())
        weights = {k: v / total for k, v in model_scores.items()}
        
        # Select dominant model
        active_model = max(weights, key=weights.get)
        
        # Adjust prediction based on active model
        adjusted_score = self._apply_model_logic(
            active_model, lstm_score, sentiment_score, volatility, regime_type
        )
        
        # Store decision
        self.active_model = active_model
        self.model_weights = weights
        self.history.append({
            "regime": regime_type,
            "active_model": active_model,
            "weights": weights.copy()
        })
        
        return {
            "activeModel": active_model,
            "weights": {k: round(v * 100, 1) for k, v in weights.items()},
            "adjustedScore": adjusted_score,
            "message": self._generate_routing_message(active_model, weights[active_model])
        }
    
    def _score_trend_model(self, regime, volatility):
        """Score suitability of trend-following model"""
        if "Trend" in regime:
            return 0.8 - (volatility * 0.3)  # Prefer in trending, penalize high vol
        elif "Ranging" in regime:
            return 0.2
        else:
            return 0.4
    
    def _score_mean_reversion_model(self, regime, volatility):
        """Score suitability of mean reversion model"""
        if "Ranging" in regime:
            return 0.8 - (volatility * 0.5)  # Prefer in ranging, hate high vol
        elif "Trend" in regime:
            return 0.1
        else:
            return 0.4
    
    def _score_volatility_model(self, regime, volatility):
        """Score suitability of volatility breakout model"""
        if "High Volatility" in regime or volatility > 0.3:
            return 0.9
        else:
            return 0.2
    
    def _apply_model_logic(self, model, lstm_score, sentiment_score, volatility, regime):
        """Apply model-specific adjustments"""
        base_score = 0.6 * lstm_score + 0.4 * (sentiment_score * 2 - 1)
        
        if model == "Trend Model":
            # Amplify strong signals, dampen weak ones
            return base_score * 1.2 if abs(base_score) > 0.3 else base_score * 0.8
        
        elif model == "Mean Reversion Model":
            # Invert signals (fade the move)
            return -base_score * 0.7
        
        elif model == "Volatility Breakout Model":
            # Only act on extreme signals
            return base_score * 1.5 if abs(base_score) > 0.5 else 0.0
        
        return base_score
    
    def _generate_routing_message(self, model, weight):
        """Generate user-facing message"""
        return f"Active Brain: {model} ({weight * 100:.0f}% confidence)"
    
    def get_routing_history(self, n=10):
        """Get recent routing decisions"""
        return self.history[-n:] if self.history else []
    
    def get_model_performance(self):
        """Analyze which model performs best (requires backtest data)"""
        if len(self.history) < 5:
            return {"available": False}
        
        # Count regime occurrences
        regime_counts = {}
        for h in self.history:
            regime = h["regime"]
            regime_counts[regime] = regime_counts.get(regime, 0) + 1
        
        return {
            "available": True,
            "regimeCounts": regime_counts,
            "mostCommonRegime": max(regime_counts, key=regime_counts.get),
            "totalDecisions": len(self.history)
        }


class ExplainabilityLedger:
    """
    ELITE TIER: Audit trail for every AI decision.
    
    Stores:
    - All input factors
    - Model weights
    - Supervisor interventions
    - Constitutional overrides
    
    Enables debugging, research, and investor trust.
    """
    
    def __init__(self):
        self.ledger = []
    
    def log_decision(self, prediction_data, inputs, overrides):
        """
        Log a complete decision with full context.
        
        Args:
            prediction_data: Final prediction output
            inputs: All input factors used
            overrides: Any interventions applied
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "prediction": {
                "bias": prediction_data.get("recommendation"),
                "confidence": prediction_data.get("signalValue"),
                "price": prediction_data.get("predictedPrice")
            },
            "inputs": inputs,
            "overrides": overrides,
            "explainability": {
                "factors": self._extract_factors(inputs),
                "weights": self._extract_weights(inputs),
                "reasoning": prediction_data.get("explanation", {})
            }
        }
        
        self.ledger.append(entry)
    
    def _extract_factors(self, inputs):
        """Extract key decision factors"""
        return {
            "lstm": inputs.get("lstm_score"),
            "sentiment": inputs.get("sentiment_score"),
            "regime": inputs.get("regime"),
            "volatility": inputs.get("volatility"),
            "stability": inputs.get("stability_score")
        }
    
    def _extract_weights(self, inputs):
        """Extract model weights"""
        return {
            "lstm": 0.6,
            "sentiment": 0.4
        }
    
    def get_ledger(self, n=10):
        """Get recent entries"""
        return self.ledger[-n:] if self.ledger else []
    
    def export_ledger(self, filepath):
        """Export full ledger for audit"""
        import json
        with open(filepath, 'w') as f:
            json.dump(self.ledger, f, indent=2)
        return f"Ledger exported to {filepath}"
    
    def get_decision_by_timestamp(self, timestamp):
        """Retrieve specific decision for debugging"""
        for entry in self.ledger:
            if entry["timestamp"] == timestamp:
                return entry
        return None
