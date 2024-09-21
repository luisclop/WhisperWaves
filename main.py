from pydub import AudioSegment
from openai import OpenAI
from dotenv import load_dotenv
import os

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

# Load the audio file
AUDIO_FILE_PATH = "input/audio.mp3"
audio_file = AudioSegment.from_file(AUDIO_FILE_PATH)

# Get the file size
file_size = os.path.getsize(AUDIO_FILE_PATH)

if file_size <= MAX_SIZE:
    try:
        print("Transcribing audio...")
        with open(AUDIO_FILE_PATH, "rb") as audio:
            transcription = client.audio.transcriptions.create(
                model="whisper-1", file=audio
            )

        # Save the transcription to the output directory
        transcription_file_path = os.path.join(OUTPUT_DIR, "transcription.txt")
        with open(transcription_file_path, "w") as file:
            file.write(transcription.text)

        print("Transcription saved to transcription.txt")
    except Exception as e:
        print(e)

else:
    print(f"The given audio file is too large. The maximum size allowed is {
          MAX_SIZE/(1024*1024)}MB. Splitting the audio file into parts...")

    # Calculate the number of parts
    num_parts = file_size // MAX_SIZE + 1

    # Split the audio file
    part_duration = len(audio_file) // num_parts

    transcriptions = []

    print("Transcribing parts...")
    try:
        for i in range(num_parts):
            print(f"Part {i+1}/{num_parts}")
            # Calculate the start and end of the audio part
            start = i * part_duration
            end = min((i + 1) * part_duration, len(audio_file))

            # Get the audio part
            audio_part = audio_file[start:end]

            # Save the audio part to a file
            audio_part_path = f"audio_part_{i}.mp3"
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

        # Combine the transcriptions
        full_transcription = "\n".join(transcriptions)

        # Save the combined transcription to the output directory
        transcription_file_path = os.path.join(OUTPUT_DIR, "transcription.txt")
        with open(transcription_file_path, "w") as file:
            file.write(full_transcription)

        print("Transcription saved to transcription.txt")

    except Exception as e:
        print(e)
