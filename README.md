# Youtube_Dowloader

This is a work in progress for a Youtube downloader, you have the options of downloading videos in 360p, 720p, 1080p, 1440p and 2160p
This code downloads a YouTube video and merges the audio and video files into a single file using moviepy.editor.
The user is asked to enter the URL of the YouTube video they want to download.
The code checks if the URL is valid and belongs to youtube.com.
If the URL is valid, the code gets a list of all available streams for the video.
The user is asked to select a download quality from the list of available streams.
If the user selects "audio", the code downloads the audio-only file.
If the user selects a video resolution, the code downloads the video file.
If the user selects a video resolution above 1080p, the code also downloads the audio-only file.
The code then merges the video WEBM file and MP4 audio files into a single file using moviepy.editor into a single MP4 format.
The final video file is saved to the current directory.

Note: The code provided is not currently working, as the video merging section is not working at 1080p and it appears that for the videos that are nativity 2160p the only options are 1080p and below.
