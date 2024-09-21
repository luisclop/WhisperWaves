import os
from pydub import AudioSegment
from rich.console import Console

console = Console()

def m4a_to_mp3(input_path: str) -> str:
    """
    Convert an M4A file to MP3 format.

    Args:
        input_path (str): Path to the input M4A file.

    Returns:
        str: Path to the output MP3 file.
    """
    if not input_path.lower().endswith(".m4a"):
            raise ValueError("El archivo debe ser de tipo M4A.")

    console.print(f"Convirtiendo {os.path.basename(input_path)} a MP3...", style="bold yellow")
    audio = AudioSegment.from_file(input_path, format="m4a")

    mp3_path = f"{os.path.splitext(input_path)[0]}.mp3"
    audio.export(mp3_path, format="mp3")

    console.print(f"Convertido y guardado como {os.path.basename(mp3_path)}.", style="bold green")
    return mp3_path
