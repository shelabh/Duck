import subprocess
import os
import wave
import time
WHISPER_PATH = "/Users/shelabhtyagi/Desktop/code/whisper.cpp/build/bin/whisper-cli"
MODEL_PATH = "/Users/shelabhtyagi/Desktop/code/whisper.cpp/models/ggml-base.en.bin"

def write_wav_file(filename, raw_audio, sample_rate=16000):
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit PCM
        wf.setframerate(sample_rate)
        wf.writeframes(raw_audio)

def transcribe_audio_chunk(raw_bytes: bytes, sample_rate=16000) -> str:
    timestamp = int(time.time())
    temp_wav_path = f"/Users/shelabhtyagi/Desktop/code/Duck/debug_chunks/chunk_{timestamp}.wav"
    write_wav_file(temp_wav_path, raw_bytes, sample_rate)
    print(f"🔊 Saved WAV: {temp_wav_path}")

    result = subprocess.run([
        WHISPER_PATH,
        "-m", MODEL_PATH,
        "-f", temp_wav_path,
        "-otxt",
        "-of", temp_wav_path.replace(".wav", "")
    ], capture_output=True)

    txt_path = temp_wav_path.replace(".wav", ".txt")
    print(f"📄 Transcript TXT: {txt_path}")

    if os.path.exists(txt_path):
        with open(txt_path, "r") as f:
            return f.read().strip()
    return ""
