# audio/vad.py

import webrtcvad

class VoiceActivityDetector:
    def __init__(self, aggressiveness: int = 2):
        """
        aggressiveness: 0-3 (0 = least aggressive, 3 = most aggressive about filtering out non-speech)
        """
        self.vad = webrtcvad.Vad(aggressiveness)

    def is_speech(self, frame_bytes: bytes, sample_rate: int = 16000) -> bool:
        """
        Returns True if speech is detected in the given frame
        """
        return self.vad.is_speech(frame_bytes, sample_rate)
