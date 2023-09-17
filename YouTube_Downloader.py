import os
from moviepy.editor import *
from pytube import YouTube
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import re
import yaml
import subprocess
import urllib.parse
import requests
from time import sleep
from pathlib import Path
import argparse

# Function to remove non-alphabet characters from the title.
def remove_non_alpha(s):
    return re.sub(r'[^a-zA-Z\s]', '', s).replace(' ', '-')

# Validating input url
try:
    video_url = input("Paste YouTube URL: ")
    result = urllib.parse.urlparse(video_url)

    # Check if the URL is valid and belongs to youtube.com
    if result.scheme == "https" and result.netloc == "www.youtube.com":
        print("URL check... PASS")
        try:
            yt = YouTube(video_url)
        except:
            print("Failed to read url. Retrying...")
            sleep(2)
            yt = YouTube(video_url)
        raw_title = yt.title
        title = remove_non_alpha(raw_title)

        # Send a request to the URL and check if the video is available
        response = requests.get(video_url)
        if "Video unavailable" in response.text:
            print("Video is not available on YouTube")
            raise ValueError("Video is not available on YouTube")
        else:
            print(f"Title: {title}")
            print("Gathering available streams...")
            sleep(2)

    else:
        print("URL is not valid or does not belong to youtube.com")
        raise ValueError("Invalid URL or URL does not belong to youtube.com")

    # Audio bitrate for 'audio_only' and merging video/audio above 1080p. Bitrate 160kbps can also be used for 2K and 4K videos.
    audio_bitrate = '128kbps'

    # Getting list of all available streams except 144p for input url.
    streams = list(yt.streams.filter(progressive=True).order_by('resolution').desc())
    hd_1 = yt.streams.filter(res='1080p').first()
    hd_2 = yt.streams.filter(res='1440p').first()
    hd_3 = yt.streams.filter(res='2160p').first()
    resolutions = set(stream.resolution for stream in streams + [hd_1, hd_2, hd_3] if
                    stream and stream.resolution and stream.resolution != '144p')
    resolutions_list = sorted(resolutions, key=lambda x: int(x[:-1]))
    resolutions_list.append('audio')
    download_quality = input(f"Enter download quality: Available streams are {resolutions_list}: ")
    file_name = f"protocolten-{title}"
    #output_path = os.path.join(output_dir, file_name)

    # This condition only handles downloading and uploading of audio-only file
    if download_quality == 'audio':
        audio_only = yt.streams.filter(abr=audio_bitrate).first()
        print("Downloading audio-only file...")
        audio_only.download() #(output_path=output_dir, filename=f"{file_name}.m4a")

    # This condition only handles downloading and uploading of 360p/720p videos
    elif download_quality in ['360p', '720p']:
        stream = yt.streams.filter(res=download_quality).first()
        print("Downloading video stream...")
        video_file = stream.download() #(output_path=output_dir, filename=f"{file_name}.mp4")

    # Getting input stream and downloading it into a specific directory
    elif download_quality in ['1080p', '1440p', '2160p']:
        stream = yt.streams.filter(res=download_quality).first()
        audio_stream = yt.streams.filter(abr=audio_bitrate).first()

        # Checking if audio and video streams are present for input link
        if not stream:
            raise ValueError(f"No video stream found for {download_quality}")
        if not audio_stream:
            raise ValueError(f"No audio stream found for {download_quality}")

        # Downloading audio and video files
        print("Downloading video stream...")
        video_file = stream.download() #(output_path=output_dir, filename="video.mp4")
        print("Downloading audio stream...")
        audio_file = audio_stream.download() #(output_path=output_dir, filename="audio.mp4")

        # Combining the audio and video file using ffmpeg tool.
        # ... (previous code)

        # Combining the audio and video file using moviepy.editor
        print("Merging video and audio files...")
        video_clip = VideoFileClip(video_file)
        audio_clip = AudioFileClip(audio_file)
        video_clip = video_clip.set_audio(audio_clip)
        output_path = f"{title}.mp4"
        video_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')
        print("Merging completed")

        # ... (rest of your code)

# This section is off, the code is not working the video merging is not working,
# #the output(s) is WEBM which contains visual data. The audio is an MP4 file
# I need to fix this, merge the audio and video files into a single file


except Exception as e:
    print(f"An error occurred: {str(e)}")



from moviepy.editor import VideoFileClip, AudioFileClip

# Load the video file
video_clip = VideoFileClip('video.mp4')

# Load the audio file
audio_clip = AudioFileClip('audio.mp4')

# Set the audio of the video to the loaded audio
video_clip = video_clip.set_audio(audio_clip)

# Write the final video file
video_clip.write_videofile('final_video.mp4', codec='libx264', audio_codec='aac')
