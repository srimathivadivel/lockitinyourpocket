# Module for voice recording functionality

import sounddevice as sd
import numpy as np
import wave
from datetime import datetime
import os

class VoiceRecorder:
    def __init__(self, sample_rate=44100, channels=1):
        self.sample_rate = sample_rate
        self.channels = channels
        self.recording = None
        
    def record_voice(self, duration=10):
        """Record audio for a specified duration in seconds."""
        print("Recording started...")
        self.recording = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype=np.int16
        )
        sd.wait()
        print("Recording finished.")
        return self.recording
    
    def save_recording(self, filename=None):
        """Save the recording to a WAV file."""
        if self.recording is None:
            raise ValueError("No recording available to save.")
            
        if filename is None:
            # Generate filename based on current timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"recording_{timestamp}.wav"
            
        # Create recordings directory if it doesn't exist
        os.makedirs("recordings", exist_ok=True)
        filepath = os.path.join("recordings", filename)
            
        with wave.open(filepath, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(2)  # 2 bytes for int16
            wf.setframerate(self.sample_rate)
            wf.writeframes(self.recording.tobytes())
            
        print(f"Recording saved to: {filepath}")
        return filepath
