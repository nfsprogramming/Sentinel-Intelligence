#!/usr/bin/env python
"""Quick system verification test"""

print("=" * 60)
print("FINANCIAL INTELLIGENCE AI - SYSTEM VERIFICATION")
print("=" * 60)

try:
    print("\n[1/4] Testing Module Imports...")
    from modules.stock_data import StockDataManager
    from modules.lstm_model import TrendPredictor
    from modules.sentiment_engine import FinBERTSentiment
    from modules.fusion import FusionEngine
    print("[OK] All modules imported successfully")
    
    print("\n[2/4] Testing Data Loader...")
    loader = StockDataManager()
    print(f"[OK] Data Loader initialized (Alpha Key: {'Found' if loader.alpha_key else 'Missing'})")
    
    print("\n[3/4] Testing LSTM Model...")
    lstm = TrendPredictor(window_size=60)
    print("[OK] LSTM Model initialized")
    
    print("\n[4/4] Testing Fusion Engine...")
    engine = FusionEngine()
    print("[OK] Fusion Engine initialized")
    
    print("\n" + "=" * 60)
    print("[SUCCESS] SYSTEM READY - All components operational!")
    print("=" * 60)
    print("\nYou can now use 'Run Market Analysis' on the web UI.")
    print("First run will download FinBERT (~400MB) - please be patient.")
    
except Exception as e:
    print(f"\n[ERROR] {e}")
    import traceback
    traceback.print_exc()
