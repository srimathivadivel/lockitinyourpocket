import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import os

class ParkinsonsSpeechModel:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.model_path = "models"
        self.feature_names = [
            'mfcc_mean', 'mfcc_std', 'mfcc_skew',
            'rms_mean', 'rms_std', 'rms_skew',
            'zcr_mean', 'zcr_std', 'zcr_skew',
            'centroid_mean', 'centroid_std', 'centroid_skew',
            'rolloff_mean', 'rolloff_std', 'rolloff_skew',
            'chroma_mean', 'chroma_std', 'chroma_skew'
        ]
        os.makedirs(self.model_path, exist_ok=True)
        
    def generate_synthetic_data(self, n_samples=1000):
        """
        Generate synthetic data for training.
        In a real application, this would be replaced with real patient data.
        """
        np.random.seed(42)
        
        # Generate synthetic features
        X = np.random.randn(n_samples, len(self.feature_names))
        
        # Generate synthetic labels (0: healthy, 1: Parkinson's)
        # Add some patterns that might be indicative of Parkinson's
        y = np.zeros(n_samples)
        
        # Higher tremor (ZCR) and irregular energy (RMS) patterns indicate Parkinson's
        parkinsons_mask = (
            (X[:, self.feature_names.index('zcr_std')] > 1.0) & 
            (X[:, self.feature_names.index('rms_std')] > 1.0)
        )
        y[parkinsons_mask] = 1
        
        return X, y
        
    def train_model(self, X=None, y=None):
        """Train the model using either provided data or synthetic data."""
        if X is None or y is None:
            print("Using synthetic data for training...")
            X, y = self.generate_synthetic_data()
            
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42
        )
        
        # Train model
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.model.fit(X_train, y_train)
        
        # Save model and scaler
        joblib.dump(self.model, os.path.join(self.model_path, 'parkinsons_model.joblib'))
        joblib.dump(self.scaler, os.path.join(self.model_path, 'scaler.joblib'))
        
        # Evaluate model
        train_score = self.model.score(X_train, y_train)
        test_score = self.model.score(X_test, y_test)
        
        print(f"Model Training Score: {train_score:.3f}")
        print(f"Model Test Score: {test_score:.3f}")
        
    def load_model(self):
        """Load the trained model and scaler."""
        model_file = os.path.join(self.model_path, 'parkinsons_model.joblib')
        scaler_file = os.path.join(self.model_path, 'scaler.joblib')
        
        if os.path.exists(model_file) and os.path.exists(scaler_file):
            self.model = joblib.load(model_file)
            self.scaler = joblib.load(scaler_file)
            return True
        return False
        
    def predict(self, features):
        """Make predictions using the trained model."""
        if self.model is None:
            if not self.load_model():
                self.train_model()
                
        # Scale features
        features_scaled = self.scaler.transform(features.reshape(1, -1))
        
        # Get prediction and probability
        prediction = self.model.predict(features_scaled)[0]
        probability = self.model.predict_proba(features_scaled)[0]
        
        return {
            'prediction': int(prediction),
            'confidence': float(probability[1]),  # Probability of Parkinson's
            'feature_importances': dict(zip(
                self.feature_names,
                self.model.feature_importances_
            ))
        }
