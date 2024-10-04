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


def initialize_pygame():
    """
    Initialize pygame and its mixer.
    """
    try:
        pygame.init()
        pygame.mixer.init()
        return True
    except pygame.error as e:
        print(f"Error initializing pygame: {e}")
        return False


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
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except pygame.error as e:
        print(f"Error playing speech.mp3: {e}")
    except FileNotFoundError:
        print(
            "speech.mp3 file not found. Make sure it exists in the same directory as this script."
        )

    pygame.quit()


def text_to_speech(text):
    speech_file_path = Path(__file__).parent / "speech.mp3"
    response = client.audio.speech.create(model="tts-1", voice="alloy", input=text)
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


# Define the hotkey for Mac (Command + Shift + E)
HOTKEY = frozenset(
    [
        pynput_keyboard.Key.cmd,
        pynput_keyboard.Key.shift,
        pynput_keyboard.KeyCode.from_char("e"),
    ]
)
current_keys = set()


def on_press(key):
    if key == pynput_keyboard.Key.esc:
        print("Escape key pressed. Stopping the listener.")
        return False  # Stop the listener

    current_keys.add(key)
    if all(k in current_keys for k in HOTKEY):
        print("Hotkey activated.")
        on_hotkey()


def on_release(key):
    try:
        current_keys.remove(key)
    except KeyError:
        pass


# Start the keyboard listener
with pynput_keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    print(
        "Keyboard listener started. Copy the text, then press Cmd+Shift+E to activate, or Esc to exit."
    )
    listener.join()

print("Application stopped.")
pygame.quit()
