from flask import Flask, render_template, request, send_file
import yt_dlp
from pathlib import Path
import sys

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        path = download(url)
        return send_file(path, as_attachment=True)
    return render_template("index.html")



def download(url):
    global status

    if getattr(sys, 'frozen', False):
        path = Path(sys.executable).resolve().parent
    else:
        path = Path(__file__).resolve().parent

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': False,
        'outtmpl': f'{path}/output/%(title)s.%(ext)s',
    }



    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info)
        file_path = Path(file_path).with_suffix(".mp3")
    return file_path

if __name__ == "__main__":
    app.run(debug=True)