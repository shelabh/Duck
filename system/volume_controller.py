# system/volume_controller.py

import subprocess

def get_current_volume() -> int:
    """
    Returns the current macOS system volume (0–100)
    """
    output = subprocess.check_output([
        "osascript", "-e", "output volume of (get volume settings)"
    ])
    return int(output.strip())

def set_volume(level: int):
    """
    Sets macOS system volume (0–100)
    """
    subprocess.call([
        "osascript", "-e", f"set volume output volume {level}"
    ])
