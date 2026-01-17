import numpy as np
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import logging
import os

logger = logging.getLogger(__name__)

# === HYBRID IMPORT LOGIC ===
# Try to import PyTorch. If unavailable, switch to Lite Mode (No Neural Net).
try:
    if os.getenv("SENTINEL_MODE") == "LITE":
        raise ImportError("Forced Lite Mode")
    import torch
    import torch.nn as nn
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False
    logger.warning("⚠️ Torch not found. LSTM will run in Lite Mode (Moving Average heuristic).")

# ===========================
# 1. HEAVY MODE (PyTorch LSTM)
# ===========================
if HAS_TORCH:
    class StackedLSTM(nn.Module):
        def __init__(self, input_size=1, hidden_layer_size=50, output_size=1):
            super().__init__()
            self.lstm = nn.LSTM(input_size, hidden_layer_size, num_layers=2, batch_first=True, dropout=0.2)
            self.linear = nn.Linear(hidden_layer_size, output_size)
        
        def forward(self, input_seq):
            lstm_out, _ = self.lstm(input_seq)
            last_time_step = lstm_out[:, -1, :]
            predictions = self.linear(last_time_step)
            return predictions

# ===========================
# 2. UNIFIED PREDICTOR
# ===========================
class TrendPredictor:
    def __init__(self, window_size=60):
        self.window_size = window_size
        self.model = None
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.lite_mode = not HAS_TORCH # Auto-detect mode based on imports
        
    def prepare_data(self, df):
        if 'Close' not in df.columns:
            raise ValueError("Dataframe missing 'Close' column")
            
        data = df[['Close']].values.astype(float)
        scaled_data = self.scaler.fit_transform(data)
        
        X, y = [], []
        if len(scaled_data) > self.window_size:
            for i in range(self.window_size, len(scaled_data)):
                X.append(scaled_data[i-self.window_size:i])
                y.append(scaled_data[i])
            
        return np.array(X), np.array(y), scaled_data
        
    def train(self, df, epochs=20):
        """
        Train the model. In Lite Mode, this is a no-op or simple statistical fit.
        """
        if self.lite_mode:
            print("⚡ Lite Mode Active: Skipping LSTM training (using Moving Averages).")
            return 0.0 # No loss
            
        # --- HEAVY MODE TRAINING ---
        X, y, full_scaled = self.prepare_data(df)
        
        # Check sufficient data
        if len(X) < 1:
            print("Not enough data for LSTM training.")
            return 0.0

        X_tensor = torch.FloatTensor(X)
        y_tensor = torch.FloatTensor(y)
        
        self.model = StackedLSTM()
        loss_fn = nn.MSELoss()
        optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)
        
        print(f"Training Stacked LSTM for {epochs} epochs...")
        self.model.train()
        for i in range(epochs):
            optimizer.zero_grad()
            y_pred = self.model(X_tensor)
            loss = loss_fn(y_pred, y_tensor)
            loss.backward()
            optimizer.step()
            
        self.model.eval()
        return loss.item()
        
    def predict_next(self, df):
        """
        Predict next price. 
        Heavy Mode: Uses LSTM inference.
        Lite Mode: Uses Weighted Moving Average (WMA) + Momentum.
        """
        current_price = df['Close'].iloc[-1]

        # --- LITE MODE PREDICTION ---
        if self.lite_mode or self.model is None:
            # Simple algo: 7-day weighted average + recent momentum
            recent = df['Close'].tail(7)
            # Weights: [1, 2, 3, 4, 5, 6, 7]
            weights = np.arange(1, len(recent) + 1)
            wma = np.sum(recent * weights) / np.sum(weights)
            
            # Momentum trigger
            momentum = df['Close'].diff().tail(3).mean()
            
            pred_price = wma + momentum
            
            # Score logic
            change_pct = (pred_price - current_price) / current_price
            score = 0.5 + (change_pct * 10)
            score = max(0.0, min(1.0, score))
            
            print(f"⚡ Lite Prediction: ${pred_price:.2f} (WMA)")
            return pred_price, score

        # --- HEAVY MODE PREDICTION ---
        _, _, full_scaled = self.prepare_data(df)
        last_window = full_scaled[-self.window_size:]
        last_window_tensor = torch.FloatTensor([last_window]) 
        
        with torch.no_grad():
            pred_scaled = self.model(last_window_tensor).item()
            
        pred_price = self.scaler.inverse_transform([[pred_scaled]])[0][0]
        
        # Score logic
        change_pct = (pred_price - current_price) / current_price
        score = 0.5 + (change_pct * 10) 
        score = max(0.0, min(1.0, score))
        
        return pred_price, score
