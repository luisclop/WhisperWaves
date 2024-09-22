RATE_PER_MINUTE = 0.006

def calculate_transcription_cost(audio_duration: int) -> float:
    """
    Calculate the cost of a transcription based on the duration of the audio.

    Args:
        audio_duration (float): Duration of the audio in seconds.

    Returns:
        float: The cost of the transcription in USD.
    """
    duration_minutes = audio_duration / (1000 * 60)
    return duration_minutes * RATE_PER_MINUTE
