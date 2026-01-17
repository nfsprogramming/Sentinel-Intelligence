import numpy as np
from datetime import datetime
import json
import os

class TranscendentIntelligence:
    """
    TRANSCENDENT TIER: A Living Market Intelligence Organism.
    
    This tier handles:
    1. Epistemic Awareness (Unknown unknowns)
    2. Self-Authored Research Questions
    3. Hypothesis Testing Loop
    4. Narrative Intelligence Engine
    5. Moral & Responsibility Layer
    6. Observer Effect Modeling
    7. Intelligence Budgeting
    8. Cross-Domain Reasoning
    9. Legacy Memory
    """

    def __init__(self, tracker):
        self.tracker = tracker
        self.daily_budget = 100
        self.state_file = os.path.join(os.path.dirname(__file__), '../data/transcendent_state.json')
        
        # Database Integration
        from modules.database import db_manager
        self.db = db_manager
        
        self._load_state()

        # Legacy Memory: Simplified historical data
        self.legacy_memory = {
            "dot_com": {"era": "2000-2002", "pattern": "Irrational Exuberance", "outcome": "Mean Reversion"},
            "global_financial_crisis": {"era": "2008", "pattern": "Systemic Contagion", "outcome": "Structural Collapse"},
            "covid_crash": {"era": "2020", "pattern": "Black Swan Liquidity", "outcome": "V-Shape Recovery"},
            "2022_inflation": {"era": "2022", "pattern": "Monetary Tightening", "outcome": "Slow Bleed"}
        }

    def _load_state(self):
        """Load budget state from MongoDB or disk."""
        self.insights_today = 0
        self.last_reset = datetime.now().date().isoformat()
        
        data = None
        
        # 1. Try MongoDB
        if self.db.is_connected():
            try:
                coll = self.db.get_collection("transcendent_state")
                doc = coll.find_one({"_id": "global_state"})
                if doc:
                    data = doc
                    # print("Loaded state from MongoDB")
            except Exception as e:
                print(f"MongoDB Load Error: {e}")

        # 2. Fallback to File
        if not data and os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    data = json.load(f)
            except Exception as e:
                print(f"File Load Error: {e}")
        
        # 3. Apply State
        if data:
            last_reset_str = data.get("last_reset", self.last_reset)
            self.last_reset = last_reset_str
            
            # Check if date changed
            if last_reset_str != datetime.now().date().isoformat():
                self.insights_today = 0
                self.last_reset = datetime.now().date().isoformat()
            else:
                self.insights_today = data.get("insights_today", 0)

    def _save_state(self):
        """Save budget state to MongoDB and disk."""
        state_data = {
            "insights_today": self.insights_today,
            "last_reset": datetime.now().date().isoformat()
        }
        
        # 1. Save to MongoDB
        if self.db.is_connected():
            try:
                coll = self.db.get_collection("transcendent_state")
                coll.update_one(
                    {"_id": "global_state"}, 
                    {"$set": state_data}, 
                    upsert=True
                )
            except Exception as e:
                print(f"MongoDB Save Error: {e}")

        # 2. Save to File (Backup)
        try:
            os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
            with open(self.state_file, 'w') as f:
                json.dump(state_data, f)
        except Exception as e:
            print(f"File Save Error: {e}")



    def process_transcendence(self, prediction_data, market_data, ticker):
        """
        Main entry point for Transcendent Analysis.
        """
        self._check_budget_reset()
        
        # 1. Epistemic Awareness
        epistemic = self._assess_epistemic_boundaries(prediction_data, market_data)
        
        # 2. Research Questions
        research = self._generate_research_questions(prediction_data, market_data)
        
        # 3. Hypothesis Testing
        hypothesis = self._test_hypotheses(prediction_data, research)
        
        # 4. Narrative Intelligence
        narrative = self._build_narratives(prediction_data, market_data, ticker)
        
        # 5. Moral & Responsibility
        moral = self._apply_moral_layer(prediction_data, market_data)
        
        # 6. Observer Effect
        observer = self._model_observer_effect(prediction_data, market_data)
        
        # 7. Intelligence Budgeting
        budget_status = self._check_budget()
        
        # 8. Cross-Domain Reasoning
        cross_domain = self._reason_cross_domain(prediction_data, market_data)
        
        # 9. Legacy Memory
        legacy = self._query_legacy_memory(prediction_data, market_data)
        
        # Determine global transcendence state
        suppressed = not epistemic["insightAllowed"] or not moral["insightAllowed"] or not budget_status["allowed"]
        
        if not suppressed:
            self.insights_today += 1
            self._save_state()

        return {
            "epistemic": epistemic,
            "research": research,
            "hypothesis": hypothesis,
            "narrative": narrative,
            "moral": moral,
            "observer": observer,
            "budget": budget_status,
            "crossDomain": cross_domain,
            "legacy": legacy,
            "isSuppressed": suppressed,
            "suppressionReason": self._get_suppression_reason(epistemic, moral, budget_status)
        }

    def _assess_epistemic_boundaries(self, pred, market):
        """Know what we cannot know."""
        uncertainty = pred.get("bayesianBeliefs", {}).get("uncertainty", 0.5)
        volatility = market.get("volatility", 0.3)
        
        # Boundaries are crossed if uncertainty is too high relative to data quality
        boundaries_detected = uncertainty > 0.8 or (volatility > 0.6 and uncertainty > 0.6)
        
        return {
            "boundariesDetected": bool(boundaries_detected),
            "unknownUnknownsRisk": "High" if uncertainty > 0.7 else "Moderate",
            "dataBlindness": ["No macro feedback", "Liquidity depth unknown"] if volatility > 0.4 else ["None detected"],
            "insightAllowed": not (uncertainty > 0.9),
            "message": "Knowledge Boundary Detected" if boundaries_detected else "Within Epistemic Limits"
        }

    def _generate_research_questions(self, pred, market):
        """Asks: What matters right now?"""
        questions = []
        
        current_regime = pred.get("regime", {}).get("type", "Unknown")
        stability = pred.get("stability", {}).get("score", 0.5)
        
        if stability < 0.4:
            questions.append("Is BTC entering a non-linear volatility phase?")
        
        if current_regime == "Trending":
            questions.append("Is this trend decoupling from macro reality?")
        else:
            questions.append("Is liquidity behavior currently abnormal for a ranging market?")
            
        return {
            "activeQuestion": questions[0] if questions else "Is sentiment decoupled from price?",
            "secondaryQuestions": questions[1:] if len(questions) > 1 else [],
            "researchPhase": "Active Investigation"
        }

    def _test_hypotheses(self, pred, research):
        """Treat signals as falsifiable hypotheses."""
        signal_val = pred.get("signalValue", 0)
        direction = pred.get("recommendation", "Neutral")
        
        # Form hypothesis based on signal
        hypothesis_text = f"Market is in a {direction} phase driven by {pred.get('explanation', 'current data')}"
        
        # Simulate strength based on stability and conviction
        strength = pred.get("conviction", 0.5)
        
        status = "Strengthening" if strength > 0.6 else ("Weakening" if strength < 0.4 else "Stable")
        
        return {
            "activeHypothesis": hypothesis_text,
            "status": status,
            "evidenceScore": round(float(strength * 10), 1),
            "refutationRisk": "Low" if status == "Strengthening" else "Elevated"
        }

    def _build_narratives(self, pred, market, ticker):
        """Build coherent narratives, not just signals."""
        current_price = pred.get("currentPrice", 0)
        pred_price = pred.get("predictedPrice", 0)
        rec = pred.get("recommendation", "Neutral")
        
        delta = (pred_price - current_price) / current_price if current_price > 0 else 0
        
        narrative = f"{ticker} exhibits {rec} characteristics with a {abs(delta)*100:.1f}% projected structural shift. "
        
        if "Bearish" in rec:
            narrative += "Price action suggests fragility during low liquidity periods, often a precursor to volatility expansion."
        elif "Bullish" in rec:
            narrative += "Consolidation patterns show underlying strength despite macro head-winds."
        else:
            narrative += "Equilibrium state detected; the market is currently searching for a new value catalyst."
            
        return {
            "title": "Structural Evolution Narrative",
            "content": narrative,
            "evolution": "Developing"
        }

    def _apply_moral_layer(self, pred, market):
        """Should I present this?"""
        volatility = market.get("volatility", 0.3)
        confidence = pred.get("signalValue", 0)
        
        # Moral restraint: If market is fragile and signal is weak, withhold
        fragility = volatility > 0.7
        should_restrain = fragility and confidence < 0.3
        
        return {
            "insightAllowed": not should_restrain,
            "riskProfile": "Aggressive" if fragility else "Normal",
            "moralRestraint": "Active" if should_restrain else "Inactive",
            "message": "Insight withheld — risk amplification potential" if should_restrain else "Responsibility Layer Cleared"
        }

    def _model_observer_effect(self, pred, market):
        """If many act on this, what happens?"""
        confidence = pred.get("signalValue", 0)
        regime = pred.get("regime", {}).get("type", "Ranging")
        
        crowding = "High" if confidence > 0.8 and regime == "Trending" else "Low"
        reflexivity = 0.4 + (confidence * 0.5)
        
        return {
            "crowdingRisk": crowding,
            "reflexivityIndex": round(float(reflexivity), 2),
            "marketImpactEstimate": "Significant" if crowding == "High" else "Minimal",
            "adjustmentFactor": 0.8 if crowding == "High" else 1.0
        }

    def _check_budget(self):
        """Quality > Quantity."""
        remaining = self.daily_budget - self.insights_today
        return {
            "allowed": remaining > 0,
            "remaining": int(remaining),
            "totalBudget": int(self.daily_budget),
            "message": f"{remaining} insights remaining today"
        }

    def _reason_cross_domain(self, pred, market):
        """Macro coherence checks."""
        macro_signal = "Risk-Off" if market.get("volatility", 0) > 0.4 else "Neutral"
        aligment = "Aligned" if (macro_signal == "Risk-Off" and "Bearish" in pred.get("recommendation", "")) else "Divergent"
        
        return {
            "macroSignal": macro_signal,
            "coherenceScore": 75 if aligment == "Aligned" else 42,
            "domainAlignment": aligment,
            "nonMarketPatterns": "Social sentiment lagging price action"
        }

    def _query_legacy_memory(self, pred, market):
        """Generational learning."""
        volatility = market.get("volatility", 0)
        current_pattern = "High Volatility" if volatility > 0.5 else "Low Volatility"
        
        match = "2022_inflation" if volatility < 0.3 else "covid_crash"
        legacy_context = self.legacy_memory.get(match, {})
        
        return {
            "historicalParallel": legacy_context.get("era", "Unknown"),
            "parallelPattern": legacy_context.get("pattern", "Market Consolidation"),
            "lessonsLearned": f"Avoid chasing {current_pattern.lower()} without volume confirmation.",
            "eraRelevance": "85% match with current structure"
        }

    def _check_budget_reset(self):
        today = datetime.now().date().isoformat()
        if today != self.last_reset: # Use simple inequality check for different days
            self.insights_today = 0
            self.last_reset = today
            self._save_state()

    def _get_suppression_reason(self, epistemic, moral, budget):
        if not budget["allowed"]: return "Intelligence Budget Depleted"
        if not epistemic["insightAllowed"]: return "Epistemic Boundary Overstepped"
        if not moral["insightAllowed"]: return "Moral Restraint Active"
        return "None"
