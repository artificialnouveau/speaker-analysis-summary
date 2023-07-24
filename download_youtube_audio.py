import sys
import youtube_dl

def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',  # or mp3, etc
            'preferredquality': '192',  # bitrate, choose what you want
        }],
        'outtmpl': 'your_audio_file.wav',  # name for downloaded file
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please provide the YouTube URL as a command-line argument.")
        sys.exit(1)
    
    url = sys.argv[1]
    download_audio(url)
