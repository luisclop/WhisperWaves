import os
from pydub import AudioSegment
from rich.console import Console

console = Console()


def mp4_to_mp3(input_path: str) -> str:
    """
    Convert an MP4 file to MP3 format by extracting the audio.

    Args:
        input_path (str): Path to the input MP4 file.

    Returns:
        str: Path to the output MP3 file.
    """
    if not input_path.lower().endswith(".mp4"):
        raise ValueError("El archivo debe ser de tipo MP4.")

    console.print(f"Extrayendo audio de {os.path.basename(
        input_path)} y convirtiéndolo a MP3...", style="bold yellow")
    audio = AudioSegment.from_file(input_path, format="mp4")

    mp3_path = f"{os.path.splitext(input_path)[0]}.mp3"
    audio.export(mp3_path, format="mp3")

    console.print(f"Audio extraído y guardado como {
                  os.path.basename(mp3_path)}.", style="bold green")
    return mp3_path
