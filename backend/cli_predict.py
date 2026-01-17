import sys
import json
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Force UTF-8 for Windows consoles
if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

def main():
    if len(sys.argv) < 3:
        # Default/Test values
        ticker = "BTC-USD"
        name = "Bitcoin"
    else:
        ticker = sys.argv[1]
        name = sys.argv[2]


    # --- NEW ARCHITECTURE: FUSION ENGINE ---
    try:
        from modules.fusion import FusionEngine
        engine = FusionEngine()
        result = engine.run_analysis(ticker)
        
        if result:
            output = {
                "ticker": ticker,
                "name": name,
                "currentPrice": float(result['currentPrice']),
                "predictedPrice": float(result['predictedPrice']),
                "recommendation": result['recommendation'],
                "actionVerb": result['actionVerb'],
                "signalStrength": result['signalStrength'],
                "signalValue": result['signalValue'],
                "fusionScore": result['fusionScore'],
                "rangeHigh": result['rangeHigh'],
                "rangeLow": result['rangeLow'],
                "timeframe": result['timeframe'],
                "scenarios": result['scenarios'],
                "regime": result['regime'],
                "multiTimeframe": result['multiTimeframe'],
                "explanation": result['explanation'],
                "expiry": result['expiry'],
                "predictionTime": result['predictionTime'],
                "modelHealth": result['modelHealth'],
                "stability": result['stability'],
                "conviction": result['conviction'],
                "guardrails": result['guardrails'],
                "counterfactual": result['counterfactual'],
                "drawdown": result['drawdown'],
                "timeline": result['timeline'],
                "historicalComparison": result['historicalComparison'],
                "bayesianBeliefs": result['bayesianBeliefs'],
                "beliefTrend": result['beliefTrend'],
                "routing": result['routing'],
                "metaGovernor": result['metaGovernor'],
                "constitution": result['constitution'],
                "honestyIndex": result['honestyIndex'],
                "ledgerEntry": result['ledgerEntry'],
                "silenceIntelligence": result['silenceIntelligence'],
                "humility": result['humility'],
                "trustDebt": result['trustDebt'],
                "biasDetection": result['biasDetection'],
                "failureTaxonomy": result['failureTaxonomy'],
                "transcendent": result['transcendent'],
                "geminiReport": "", 
                "alphaVantage": {
                    "sentiment": result['sentiment'],
                    "headline": result['headline']
                },
                "backtestStats": result.get('backtestStats', {
                    "totalPredictions": 0,
                    "winRate": 0,
                    "avgError": 0
                })
            }
        else:
            output = {"error": "Fusion Analysis failed (insufficient data?)"}

        # separator to ensure we only parse the json
        print("__JSON_START__")
        print(json.dumps(output))
        print("__JSON_END__")

    except Exception as e:
        import traceback
        traceback.print_exc()
        print("__JSON_START__")
        print(json.dumps({"error": f"Fusion Engine Error: {str(e)}"}))
        print("__JSON_END__")

if __name__ == "__main__":
    main()
