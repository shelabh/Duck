# # audio/mic_stream.py

# import sounddevice as sd
# import numpy as np

# SAMPLE_RATE = 16000        # 16kHz is required for webrtcvad
# FRAME_DURATION = 20        # in milliseconds
# FRAME_SIZE = int(SAMPLE_RATE * FRAME_DURATION / 1000)  # 320 samples for 20ms
# CHANNELS = 1               # Mono audio

# def get_audio_frames():
#     """
#     Generator that yields 20ms chunks of raw PCM audio from mic as bytes
#     """
#     with sd.InputStream(
#         samplerate=SAMPLE_RATE,
#         channels=CHANNELS,
#         dtype='int16',
#         blocksize=FRAME_SIZE,
#         latency='low'
#     ) as stream:
#         while True:
#             audio_chunk, _ = stream.read(FRAME_SIZE)  # shape: (320, 1)
#             audio_chunk = audio_chunk.flatten()
#             yield audio_chunk.tobytes()
# audio/mic_stream.py

import sounddevice as sd
import numpy as np

SAMPLE_RATE = 16000
CHANNELS = 1
SAMPLE_WIDTH = 2  # bytes (16-bit)
DTYPE = 'int16'

def get_audio_chunks(duration_sec=2.0):
    """
    Generator that yields `duration_sec` long raw PCM audio chunks as bytes
    """
    frame_count = int(SAMPLE_RATE * duration_sec)

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype=DTYPE,
        blocksize=frame_count,
        latency='low'
    ) as stream:
        while True:
            audio_data, _ = stream.read(frame_count)
            audio_data = audio_data.flatten()
            yield audio_data.tobytes()
