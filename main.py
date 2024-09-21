import os
from pydub import AudioSegment
from openai import OpenAI
from dotenv import load_dotenv
import click
from rich.prompt import Prompt
from rich.console import Console

console = Console()

# Load the .env file
load_dotenv()

# API Parameters
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)
MAX_SIZE = 1024 * 1024 * 25

# Ensure the output directory exists
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def transcribe_audio(input_path: str, output_path: str):
    try:
        # Load the audio file
        audio_file = AudioSegment.from_file(input_path)
        file_size = os.path.getsize(input_path)
        if file_size <= MAX_SIZE:
            console.print(f"Transcribing {input_path}...", style="bold green")
            with open(input_path, "rb") as audio:
                transcription = client.audio.transcriptions.create(
                    model="whisper-1", file=audio
                )
            with open(output_path, "w") as file:
                file.write(transcription.text)
            console.print(f"Transcription saved to {output_path}", style="bold green")
        else:
            console.print(f"The given audio file {input_path} is too large. Splitting it into parts...", style="bold yellow")

            num_parts = file_size // MAX_SIZE + 1
            part_duration = len(audio_file) // num_parts
            transcriptions = []

            for i in range(num_parts):
                console.print(f"Transcribing part {i + 1}/{num_parts}...", style="bold green")
                start = i * part_duration
                end = min((i + 1) * part_duration, len(audio_file))

                # Get the audio part
                audio_part = audio_file[start:end]

                # Save the audio part to a file
                audio_part_path = f"{input_path}_part_{i}.mp3"
                audio_part.export(audio_part_path, format="mp3")

                # Transcribe the audio part
                with open(audio_part_path, "rb") as audio_part_file:
                    transcription = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_part_file,
                    )
                transcriptions.append(transcription.text)

                # Remove the audio part file
                os.remove(audio_part_path)

                # Save the combined transcription to the output directory
                full_transcription = "\n".join(transcriptions)
                with open(output_path, "w") as file:
                    file.write(full_transcription)
                console.print(f"Transcription saved to {output_path}", style="bold green")
    except Exception as e:
        console.print(f"Error: {e}", style="bold red")

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
