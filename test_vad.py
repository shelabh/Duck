# test_vad.py

from audio.mic_stream import get_audio_frames
from audio.vad import VoiceActivityDetector

vad = VoiceActivityDetector()

for frame in get_audio_frames():
    speaking = vad.is_speech(frame)
    print("🎤 Speaking" if speaking else "🔇 Silence")
