import yt_dlp as youtube_dl
import uuid
import whisper
import os
import improve_transcript


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d["status"] == "finished":
        print("Done downloading, now converting ...")


def download_video(url: str) -> str:
    loc = str(uuid.uuid4())
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "logger": MyLogger(),
        "progress_hooks": [my_hook],
        "outtmpl": loc,
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return loc


def caption_video(filename: str):
    model = whisper.load_model("base")
    result = model.transcribe(filename, language="en", fp16=False)
    return result


file = download_video(url="https://www.youtube.com/watch?v=O51xSAeB1Mc") + ".mp3"
unmodified_text = caption_video(file)["text"]
print(unmodified_text)
print("-----------\n")
print(improve_transcript.improve_transcript(unmodified_text))
os.remove(file)
