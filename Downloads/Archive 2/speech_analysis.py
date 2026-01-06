import librosa
import numpy as np
from sklearn.preprocessing import StandardScaler
import pandas as pd
import soundfile as sf
from scipy.stats import skew
from ml_model import ParkinsonsSpeechModel

class SpeechAnalyzer:
    def __init__(self):
        self.features = None
        self.ml_model = ParkinsonsSpeechModel()
        # Initialize the model with synthetic data
        if self.ml_model.model is None:
            self.ml_model.train_model()
        
    def extract_features(self, audio_path):
        """Extract relevant features from the audio file."""
        try:
            # Load the audio file using soundfile
            y, sr = sf.read(audio_path)
            
            # Convert to mono if stereo
            if len(y.shape) > 1:
                y = np.mean(y, axis=1)
            
            # Extract features
            features_list = []
            
            # 1. MFCC features
            mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            mfcc_mean = np.mean(mfccs)
            mfcc_std = np.std(mfccs)
            mfcc_skew = skew(mfccs.ravel())
            features_list.extend([mfcc_mean, mfcc_std, mfcc_skew])
            
            # 2. Root Mean Square Energy
            rms = librosa.feature.rms(y=y)[0]
            rms_mean = np.mean(rms)
            rms_std = np.std(rms)
            rms_skew = skew(rms)
            features_list.extend([rms_mean, rms_std, rms_skew])
            
            # 3. Zero Crossing Rate
            zcr = librosa.feature.zero_crossing_rate(y)[0]
            zcr_mean = np.mean(zcr)
            zcr_std = np.std(zcr)
            zcr_skew = skew(zcr)
            features_list.extend([zcr_mean, zcr_std, zcr_skew])
            
            # 4. Spectral Centroid
            centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
            centroid_mean = np.mean(centroid)
            centroid_std = np.std(centroid)
            centroid_skew = skew(centroid)
            features_list.extend([centroid_mean, centroid_std, centroid_skew])
            
            # 5. Spectral Rolloff
            rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
            rolloff_mean = np.mean(rolloff)
            rolloff_std = np.std(rolloff)
            rolloff_skew = skew(rolloff)
            features_list.extend([rolloff_mean, rolloff_std, rolloff_skew])
            
            # 6. Chroma Features
            chroma = librosa.feature.chroma_stft(y=y, sr=sr)
            chroma_mean = np.mean(chroma)
            chroma_std = np.std(chroma)
            chroma_skew = skew(chroma.ravel())
            features_list.extend([chroma_mean, chroma_std, chroma_skew])
            
            # Store all features
            self.features = np.array(features_list)
            
            return self.features
            
        except Exception as e:
            print(f"Error extracting features: {str(e)}")
            return None
    
    def analyze_parkinsons_indicators(self):
        """Analyze the extracted features for Parkinson's indicators using ML model."""
        if self.features is None or len(self.features) == 0:
            raise ValueError("No features extracted. Run extract_features first.")
        
        # Get prediction from ML model
        result = self.ml_model.predict(self.features)
        
        # Calculate risk score based on model confidence
        risk_score = result['confidence']
        
        # Get top contributing features
        feature_importance = result['feature_importances']
        top_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # Prepare analysis results
        analysis = {
            'risk_score': risk_score,
            'prediction': result['prediction'],
            'risk_factors': {
                'high_tremor': risk_score > 0.6,
                'irregular_speech': risk_score > 0.5,
                'voice_instability': risk_score > 0.7
            },
            'top_features': top_features
        }
        
        return analysis
    
    def get_progress_data(self):
        """Get progress data for visualization."""
        # In a real application, this would fetch historical data
        # For now, return example data
        return {
            'dates': ['2025-01-22', '2025-01-23', '2025-01-24', '2025-01-25', 
                     '2025-01-26', '2025-01-27', '2025-01-28'],
            'scores': [85, 82, 88, 84, 86, 83, 87],
            'observations': [
                "Speech clarity has improved over the past week",
                "Voice tremor remains stable",
                "Good breath control during speech"
            ]
        }
