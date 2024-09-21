from moviepy.editor import VideoFileClip

try:
    video = VideoFileClip("video.mp4")

    # Check if the video contains an audio track
    if video.audio:
        video.audio.write_audiofile("audio.mp3")
        print("Audio extraction complete.")
    else:
        print("No audio track found in the video.")

except Exception as e:
    print(f"An error occurred: {e}")
