import io
import math
import os
from pydub import AudioSegment
from openai import OpenAI
from rich.console import Console
from utils.transcription_cost import calculate_transcription_cost

console = Console()

# API Parameters
MAX_SIZE = 1024 * 1024 * 25  # 25MB
MAX_DURATION_MS = 1300 * 1000  # 1300s (API limit is 1400s, using margin)


def get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key is None:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")
    return OpenAI(api_key=api_key)


def transcribe_audio(input_path: str, output_path: str) -> None:
    client = get_client()

    try:
        audio_file = AudioSegment.from_file(input_path)
        file_size = os.path.getsize(input_path)
        duration_ms = len(audio_file)
        transcription_cost = calculate_transcription_cost(duration_ms)

        input_file_name = os.path.basename(input_path)
        output_file_name = os.path.splitext(input_file_name)[0] + ".txt"

        if file_size <= MAX_SIZE and duration_ms <= MAX_DURATION_MS:
            console.print(
                f"Transcribing {input_file_name}...", style="bold green")
            with open(input_path, "rb") as audio:
                transcription = client.audio.transcriptions.create(
                    model="gpt-4o-transcribe", file=audio
                )
            with open(output_path, "w") as file:
                file.write(transcription.text)
            console.print(
                f"Transcription saved to output/{output_file_name}", style="bold green")
            console.print(
                f"Transcription cost: ${transcription_cost:.2f}", style="bold green")
        else:
            console.print(
                f"The given audio file {input_path} is too large. Splitting it into parts...", style="bold yellow")

            num_parts = max(
                math.ceil(file_size / MAX_SIZE),
                math.ceil(duration_ms / MAX_DURATION_MS),
            )
            part_duration = duration_ms / num_parts
            transcriptions = []

            for i in range(num_parts):
                console.print(
                    f"Transcribing part {i + 1}/{num_parts}...", style="bold green")
                start = int(i * part_duration)
                end = int(min((i + 1) * part_duration, duration_ms))

                audio_part = audio_file[start:end]

                buffer = io.BytesIO()
                audio_part.export(buffer, format="mp3")
                buffer.seek(0)
                buffer.name = f"part_{i + 1}.mp3"

                transcription = client.audio.transcriptions.create(
                    model="gpt-4o-transcribe",
                    file=buffer,
                )
                transcriptions.append(transcription.text)

            full_transcription = "\n".join(transcriptions)
            with open(output_path, "w") as file:
                file.write(full_transcription)
            console.print(
                f"Transcription saved to output/{output_file_name}", style="bold green")
            console.print(
                f"Transcription cost: ${transcription_cost:.2f}", style="bold green")

    except Exception as e:
        console.print(f"Error: {e}", style="bold red")
