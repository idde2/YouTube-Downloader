import yt_dlp
from pathlib import Path
import sys
import customtkinter as ctk
import threading

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

status = 0

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("youtube downloader")
        self.geometry("400x250")

        self.entry = ctk.CTkEntry(self, width=250, placeholder_text="Text eingeben...")
        self.entry.pack(pady=(30, 10))

        self.entry.bind("<Return>", self.on_send)

        self.button = ctk.CTkButton(self, text="Senden", command=self.on_send)
        self.button.pack()

        self.output = ctk.CTkLabel(self, text="", font=("Arial", 14))
        self.output.pack(pady=10)

        self.progress = ctk.CTkProgressBar(self, width=250)
        self.progress.set(0)
        self.progress.pack(pady=10)

        self.after(100, lambda: self.entry.focus())

    def on_send(self, event=None):
        url = self.entry.get()
        self.entry.delete(0, "end")
        self.output.configure(text="Downloading...")
        self.progress.set(0)

        threading.Thread(target=self.threaded_download, args=(url,), daemon=True).start()

    def threaded_download(self, url):
        global status

        def update_progress(value):
            self.progress.set(value)

        download(url, update_progress)

        if status == 0:
            self.output.configure(text="Download successful")
        else:
            self.output.configure(text="Download failed")

        self.progress.set(0)


if getattr(sys, 'frozen', False):
    path = Path(sys.executable).resolve().parent
else:
    path = Path(__file__).resolve().parent


def download(url, progress_callback):
    global status

    def hook(d):
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded = d.get('downloaded_bytes', 0)

            if total:
                progress = downloaded / total
                progress_callback(progress)

    ydl_opts = {
        'format': 'bestaudio/best',
        'progress_hooks': [hook],
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': False,
        'outtmpl': f'{path}/output/%(title)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        status = ydl.download([url])


if __name__ == '__main__':
    app = App()
    app.mainloop()
