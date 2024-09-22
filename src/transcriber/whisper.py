import os
import tempfile
from pydub import AudioSegment
from openai import OpenAI
from rich.console import Console

console = Console()

# API Parameters
MAX_SIZE = 1024 * 1024 * 25

def get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key is None:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")
    return OpenAI(api_key=api_key)

def transcribe_audio(input_path: str, output_path: str) -> None:
    client = get_client()

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

            num_parts = (file_size // MAX_SIZE) + 1
            part_duration = len(audio_file) / num_parts
            transcriptions = []

            for i in range(num_parts):
                console.print(f"Transcribing part {i + 1}/{num_parts}...", style="bold green")
                start = int(i * part_duration)
                end = int(min((i + 1) * part_duration, len(audio_file)))

                # Get the audio part
                audio_part = audio_file[start:end]

                # Use a temporary file
                with tempfile.NamedTemporaryFile(suffix=".mp3", delete=True) as temp_audio_file:
                    audio_part.export(temp_audio_file.name, format="mp3")
                    temp_audio_file.seek(0)

                    # Transcribe the audio part
                    transcription = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=temp_audio_file,
                    )
                    transcriptions.append(transcription.text)

            # Save the combined transcription to the output directory
            full_transcription = "\n".join(transcriptions)
            with open(output_path, "w") as file:
                file.write(full_transcription)
            console.print(f"Transcription saved to {output_path}", style="bold green")

    except Exception as e:
        console.print(f"Error: {e}", style="bold red")
