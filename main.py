import pyperclip
from pynput import keyboard as pynput_keyboard
import time
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import os
import pygame

# Load environment variables from .env file
load_dotenv()

client = OpenAI()


# Global state to track playback
class PlaybackState:
    def __init__(self):
        self.is_paused = False
        self.pygame_initialized = False


playback_state = PlaybackState()


def initialize_pygame():
    """
    Initialize pygame and its mixer.
    """
    try:
        if not playback_state.pygame_initialized:
            pygame.init()
            pygame.mixer.init()
            playback_state.pygame_initialized = True
        return True
    except pygame.error as e:
        print(f"Error initializing pygame: {e}")
        return False


def toggle_playback():
    """
    Toggle between pause and play states.
    """
    if not playback_state.pygame_initialized:
        print("Pygame not initialized. Cannot control playback.")
        return

    try:
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            playback_state.is_paused = True
            print("Playback paused")
        elif playback_state.is_paused:  # Was paused, now resuming
            pygame.mixer.music.unpause()
            playback_state.is_paused = False
            print("Playback resumed")
    except pygame.error as e:
        print(f"Error toggling playback: {e}")


def play_speech():
    """
    Function to play the speech.mp3 file.
    """
    if not pygame.mixer.get_init():
        print("Pygame mixer is not initialized. Attempting to initialize...")
        if not initialize_pygame():
            print("Failed to initialize pygame. Cannot play audio.")
            return

    try:
        pygame.mixer.music.load("speech.mp3")
        pygame.mixer.music.play()
        playback_state.is_paused = False

    except pygame.error as e:
        print(f"Error playing speech.mp3: {e}")
    except FileNotFoundError:
        print(
            "speech.mp3 file not found. Make sure it exists in the same directory as this script."
        )


def text_to_speech(text):
    speech_file_path = Path(__file__).parent / "speech.mp3"
    response = client.audio.speech.create(
        model="tts-1", voice="alloy", input=text, speed=1.0
    )
    response.stream_to_file(speech_file_path)
    print(f"Speech file created at: {speech_file_path}")
    time.sleep(0.5)
    play_speech()


def on_hotkey():
    # Get the currently highlighted text
    highlighted_text = pyperclip.paste()
    print(f"Highlighted text: '{highlighted_text}'")

    if highlighted_text:
        print("Text highlighted. Converting to speech...")
        text_to_speech(highlighted_text)
    else:
        print("No text highlighted.")


# Define the hotkeys
CONVERT_HOTKEY = frozenset([pynput_keyboard.Key.f8])
PLAYBACK_HOTKEY = frozenset([pynput_keyboard.Key.f9])  # Separate hotkey for pause/play
current_keys = set()


def on_press(key):
    if key == pynput_keyboard.Key.esc:
        print("Escape key pressed. Stopping the listener.")
        return False  # Stop the listener
    current_keys.add(key)
    if all(k in current_keys for k in CONVERT_HOTKEY):
        print("Convert hotkey activated.")
        on_hotkey()
    elif all(k in current_keys for k in PLAYBACK_HOTKEY):
        print("Playback control hotkey activated.")
        toggle_playback()


def on_release(key):
    try:
        current_keys.remove(key)
    except KeyError:
        pass


def update():
    """
    Update function to keep pygame running
    """
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        pygame.time.Clock().tick(10)


if __name__ == "__main__":
    # Initialize pygame at startup
    initialize_pygame()

    # Start the keyboard listener
    with pynput_keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        print("Keyboard listener started. Instructions:")
        print("1. Copy text and press F8 to convert to speech and play immediately")
        print("2. Press F9 to pause/resume current playback")
        print("3. Press Esc to exit")
        listener.join()

    print("Application stopped.")
    pygame.quit()
