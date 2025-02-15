Below is a `README.md` file for your YouTube to MP4 downloader script. This file provides an overview of the project, installation instructions, usage guidelines, and other relevant details.

---

# YouTube to MP4 Downloader

A Python script to download YouTube videos as MP4 files. The script supports downloading videos in various resolutions and can also extract audio-only files. It uses `pytubefix` for downloading and `moviepy` for merging video and audio streams.

---

## Features

- Download YouTube videos in multiple resolutions.
- Extract audio-only files in `.m4a` format.
- Merge video and audio streams for adaptive streams (where video and audio are separate).
- Clean up temporary files after merging.
- Simple command-line interface.

---

## Prerequisites

Before running the script, ensure you have the following installed:

1. **Python 3.6 or higher**.
2. Required Python libraries:
   - `pytubefix`
   - `moviepy`
   - `requests`

---

## Installation

1. **Clone the repository** (if applicable):
   ```bash
   git clone https://github.com/gappeah/YouTube-MP4-Downloader-Pro.git
   cd YouTube-MP4-Downloader-Pro
   ```

2. **Install the required libraries**:
   ```bash
   pip install pytubefix moviepy requests
   ```

3. **Ensure FFmpeg is installed** (required by `moviepy`):
   - Download and install FFmpeg from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html).
   - Add FFmpeg to your system's PATH.

---

## Usage

1. **Run the script**:
   ```bash
   python youtube_to_mp4.py
   ```

2. **Paste the YouTube URL**:
   - When prompted, paste the URL of the YouTube video you want to download.

3. **Select download quality**:
   - The script will display available resolutions (e.g., `360p`, `720p`, `1080p`).
   - Enter the desired resolution or type `audio` to download only the audio.

4. **Wait for the download to complete**:
   - The script will download the video and audio (if necessary) and merge them into a single `.mp4` file.
   - The final file will be saved in the current working directory.

---

## Example

```bash
$ python youtube_to_mp4.py
Paste YouTube URL: https://www.youtube.com/watch?v=example
URL check... PASS
Title: Example-Video-Title
Gathering available streams...
Available streams are: ['360p', '720p', '1080p', 'audio']
Enter download quality: 720p
Downloading adaptive video stream at 720p...
Downloading audio stream...
Merging video and audio files...
Merging completed successfully.
Your video is ready: Example-Video-Title_merged.mp4
```

---

## Notes

- **Progressive vs. Adaptive Streams**:
  - Progressive streams contain both video and audio and are downloaded directly.
  - Adaptive streams require separate downloads for video and audio, which are then merged.

- **Temporary Files**:
  - Temporary files (e.g., `.mp4` and `.m4a`) are deleted after merging.

- **Error Handling**:
  - If the video is unavailable or the URL is invalid, the script will display an error message.

---

## Troubleshooting

1. **Video Freezes During Playback**:
   - Ensure FFmpeg is installed and added to your system's PATH.
   - If the issue persists, try re-encoding the video using the `ffmpeg` command:
     ```bash
     ffmpeg -i input.mp4 -c:v libx264 -c:a aac output.mp4
     ```

2. **No Audio After Merging**:
   - Check if the audio stream was downloaded successfully.
   - Ensure the audio file (`.m4a`) is not corrupted.

3. **Dependency Errors**:
   - Make sure all required libraries are installed:
     ```bash
     pip install pytubefix moviepy requests
     ```

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

---

## Acknowledgments

- [pytubefix](https://github.com/pytubefix/pytubefix) for YouTube video downloading.
- [moviepy](https://zulko.github.io/moviepy/) for video and audio merging.

---

Enjoy downloading YouTube videos with ease! 🎥🎶

---
