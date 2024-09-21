# Whisper Audio Transcription Script

This script takes audio files in either MP3 or M4A formats, transcribes the audio using OpenAI's Whisper model, and saves the transcription to a text file. If the audio file is too large, it automatically splits the audio into smaller parts, transcribes each part separately, and combines the transcriptions into a single output file.

## Prerequisites

1. Python 3.7 or higher
2. Pip package manager
3. [OpenAI](https://openai.com) API key
4. [FFmpeg](https://ffmpeg.org/download.html) installed (required for `pydub` to handle audio files)

## Setup

1. Clone the repository or download the project.
2. Install the required Python packages:

    ```sh
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the root directory of the project and add your OpenAI API key:

    ```env
    OPENAI_API_KEY=your_openai_api_key_here
    ```

4. Ensure you have a folder named `input` in the root directory of the project, and place the audio files you want to transcribe into this folder (both MP3 and M4A formats are supported).

## Usage

1. Run the script:

    ```sh
    python src/main.py
    ```

   Alternatively, if you want to specify a different input directory, you can provide it as an argument:

   ```sh
   python src/main.py input_directory
   ```

2. The script will process all audio files located in the specified `input` directory:
   - If the file size is less than or equal to 25MB, it transcribes the entire audio file.
   - If the file size is greater than 25MB, it splits the audio into smaller parts, transcribes each part, and combines the transcriptions.

3. The final transcriptions will be saved to the `output` directory as `filename.txt`, where `filename` is the name of the original audio file without its extension.

## Notes

- This script uses the `pydub` library to handle audio files, so make sure you have FFmpeg installed and accessible in your PATH.
- The maximum audio file size allowed by the script is 25MB. If an audio file exceeds this size, the script will automatically handle splitting the file into smaller parts and merging the transcriptions.
- Place your audio files (either MP3 or M4A) in the `input` directory, and the script will handle the rest.

```sh
input/
  ├── audio.mp3
  └── audio.m4a
output/
  ├── audio.txt
  └── audio_m4a.txt
src/
  └── main.py
.env
requirements.txt
```
