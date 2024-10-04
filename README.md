# Audify
*A text-to-speech application for improved reading comprehension.*

This Python application allows you to convert highlighted text to speech using OpenAI's Text-to-Speech API. It works by capturing the text held most recently in the Clipboard when a specific hotkey is pressed, converting it to speech, and then playing the audio.

## Motivation
You might think this is not for you, but this tool seeks to benefit everyone. It is **easier to comprehend written information with combined audiorty and visual input**. This means we comprehend written information better, when we read and listen to it at the same time. I.e. listening to the audiobook and following along with the physical book at the same time. 

Where did I get this idea? I am dyslexic and when I was diagnosed at the ripe old age of 18, it was suggested that exactly this method would help me and it did. However, as a user, I feel I'm getting a subpar experience. 

- Despite major AI advancements, OS system Text-to-Speech accessibility tool are still **robotic** sounding. This makes it **less easy to process** than more natural-sounding AI -generated speech.
- The right click interface kind of sucks. It **doesn't work on all applications**.

So, I created this terminal application to play any text that I highlighted, so I can have any text on my laptop read back to me. 🍰

### A note on NotebookLM. 
The above reasons lend themselves to why NotebookLM podcasts are so great - making written information available to other parts of the brain and diversifying the formats of information makes it easier to comprehend. As a dyslexic, the whole NotebookLM tool has made it considerably easier for me to comprehend written information and goes to show that designing for accessibility sets to benefit us all.

Given that I work in AI, I depend on keeping up with scientific papers and innovations. Tools like these have made my life a lot easier.

## Features

- Capture copied text from any application 
- Convert text to speech using OpenAI's TTS-1 model
- Play generated speech through your computer's audio output
- Easy-to-use hotkey activation (Command + Shift + E on macOS)

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6 or higher installed on your system
- An OpenAI API key (you can get one from [OpenAI's website](https://openai.com/))

## Installation

1. Clone this repository or download the script.

2. Install the required Python packages:

   ```
   pip install pyperclip pynput pygame openai python-dotenv
   ```

3. Create a `.env` file in the same directory as the script and add your OpenAI API key:

   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

1. Run the script:

   ```
   python main.py
   ```

2. The application will start and wait for the hotkey to be pressed.

3. In any application, highlight and copy the text you want to convert to speech (Cmd+C on MacOS).

4. Press Command + Shift + E (on macOS) to activate the text-to-speech conversion.

5. The highlighted text will be captured, converted to speech, and played through your computer's audio output.

6. To exit the application, press the Esc key.

## Customization

- To change the hotkey, modify the `HOTKEY` variable in the script.
- To use a different voice, change the `voice` parameter in the `text_to_speech` function. Available options are "alloy", "echo", "fable", "onyx", "nova", and "shimmer".

## Troubleshooting

- If you encounter issues with audio playback, ensure that pygame is properly initialized and that your system's audio is working correctly.
- If the text capture isn't working, make sure the script has the necessary permissions to simulate key presses and access the clipboard.

## Contributing

Contributions to this project are welcome. Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgements

- This project uses OpenAI's API for text-to-speech conversion.
- The audio playback is handled using the pygame library.