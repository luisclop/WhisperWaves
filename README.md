# Whisper Audio Transcription Script

This script takes an audio file in MP3 format, transcribes the audio using OpenAI's Whisper model, and saves the transcription to a text file. If the audio file is too large, it automatically splits the audio into smaller parts, transcribes each part separately, and combines the transcriptions into a single output file.

## Prerequisites

1. Python 3.7 or higher
2. Pip package manager
3. [OpenAI](https://openai.com) API key
4. [FFmpeg](https://ffmpeg.org/download.html) installed (required for `pydub` to handle MP3 files)

## Setup

1. Clone the repository or download the `main.py` script.
2. Install the required Python packages:

    ```sh
    pip install pydub openai python-dotenv
    ```

3. Create a `.env` file in the root directory of the project and add your OpenAI API key:

    ```env
    OPENAI_API_KEY=your_openai_api_key_here
    ```

4. Ensure you have a folder named `input` in the root directory of the project, and place the `audio.mp3` file you want to transcribe into this folder.

## Usage

1. Run the script:

    ```sh
    python main.py
    ```

2. The script will process the `audio.mp3` file located in the `input` directory:
   - If the file size is less than or equal to 25MB, it transcribes the entire audio file.
   - If the file size is greater than 25MB, it splits the audio into smaller parts, transcribes each part, and combines the transcriptions.

3. The final transcription will be saved to the `output` directory as `transcription.txt`.

## Notes

- This script uses the `pydub` library to handle audio files, so make sure you have FFmpeg installed and accessible in your PATH.
- The maximum audio file size allowed by the script is 25MB. If an audio file exceeds this size, the script will automatically handle splitting the file into smaller parts and merging the transcriptions.
- Ensure your MP3 file is named `audio.mp3` and placed in the `input` directory, or adjust the script accordingly to handle different file paths/names.

```sh
input/
  └── audio.mp3
output/
  └── transcription.txt
main.py
.env
```
