import os
import click
from dotenv import load_dotenv
from rich.prompt import Prompt
from rich.console import Console

# Load the .env file
load_dotenv()

# Module imports
from transcriber.whisper import transcribe_audio
from utils.m4a_converter import m4a_to_mp3

console = Console()

# Ensure the output directory exists
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@click.command()
@click.argument("input_dir", type=click.Path(exists=True), default="input")
def main(input_dir):
    """Transcribes audio files (M4A or MP3) from the input directory."""
    console.print("Welcome to the Audio Transcription Tool!", style="bold blue")
    console.print(f"Searching for audio files in '{input_dir}'...", style="bold green")

    input_files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f)) and (f.endswith(".mp3") or f.endswith(".m4a"))]

    if not input_files:
        console.print("No audio files found in the input directory.", style="bold red")
        return

    # Lista para almacenar los archivos que se van a transcribir
    files_to_transcribe = []

    for input_file in input_files:
        input_path = os.path.join(input_dir, input_file)

        if input_file.endswith(".m4a"):
            converted_path = m4a_to_mp3(input_path)
            files_to_transcribe.append(converted_path)
        else:
            files_to_transcribe.append(input_path)

    # Transcribir todos los archivos (ya sean mp3 o convertidos)
    for audio_file in files_to_transcribe:
        output_path = os.path.join(OUTPUT_DIR, f"{os.path.splitext(os.path.basename(audio_file))[0]}.txt")
        transcribe_audio(audio_file, output_path)

    console.print("Transcription process completed.", style="bold blue")

if __name__ == "__main__":
    main()
