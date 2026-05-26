from transcriber.whisper import transcribe_audio
from utils.m4a_converter import m4a_to_mp3
from utils.mp4_converter import mp4_to_mp3
import os
import sys
import click
from dotenv import load_dotenv
from rich.prompt import Prompt
from rich.console import Console

console = Console()


def is_frozen():
    """Check if the script is frozen with pyinstaller"""
    return getattr(sys, 'frozen', False)


def resource_path(relative_path):
    """Get the absolute path to a resource file"""
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)


if is_frozen():
    # If the script is frozen with pyinstaller, load the .env file from the resources folder
    dotenv_path = resource_path(".env.prod")
    load_dotenv(dotenv_path=dotenv_path)
else:
    # Otherwise, load the .env file from the current directory
    dotenv_path = '.env.dev'
    load_dotenv(dotenv_path=dotenv_path)

# Module imports


def get_input_directory():
    """Get the correct path for the input directory based on the running context."""
    if is_frozen():
        # When frozen, the input directory is relative to the executable
        # Get the directory of the executable
        base_path = os.path.dirname(sys.executable)
    else:
        # When not frozen, the input directory is relative to the current script
        base_path = os.path.abspath(".")  # Current working directory

    return os.path.join(base_path, "input")


def get_output_directory():
    """Get the correct path for the output directory based on the running context."""
    if is_frozen():
        # When frozen, the output directory is relative to the executable
        # Get the directory of the executable
        base_path = os.path.dirname(sys.executable)
    else:
        # When not frozen, the output directory is relative to the current script
        base_path = os.path.abspath(".")  # Current working directory

    return os.path.join(base_path, "output")


# Ensure the output directory exists
OUTPUT_DIR = get_output_directory()
os.makedirs(OUTPUT_DIR, exist_ok=True)


@click.command()
@click.argument("input_dir", type=click.Path(exists=True), default=get_input_directory())
def main(input_dir):
    """Transcribes audio files (M4A or MP3) from the input directory."""
    console.print("Welcome to the Audio Transcription Tool!",
                  style="bold blue")
    console.print(
        "Searching for audio files in input directory...", style="bold green")

    input_files = [f for f in os.listdir(input_dir) if os.path.isfile(
        os.path.join(input_dir, f)) and (f.endswith(".mp3") or f.endswith(".m4a")) or f.endswith(".mp4")]

    if not input_files:
        console.print(
            "No audio files found in the input directory.", style="bold red")
        return

    converted_paths = set()
    files_to_transcribe = []

    for input_file in input_files:
        input_path = os.path.join(input_dir, input_file)

        if input_file.endswith(".m4a"):
            converted_path = m4a_to_mp3(input_path)
            converted_paths.add(converted_path)
            files_to_transcribe.append(converted_path)
        elif input_file.endswith(".mp4"):
            converted_path = mp4_to_mp3(input_path)
            converted_paths.add(converted_path)
            files_to_transcribe.append(converted_path)

    for input_file in input_files:
        input_path = os.path.join(input_dir, input_file)
        if input_file.endswith(".mp3") and input_path not in converted_paths:
            files_to_transcribe.append(input_path)

    # Transcribir todos los archivos (ya sean mp3 o convertidos)
    for audio_file in files_to_transcribe:
        output_path = os.path.join(
            OUTPUT_DIR, f"{os.path.splitext(os.path.basename(audio_file))[0]}.txt")
        transcribe_audio(audio_file, output_path)

    console.print("Transcription process completed.", style="bold blue")


if __name__ == "__main__":
    main()
