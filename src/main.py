import os
import click
from dotenv import load_dotenv
from rich.prompt import Prompt
from rich.console import Console

# Load the .env file
load_dotenv()

# Module imports
from transcriber.whisper import transcribe_audio

console = Console()

# Ensure the output directory exists
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@click.command()
@click.argument("input_dir", type=click.Path(exists=True), default="input")
def main(input_dir):
    console.print("Starting transcription process...", style="bold blue")

    input_files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f)) and f.endswith(".mp3")]

    if not input_files:
        console.print("No audio files found in the input directory.", style="bold red")
        return

    for input_file in input_files:
        input_path = os.path.join(input_dir, input_file)
        output_path = os.path.join(OUTPUT_DIR, f"{os.path.splitext(input_file)[0]}.txt")
        transcribe_audio(input_path, output_path)

    console.print("Transcription process completed.", style="bold blue")

if __name__ == "__main__":
    main()
