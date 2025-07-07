# logic/ducking_controller.py

import time
from audio.mic_stream import get_audio_frames
from audio.vad import VoiceActivityDetector
from system.volume_controller import get_current_volume, set_volume

class DuckingController:
    def __init__(self,
                 vad_aggressiveness=2,
                 silence_timeout=1.5,
                 ducked_volume=10):
        self.vad = VoiceActivityDetector(vad_aggressiveness)
        self.ducked_volume = ducked_volume
        self.original_volume = get_current_volume()
        self.last_speaking_time = 0
        self.is_ducked = False
        self.silence_timeout = silence_timeout

    def run(self):
        print("🎧 Ducking controller started. Speak to test...")

        for frame in get_audio_frames():
            speaking = self.vad.is_speech(frame)

            current_time = time.time()

            if speaking:
                self.last_speaking_time = current_time
                if not self.is_ducked:
                    print("🎤 Speech detected → lowering volume")
                    self.original_volume = get_current_volume()
                    set_volume(self.ducked_volume)
                    self.is_ducked = True

            elif self.is_ducked and (current_time - self.last_speaking_time > self.silence_timeout):
                print("🔇 Silence → restoring volume")
                set_volume(self.original_volume)
                self.is_ducked = False
