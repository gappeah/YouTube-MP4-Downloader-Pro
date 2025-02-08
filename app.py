import os
from moviepy.editor import VideoFileClip, AudioFileClip
from pytubefix import YouTube
from pytubefix.cli import on_progress
import re
import urllib.parse
import requests
from time import sleep

# Function to remove non-alphabet characters from the title.
def remove_non_alpha(s):
    return re.sub(r"[^a-zA-Z\s]", '', s).replace(' ', '-')

try:
    video_url = input("Paste YouTube URL: ")
    result = urllib.parse.urlparse(video_url)

    # Check if the URL is valid and belongs to YouTube.com
    if (result.scheme == "https" and result.netloc == "www.youtube.com") or ("youtu.be" in video_url):
        print("URL check... PASS")
        try:
            # Create a YouTube object using pytubefix and a progress callback
            yt = YouTube(video_url, on_progress_callback=on_progress)
        except Exception as e:
            print("Failed to read url. Retrying...")
            sleep(2)
            yt = YouTube(video_url, on_progress_callback=on_progress)
        raw_title = yt.title
        title = remove_non_alpha(raw_title)

        # Check if the video is available
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

    # Audio bitrate for audio-only downloads and for merging above 1080p videos.
    audio_bitrate = '128kbps'

    # Get list of available progressive streams (for resolutions up to 720p) and check for higher-quality streams
    streams = list(yt.streams.filter(progressive=True).order_by('resolution').desc())
    hd_1 = yt.streams.filter(res='1080p').first()
    hd_2 = yt.streams.filter(res='1440p').first()
    hd_3 = yt.streams.filter(res='2160p').first()
    resolutions = set(
        stream.resolution
        for stream in streams + [hd_1, hd_2, hd_3]
        if stream and stream.resolution and stream.resolution != '144p'
    )
    resolutions_list = sorted(resolutions, key=lambda x: int(x[:-1]))
    resolutions_list.append('audio')
    download_quality = input(f"Enter download quality: Available streams are {resolutions_list}: ")
    file_name = title
    output_dir = os.getcwd()

    # Download and save audio-only file
    if download_quality == 'audio':
        audio_only = yt.streams.filter(abr=audio_bitrate).first()
        print("Downloading audio-only file...")
        audio_file = os.path.join(output_dir, f"{file_name}.m4a")
        audio_only.download(output_path=output_dir, filename=f"{file_name}.m4a")

    # Download video-only for lower resolutions (360p, 720p)
    elif download_quality in ['360p', '720p']:
        stream = yt.streams.filter(res=download_quality).first()
        print("Downloading video stream...")
        video_file = os.path.join(output_dir, f"{file_name}.mp4")
        stream.download(output_path=output_dir, filename=f"{file_name}.mp4")
        print("Your video is ready!")

    # For higher resolutions (1080p, 1440p, 2160p) download separate audio and video streams and merge them.
    elif download_quality in ['1080p', '1440p', '2160p']:
        stream = yt.streams.filter(res=download_quality).first()
        audio_stream = yt.streams.filter(abr=audio_bitrate).first()

        if not stream:
            raise ValueError(f"No video stream found for {download_quality}")
        if not audio_stream:
            raise ValueError(f"No audio stream found for {download_quality}")

        if stream and audio_stream:
            print("Downloading video stream...")
            video_file = os.path.join(output_dir, f"{file_name}.mp4")
            stream.download(output_path=output_dir, filename=f"{file_name}.mp4")
            print("Downloading audio stream...")
            audio_file = os.path.join(output_dir, f"{file_name}.m4a")
            audio_stream.download(output_path=output_dir, filename=f"{file_name}.m4a")

            # Merge video and audio using moviepy
            print("Merging video and audio files...")
            video_clip = VideoFileClip(video_file)
            audio_clip = AudioFileClip(audio_file)
            final_clip = video_clip.set_audio(audio_clip)
            output_path = f"{title}.mp4"
            final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')

            print("Merging completed")
            print("Your video is ready!")
        else:
            print(f"No suitable {download_quality} video or audio stream found.")
            raise ValueError(f"No suitable {download_quality} video or audio stream found")
except Exception as e:
    print(f"An error occurred: {str(e)}")
