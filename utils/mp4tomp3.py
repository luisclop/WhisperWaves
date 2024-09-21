from moviepy.editor import VideoFileClip

video = VideoFileClip("video.mp4")
video.audio.write_audiofile("audio.mp3")
