
## Youtube Downloader Pro

**A Python script to download YouTube videos and audio with optional merging**

### Overview

This script utilizes the PyTube and moviepy libraries to effortlessly download YouTube videos and audio files. It provides options to choose the desired download quality, including audio-only, 360p, 720p, 1080p, 1440p, and 2160p. For higher-resolution videos, it automatically merges the video and audio streams using moviepy to create a complete video file.

### Requirements

1. Python 3.x
2. PyTube library: `pip install pytube`
3. moviepy library: `pip install moviepy`

### Usage

1. Download the `youtube_downloader.py` file to your local machine.
2. Open the terminal or command prompt and navigate to the directory containing the `youtube_downloader.py` file.
3. Run the script by entering the following command:
```
python youtube_downloader.py
```
4. Enter the YouTube video URL when prompted.
5. Choose the desired download quality from the available options:
    - `audio`: Download only the audio track.
    - `360p`, `720p`, `1080p`, `1440p`, `2160p`: Download the video with the specified resolution.
6. The downloaded file will be saved in the current working directory with the specified filename (default: `protocolten-<title>`). For audio-only downloads, the file extension will be `.m4a`. For videos, the file extension will be `.mp4`.

### Examples

**Download audio-only:**

Enter the YouTube URL and select `audio` as the download quality. The audio file will be saved with the filename `protocolten-<title>.m4a`.

**Download 1080p video:**

Enter the YouTube URL and select `1080p` as the download quality. The complete video file will be saved with the filename `protocolten-<title>.mp4`.

### Additional Notes

1. The script performs basic checks to ensure the provided URL is valid and belongs to YouTube.
2. The audio bitrate for `audio_only` and merging video/audio above 1080p is set to 128kbps.
3. The script handles downloading and merging video/audio files successively, ensuring that the video file is created only after the audio and video streams are successfully downloaded.

