# main.py

from logic.ducking_controller import DuckingController

if __name__ == "__main__":
    controller = DuckingController(
        vad_aggressiveness=3,
        silence_timeout=1.5,  # seconds of silence before restoring volume
        ducked_volume=30      # volume level during speech
    )
    controller.run()
