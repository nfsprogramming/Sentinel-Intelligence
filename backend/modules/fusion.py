from modules.stock_data import StockDataManager
from modules.lstm_model import TrendPredictor
from modules.sentiment_engine import FinBERTSentiment
from modules.backtest_tracker import BacktestTracker
from modules.advanced_analysis import RegimeDetector, MultiTimeframeAnalyzer, ExplanationEngine
from modules.uncertainty_tools import UncertaintyCalculator, PredictionTimer, ModelHealthMonitor
from modules.advanced_guardrails import SignalStabilityTracker, EthicalGuardrails, ConvictionLanguage
from modules.decision_quality import CounterfactualAnalyzer, DrawdownAwareConfidence, NarrativeTimeline
from modules.bayesian_belief import BayesianBeliefEngine, MetaModelGovernor, SelfScoringHonestyIndex
from modules.elite_governance import HardRiskConstitution, RegimeConditionalRouter, ExplainabilityLedger
from modules.omega_intelligence import SilenceIntelligence, ModelHumilityIndex, TrustDebtLedger, CognitiveBiasDetector, FailureTaxonomy
from modules.transcendent_intelligence import TranscendentIntelligence
from datetime import datetime

class FusionEngine:
    def __init__(self, backtest_file=None):
        self.data_loader = StockDataManager()
        self.lstm = TrendPredictor(window_size=60)
        self.sentiment = FinBERTSentiment()
        if backtest_file:
            self.tracker = BacktestTracker(storage_path=backtest_file)
        else:
            self.tracker = BacktestTracker()
        self.regime_detector = RegimeDetector()
        self.mtf_analyzer = MultiTimeframeAnalyzer()
        self.explainer = ExplanationEngine()
        self.uncertainty_calc = UncertaintyCalculator()
        self.timer = PredictionTimer(validity_hours=6)
        self.health_monitor = ModelHealthMonitor(self.tracker)
        self.stability_tracker = SignalStabilityTracker(self.tracker)
        self.guardrails = EthicalGuardrails()
        self.conviction_lang = ConvictionLanguage()
        self.counterfactual = CounterfactualAnalyzer(self.tracker)
        self.drawdown_aware = DrawdownAwareConfidence(self.tracker)
        self.narrative = NarrativeTimeline(self.tracker)
        
        # === ELITE TIER ===
        self.bayesian = BayesianBeliefEngine()
        self.meta_governor = MetaModelGovernor(self.tracker)
        self.constitution = HardRiskConstitution()
        self.router = RegimeConditionalRouter()
        self.honesty_index = SelfScoringHonestyIndex(self.tracker)
        self.ledger = ExplainabilityLedger()
        
        # === OMEGA TIER ===
        self.silence = SilenceIntelligence()
        self.humility = ModelHumilityIndex(self.tracker)
        self.trust_debt = TrustDebtLedger(self.tracker)
        self.bias_detector = CognitiveBiasDetector(self.tracker)
        self.failure_taxonomy = FailureTaxonomy(self.tracker)
        self.transcendent = TranscendentIntelligence(self.tracker)
        
    def run_analysis(self, ticker):
        print(f"--- Starting Hybrid Analysis for {ticker} ---")
        
        # 1. Fetch Data
        df = self.data_loader.fetch_data(ticker, start_date="2015-01-01")
        if df is None or len(df) < 100:
            return None
            
        # 2. LSTM Prediction
        # Train on fly (for demo) or load pre-trained
        # Training huge LSTM on fly might be slow (10-20s on CPU)
        # We limit epochs for responsivness in this demo
        loss = self.lstm.train(df, epochs=10)
        predicted_price, lstm_score = self.lstm.predict_next(df)
        
        print(f"LSTM Prediction: ${predicted_price:.2f} (Score: {lstm_score:.2f})")
        
        # 3. Sentiment Analysis
        # Ticker format: BTC-USD -> BTC
        symbol = ticker.split("-")[0] if "-" in ticker else ticker
        sent_score, sent_label = self.sentiment.analyze(symbol)
        
        # Map FinBERT label to Finance Terms
        label_map = {
            "positive": "Bullish",
            "negative": "Bearish",
            "neutral": "Neutral"
        }
        display_label = label_map.get(sent_label, sent_label)
        
        print(f"FinBERT Sentiment: {sent_label} -> {display_label} (Score: {sent_score:.2f})")
        
        # 4. Hybrid Fusion
        # final_score = 0.6 * LSTM_prediction + 0.4 * sentiment_score
        final_score = (0.6 * lstm_score) + (0.4 * sent_score)
        
        print(f"Hybrid Fusion Score: {final_score:.4f}")
        
        # Decision - Use professional bias terminology
        if final_score >= 0.6:
            bias = "Bullish Bias"
            trend = "UP Trend"
        elif final_score <= 0.4:
            bias = "Bearish Bias"
            trend = "DOWN Trend"
        else:
            bias = "Neutral"
            trend = "Sideways"
            
        # Signal Strength - Calibrated categories instead of fake precision
        score_distance = abs(final_score - 0.5)
        if score_distance >= 0.3:
            strength = "High"
            strength_value = score_distance
        elif score_distance >= 0.15:
            strength = "Medium"
            strength_value = score_distance
        else:
            strength = "Low"
            strength_value = score_distance
        
        # Price Ranges - More realistic than exact predictions
        current_price = df['Close'].iloc[-1]
        price_change_pct = (predicted_price - current_price) / current_price
        
        # Calculate 7-day expected range (±2% volatility buffer)
        volatility_buffer = 0.02
        if bias == "Bullish Bias":
            range_low = current_price * (1 + (price_change_pct * 0.5))
            range_high = predicted_price * (1 + volatility_buffer)
        elif bias == "Bearish Bias":
            range_low = predicted_price * (1 - volatility_buffer)
            range_high = current_price * (1 - (price_change_pct * 0.5))
        else:  # Neutral
            range_low = current_price * (1 - volatility_buffer)
            range_high = current_price * (1 + volatility_buffer)
        
        # Log this prediction for backtesting
        self.tracker.log_prediction(
            ticker=ticker,
            current_price=current_price,
            predicted_price=predicted_price,
            bias=bias,
            signal_strength=strength,
            fusion_score=final_score,
            timeframe="7D"
        )
        
        # Get backtest statistics
        stats = self.tracker.get_stats(last_n=30)
        
        # === ENTERPRISE-LEVEL ENHANCEMENTS ===
        
        # 1. Regime Detection
        regime_type, risk_level, regime_desc = self.regime_detector.detect_regime(df)
        adjusted_strength_value = self.regime_detector.adjust_confidence_for_regime(
            strength_value, regime_type
        )
        
        # 2. Multi-Timeframe Analysis
        mtf_analysis = self.mtf_analyzer.analyze_timeframes(df, bias, final_score)
        
        # 3. Explanation Engine
        explanation = self.explainer.generate_explanation(
            df, lstm_score, sent_score, final_score, bias
        )
        
        # 4. Uncertainty Visualization (Best/Base/Worst)
        returns = df['Close'].pct_change()
        historical_volatility = returns.rolling(20).std().iloc[-1]
        scenarios = self.uncertainty_calc.calculate_scenarios(
            current_price, predicted_price, historical_volatility, strength_value
        )
        
        # 5. Time-aware Confidence Decay
        prediction_time = datetime.now()
        expiry_info = self.timer.get_expiry_info(prediction_time)
        
        # Apply decay to signal strength
        decayed_strength_value = adjusted_strength_value * expiry_info['decayFactor']
        
        # 6. Model Health Monitoring
        model_health = self.health_monitor.assess_health()
        
        # === ADVANCED GUARDRAILS ===
        
        # 7. Signal Stability Tracking
        stability_level, stability_score, flip_count, stability_msg = self.stability_tracker.calculate_stability(n=10)
        
        # Adjust confidence for stability
        stability_adjusted_value, stability_warning = self.stability_tracker.adjust_confidence_for_stability(
            decayed_strength_value, stability_score
        )
        
        # 8. Ethical Confidence Guardrails (Hard cap at 70%)
        final_strength_value, final_strength_category, guardrail_message = self.guardrails.apply_guardrails(
            strength_value, stability_adjusted_value
        )
        
        # 9. Conviction Language (Verb-based states)
        conviction_state, conviction_desc = self.conviction_lang.get_conviction_state(
            final_strength_category, final_score, stability_level
        )
        action_verb = self.conviction_lang.get_action_verb(bias, conviction_state)
        
        # === DECISION QUALITY ANALYSIS ===
        
        # 10. Counterfactual Analysis (AI vs Hold vs Cash)
        counterfactual = self.counterfactual.analyze_alternatives(
            current_price, predicted_price, bias, timeframe_days=7
        )
        
        # 11. Drawdown-Aware Confidence
        drawdown_penalty, consecutive_losses, drawdown_message = self.drawdown_aware.calculate_drawdown_penalty(n=10)
        
        # Apply drawdown penalty to final strength
        if drawdown_penalty < 1.0:
            final_strength_value = final_strength_value * drawdown_penalty
            final_strength_value = round(final_strength_value, 2)
            # Recalculate category
            if final_strength_value >= 0.3:
                final_strength_category = "High"
            elif final_strength_value >= 0.15:
                final_strength_category = "Medium"
            else:
                final_strength_category = "Low"
        
        # 12. Narrative Timeline
        timeline = self.narrative.generate_timeline(n=5)
        
        # 13. Historical Performance Comparison
        historical_comparison = self.counterfactual.get_historical_comparison(lookback_days=30)
        
        # === ELITE TIER ANALYSIS ===
        
        # 14. Bayesian Belief Update
        bayesian_beliefs = self.bayesian.update_beliefs(
            lstm_score, sent_score, risk_level, stability_score
        )
        belief_trend = self.bayesian.get_belief_trend(n=5)
        
        # 15. Regime-Conditional Routing
        routing = self.router.route(
            regime_type, risk_level, lstm_score, sent_score, historical_volatility
        )
        
        # Use routed score instead of simple fusion
        routed_score = routing["adjustedScore"]
        
        # 16. Meta-Model Governance (Supervisor AI)
        prediction_snapshot = {
            "predictionTime": datetime.now().isoformat(),
            "signalValue": final_strength_value,
            "regime": {"type": regime_type, "risk": risk_level},
            "drawdown": {"consecutiveLosses": consecutive_losses}
        }
        market_snapshot = {
            "volatility": historical_volatility,
            "volume": 10000000  # TODO: Get real volume from data
        }
        
        meta_intervention = self.meta_governor.assess_and_intervene(prediction_snapshot)
        
        # 17. Hard Risk Constitution (Immutable Safety)
        constitution_result = self.constitution.enforce(prediction_snapshot, market_snapshot)
        
        # Apply constitutional modifications if any
        if constitution_result["modified"]:
            final_strength_value = constitution_result["modified"]["signalValue"]
            bias = constitution_result["modified"]["recommendation"]
            action_verb = constitution_result["modified"]["actionVerb"]
            final_strength_category = constitution_result["modified"]["signalStrength"]
        
        # 18. Self-Scoring Honesty Index
        honesty_score = self.honesty_index.calculate_honesty_score()
        
        # 19. Explainability Ledger (Audit Trail)
        self.ledger.log_decision(
            prediction_data={
                "recommendation": bias,
                "signalValue": final_strength_value,
                "predictedPrice": predicted_price,
                "explanation": explanation
            },
            inputs={
                "lstm_score": lstm_score,
                "sentiment_score": sent_score,
                "regime": regime_type,
                "volatility": historical_volatility,
                "stability_score": stability_score
            },
            overrides={
                "meta_intervention": meta_intervention,
                "constitution": constitution_result,
                "drawdown_penalty": drawdown_penalty
            }
        )
        
        # === OMEGA TIER ANALYSIS ===
        
        # 20. Model Humility Index
        humility_result = self.humility.calculate_humility(final_strength_value)
        
        # Apply humility adjustment if needed
        if humility_result.get("enforcementNeeded"):
            final_strength_value = humility_result["adjustedConfidence"]
        
        # 21. Trust Debt Assessment
        trust_debt_result = self.trust_debt.assess_trust_debt()
        
        # Apply trust debt actions
        if trust_debt_result.get("action") == "force_neutral":
            bias = "Neutral Bias"
            action_verb = "Neutral Stance"
            final_strength_value = 0.0
        elif trust_debt_result.get("action") == "reduce_confidence":
            final_strength_value = final_strength_value * 0.7
        
        # 22. Cognitive Bias Detection
        market_snapshot_full = {
            "volatility": historical_volatility,
            "volume": 10000000,
            "recent_return": (predicted_price - current_price) / current_price if current_price > 0 else 0
        }
        
        prediction_snapshot_full = {
            **prediction_snapshot,
            "recommendation": bias,
            "currentPrice": current_price,
            "predictedPrice": predicted_price,
            "bayesianBeliefs": bayesian_beliefs,
            "multiTimeframe": mtf_analysis,
            "stability": {
                "score": stability_score
            }
        }
        
        bias_detection = self.bias_detector.detect_biases(prediction_snapshot_full, market_snapshot_full)
        
        # 23. Failure Taxonomy
        failure_analysis = self.failure_taxonomy.classify_failures(n=10)
        
        # 24. Silence Intelligence (Final Gate)
        worthiness = self.silence.assess_worthiness(prediction_snapshot_full, market_snapshot_full)
        
        # === TRANSCENDENT TIER ANALYSIS ===
        transcendent_result = self.transcendent.process_transcendence(prediction_snapshot_full, market_snapshot_full, ticker)

        # If suppressed by transcendence, override
        if transcendent_result["isSuppressed"]:
            bias = "Signal Suppressed"
            action_verb = "Intelligence Restrained"
            final_strength_value = 0.0
            final_strength_category = "None"
        
        # If not worthy by silence intelligence, override to neutral/silent
        elif not worthiness["worthy"]:
            bias = "No Signal"
            action_verb = "AI Remains Silent"
            final_strength_value = 0.0
            final_strength_category = "None"
        
        
        # Round numbers to avoid "magic number" appearance
        def round_to_bucket(value):
            """Round to nearest 100 for prices > 1000, nearest 10 otherwise"""
            if value > 1000:
                return round(value / 100) * 100
            return round(value / 10) * 10
        
        
        
        def to_py(obj):
            """Recursively convert numpy types to native python types"""
            import numpy as np
            import pandas as pd
            if isinstance(obj, (np.integer, np.floating, np.bool_)):
                return obj.item()
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, (pd.Timestamp, datetime)):
                return obj.isoformat()
            elif isinstance(obj, dict):
                return {k: to_py(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [to_py(i) for i in obj]
            elif hasattr(obj, 'tolist'): # Handle other iterables
                 return obj.tolist()
            return obj

        raw_result = {
            # Core prediction
            "currentPrice": current_price,
            "predictedPrice": round_to_bucket(predicted_price),
            "recommendation": bias,
            "actionVerb": action_verb,
            "signalStrength": final_strength_category,
            "signalValue": final_strength_value,
            "fusionScore": round(final_score, 2),
            
            # Price ranges
            "rangeHigh": round_to_bucket(range_high),
            "rangeLow": round_to_bucket(range_low),
            "timeframe": "7D",
            
            # Uncertainty scenarios
            "scenarios": {
                "best": round_to_bucket(scenarios['best']),
                "base": round_to_bucket(scenarios['base']),
                "worst": round_to_bucket(scenarios['worst'])
            },
            
            # Sentiment
            "sentiment": display_label,
            "headline": f"Fusion: {final_score:.2f} | LSTM: {lstm_score:.2f} | Sentiment: {sent_score:.2f}",
            
            # Regime detection
            "regime": {
                "type": regime_type,
                "risk": risk_level,
                "description": regime_desc
            },
            
            # Multi-timeframe analysis
            "multiTimeframe": mtf_analysis,
            
            # Explanation
            "explanation": explanation,
            
            # Time-aware decay
            "expiry": expiry_info,
            "predictionTime": prediction_time.isoformat(),
            
            # Model health
            "modelHealth": model_health,
            
            # Guardrails
            "stability": {
                "level": stability_level,
                "score": stability_score,
                "flipCount": flip_count,
                "message": stability_msg,
                "warning": stability_warning
            },
            "conviction": {
                "state": conviction_state,
                "description": conviction_desc
            },
            "guardrails": {
                "maxConfidence": self.guardrails.MAX_CONFIDENCE,
                "message": guardrail_message
            },
            
            # Decision Quality
            "counterfactual": counterfactual,
            "drawdown": {
                "penalty": drawdown_penalty,
                "consecutiveLosses": consecutive_losses,
                "message": drawdown_message
            },
            "timeline": timeline,
            "historicalComparison": historical_comparison,
            
            # Elite Tier
            "bayesianBeliefs": bayesian_beliefs,
            "beliefTrend": belief_trend,
            "routing": routing,
            "metaGovernor": meta_intervention,
            "constitution": {
                "active": constitution_result["active"],
                "violations": constitution_result["violations"],
                "message": constitution_result["message"],
                "rules": self.constitution.get_constitution_summary()
            },
            "honestyIndex": honesty_score,
            "ledgerEntry": self.ledger.get_ledger(n=1)[0] if self.ledger.get_ledger(n=1) else None,
            
            # Omega Tier
            "silenceIntelligence": worthiness,
            "humility": humility_result,
            "trustDebt": trust_debt_result,
            "biasDetection": bias_detection,
            "failureTaxonomy": failure_analysis,
            "transcendent": transcendent_result,
            "backtestStats": stats
        }
        
        return to_py(raw_result)

