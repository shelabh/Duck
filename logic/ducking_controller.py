# # logic/ducking_controller.py

# import time
# from audio.mic_stream import get_audio_frames
# from audio.vad import VoiceActivityDetector
# from system.volume_controller import get_current_volume, set_volume

# class DuckingController:
#     def __init__(self,
#                  vad_aggressiveness=2,
#                  silence_timeout=1.5,
#                  ducked_volume=10):
#         self.vad = VoiceActivityDetector(vad_aggressiveness)
#         self.ducked_volume = ducked_volume
#         self.original_volume = get_current_volume()
#         self.last_speaking_time = 0
#         self.is_ducked = False
#         self.silence_timeout = silence_timeout

#     def run(self):
#         print("🎧 Ducking controller started. Speak to test...")

#         for frame in get_audio_frames():
#             speaking = self.vad.is_speech(frame)

#             current_time = time.time()

#             if speaking:
#                 self.last_speaking_time = current_time
#                 if not self.is_ducked:
#                     print("🎤 Speech detected → lowering volume")
#                     self.original_volume = get_current_volume()
#                     set_volume(self.ducked_volume)
#                     self.is_ducked = True

#             elif self.is_ducked and (current_time - self.last_speaking_time > self.silence_timeout):
#                 print("🔇 Silence → restoring volume")
#                 set_volume(self.original_volume)
#                 self.is_ducked = False
# logic/ducking_controller.py

import time
from audio.mic_stream import get_audio_chunks
from models.whisper_wrapper import transcribe_audio_chunk
from system.volume_controller import get_current_volume, set_volume

class DuckingController:
    def __init__(self,
                 silence_timeout=2.0,
                 ducked_volume=10,
                 min_words=3):
        self.ducked_volume = ducked_volume
        self.original_volume = get_current_volume()
        self.last_speaking_time = 0
        self.is_ducked = False
        self.silence_timeout = silence_timeout
        self.min_words = min_words

    def is_real_speech(self, text: str) -> bool:
        # Filter short or unclear audio
        return len(text.split()) >= self.min_words

    def run(self):
        print("🎧 Whisper-based ducking controller running...")

        for chunk in get_audio_chunks(duration_sec=2.0):
            transcript = transcribe_audio_chunk(chunk)

            print(f"[Transcript]: {transcript}")

            current_time = time.time()
            if self.is_real_speech(transcript):
                self.last_speaking_time = current_time
                if not self.is_ducked:
                    print("🎤 Detected real speech → ducking volume")
                    self.original_volume = get_current_volume()
                    set_volume(self.ducked_volume)
                    self.is_ducked = True

            elif self.is_ducked and (current_time - self.last_speaking_time > self.silence_timeout):
                print("🔇 Silence for a while → restoring volume")
                set_volume(self.original_volume)
                self.is_ducked = False
