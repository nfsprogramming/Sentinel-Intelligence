export const MOCK_TRANSCENDENT_DATA = {
    ticker: "BTC-USD",
    name: "Bitcoin",
    currentPrice: 94520.50,
    predictedPrice: 91200.00,
    recommendation: "Bearish Bias",
    actionVerb: "Leaning Bearish",
    signalStrength: "Medium",
    signalValue: 0.25,
    fusionScore: 0.2,
    rangeHigh: 98400,
    rangeLow: 88200,
    timeframe: "7D",
    scenarios: {
        best: 102000,
        base: 91200,
        worst: 85000
    },
    regime: {
        type: "Ranging",
        risk: "Low",
        description: "Sideways consolidation - mean reversion likely"
    },
    multiTimeframe: {
        "1H": "Neutral",
        "4H": "Bearish",
        "1D": "Bearish",
        consensus: "Strong Bearish",
        agreement: 66
    },
    explanation: {
        summary: "Bearish Bias due to ↓ downward trend and price momentum (bearish). Volatility: Low.",
        trend: "↓ Downward",
        volatility: "Low",
        dominantFactor: "Price momentum (bearish)"
    },
    expiry: {
        remainingHours: 6.0,
        isExpired: false,
        decayFactor: 1.0
    },
    modelHealth: {
        status: "Nominal",
        message: "System operating within normal parameters",
        errorTrend: "Stable",
    },
    stability: {
        level: "High",
        score: 0.85,
        flipCount: 1,
        message: "Signal consistency is robust",
        warning: null
    },
    conviction: {
        state: "Cautious",
        description: "🤔 Mixed signals with bearish tilt"
    },
    guardrails: {
        maxConfidence: 0.7,
        message: null
    },
    counterfactual: {
        ai: 12.4,
        hold: -5.2,
        cash: 0.0,
        message: "AI outperforms buy & hold by 17.6%"
    },
    bayesianBeliefs: {
        beliefs: {
            "Bullish": 15.2,
            "Neutral": 65.4,
            "Bearish": 19.4
        },
        uncertainty: 0.35,
        message: "Strong Neutral/Bearish belief structure"
    },
    routing: {
        activeModel: "Mean Reversion Model",
        weights: {
            "Trend Model": 20,
            "Mean Reversion Model": 60,
            "Volatility Breakout Model": 20
        }
    },
    metaGovernor: {
        active: false,
        message: "Supervisor: All systems nominal"
    },
    constitution: {
        active: false,
        message: "✓ Risk Constitution: All rules satisfied"
    },
    honestyIndex: {
        available: true,
        score: 98,
        grade: "A+",
        components: {
            accuracy: 97,
            coherence: 99,
            stability: 98
        },
        message: "High fidelity self-reporting"
    },
    silenceIntelligence: {
        worthy: true,
        score: 0.78,
        threshold: 0.4,
        reason: "Signal meets worthiness threshold"
    },
    humility: {
        enforcementNeeded: false,
        message: "Confidence calibrated correctly"
    },
    trustDebt: {
        severity: "None",
        message: "Trust ledger positive"
    },
    biasDetection: {
        detected: false,
        biases: [],
        message: "✓ No cognitive biases detected"
    },
    transcendent: {
        epistemic: {
            boundariesDetected: false,
            unknownUnknownsRisk: "Moderate",
            dataBlindness: ["None detected"],
            message: "Within Epistemic Limits"
        },
        research: {
            activeQuestion: "Is liquidity behavior currently abnormal for a ranging market?",
            researchPhase: "Active Investigation"
        },
        hypothesis: {
            status: "Stable",
            evidenceScore: 7.2,
            refutationRisk: "Low"
        },
        narrative: {
            content: "BTC-USD exhibits Bearish Bias characteristics with a 76.4% projected structural shift. Price action suggests fragility during low liquidity periods.",
            evolution: "Developing"
        },
        moral: {
            moralRestraint: "Inactive",
            message: "Responsibility Layer Cleared"
        },
        observer: {
            crowdingRisk: "Low",
            reflexivityIndex: 0.53,
            marketImpactEstimate: "Minimal"
        },
        budget: {
            remaining: 2,
            totalBudget: 3,
            message: "2 insights remaining today"
        },
        crossDomain: {
            domainAlignment: "Divergent",
            coherenceScore: 42
        },
        legacy: {
            historicalParallel: "2022",
            lessonsLearned: "Avoid chasing low volatility without volume confirmation."
        }
    }
};
