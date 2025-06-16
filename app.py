#Import Python libraries
# This script downloads a YouTube video and merges audio and video streams if necessary.
import os
import re
import urllib.parse
import requests
from time import sleep
from pytubefix import YouTube
from pytubefix.cli import on_progress
from moviepy.editor import VideoFileClip, AudioFileClip

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
            yt = YouTube(video_url, on_progress_callback=on_progress)
        except Exception as e:
            print("Failed to read URL. Retrying...")
            sleep(2)
            yt = YouTube(video_url, on_progress_callback=on_progress)
        raw_title = yt.title
        title = remove_non_alpha(raw_title)

        # Send a request to check availability
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

    audio_bitrate = '128kbps'
    # Build available resolution set from both progressive and adaptive streams.
    progressive_streams = yt.streams.filter(progressive=True)
    adaptive_streams = yt.streams.filter(adaptive=True)
    
    # Get resolutions from both kinds of streams (ignore very low resolution, e.g. 144p)
    resolutions = set()
    for stream in progressive_streams:
        if stream.resolution and stream.resolution != '144p':
            resolutions.add(stream.resolution)
    for stream in adaptive_streams:
        if stream.resolution and stream.resolution != '144p':
            resolutions.add(stream.resolution)
    
    # Sort resolutions numerically (assumes format like "360p", "720p", etc.)
    resolutions_list = sorted(resolutions, key=lambda x: int(x.rstrip('p')))
    # Append the audio-only option
    resolutions_list.append('audio')
    print(f"Available streams are: {resolutions_list}")
    download_quality = input("Enter download quality: ").strip()

    file_name = title
    output_dir = os.getcwd()

    # If the user wants audio only, do it directly.
    if download_quality == 'audio':
        audio_only = yt.streams.filter(abr=audio_bitrate).first()
        if audio_only is None:
            raise ValueError("No audio stream found.")
        print("Downloading audio-only file...")
        audio_only.download(output_path=output_dir, filename=f"{file_name}.m4a")

    else:
        # First try to get a progressive stream for the chosen resolution.
        stream_prog = yt.streams.filter(progressive=True, res=download_quality).first()
        if stream_prog:
            # If a progressive stream exists, download it directly.
            print(f"Downloading progressive video stream at {download_quality}...")
            stream_prog.download(output_path=output_dir, filename=f"{file_name}.mp4")
            print("Your video is ready!")
        else:
            # Otherwise, check if an adaptive (video-only) stream is available.
            stream_adapt = yt.streams.filter(adaptive=True, res=download_quality).first()
            if stream_adapt is None:
                raise ValueError(f"No stream found for resolution {download_quality}")
            # Adaptive streams are video-only; so download audio separately.
            print(f"Downloading adaptive video stream at {download_quality}...")
            video_file = os.path.join(output_dir, f"{file_name}.mp4")
            stream_adapt.download(output_path=output_dir, filename=f"{file_name}.mp4")
            print("Downloading audio stream...")
            audio_stream = yt.streams.filter(abr=audio_bitrate).first()
            if audio_stream is None:
                raise ValueError(f"No audio stream found for merging with {download_quality}")
            audio_file = os.path.join(output_dir, f"{file_name}.m4a")
            audio_stream.download(output_path=output_dir, filename=f"{file_name}.m4a")

            # Merge video and audio using moviepy
            print("Merging video and audio files...")
            try:
                # Load video and audio clips
                video_clip = VideoFileClip(video_file)
                audio_clip = AudioFileClip(audio_file)

                # Ensure the video and audio have the same duration
                if video_clip.duration != audio_clip.duration:
                    print("Warning: Video and audio durations do not match. Trimming to the shorter length.")
                    min_duration = min(video_clip.duration, audio_clip.duration)
                    video_clip = video_clip.subclip(0, min_duration)
                    audio_clip = audio_clip.subclip(0, min_duration)

                # Set the audio of the video clip
                final_clip = video_clip.set_audio(audio_clip)

                # Write the final video file with synchronized audio
                merged_file = os.path.join(output_dir, f"{title}_merged.mp4")
                final_clip.write_videofile(
                    merged_file,
                    codec='libx264',  # Video codec
                    audio_codec='aac',  # Audio codec
                    fps=video_clip.fps,  # Use the original video frame rate
                    threads=4  # Use multiple threads for faster processing
                )

                # Clean up temporary files
                video_clip.close()
                audio_clip.close()
                os.remove(video_file)
                os.remove(audio_file)

                print("Merging completed successfully.")
                print(f"Your video is ready: {merged_file}")
            except Exception as e:
                print(f"Error during merging: {str(e)}")
                raise

except Exception as e:
    print(f"An error occurred: {str(e)}")