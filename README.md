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

3. Create a `.env.dev` file for the development environment and a `.env.prod` file for the production environment in the root directory of the project, and add your OpenAI API key:

    ```env
    OPENAI_API_KEY=your_openai_api_key_here
    ```

4. Ensure you have a folder named `input` in the root directory of the project, and place the audio files you want to transcribe into this folder (both MP3 and M4A formats are supported).

## Usage

### Development Mode

1. Run the script:

    ```sh
    python src/main.py
    ```

   Alternatively, if you want to specify a different input directory, you can provide it as an argument:

   ```sh
   python src/main.py input_directory
   ```

### Production Mode

For production, make sure to use the `.env.prod` file that includes your OpenAI API key, and run the script as a standalone executable after packaging it with PyInstaller.

1. **Package the application** using PyInstaller. Use the `.spec` file to specify the dependencies and the project structure:

    ```sh
    pyinstaller WhisperWaves.spec
    ```

2. After packaging, navigate to the `dist` directory where the executable is created.

    ```sh
    ./dist/WhisperWaves
    ```

3. **Input Preparation**: Once the project is compiled, you no longer need to run any script. Just create the `input` folder and place the audio files you want to transcribe. The executable will automatically process all audio files and save the transcriptions in the `output` directory.

4. The final transcriptions will be saved to the `output` directory as `filename.txt`, where `filename` is the name of the original audio file without its extension.

## Notes

- This script uses the `pydub` library to handle audio files, so make sure you have FFmpeg installed and accessible in your PATH.
- The maximum audio file size allowed by the script is 25MB. If an audio file exceeds this size, the script will automatically handle splitting the file into smaller parts and merging the transcriptions.
- Place your audio files (either MP3 or M4A) in the `input` directory, and the program will handle the rest.

```sh
input/
  ├── audio.mp3
  └── audio.m4a
output/
  ├── audio.txt
  └── audio_m4a.txt
src/
  └── main.py
.env.dev
.env.prod
WhisperWaves.spec
requirements.txt
```
