import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import yt_dlp
import os
import re

class DownloadProgress:
    def __init__(self, progress_bar):
        self.progress_bar = progress_bar

    def update(self, d):
        if d['status'] == 'downloading':
            percent_str = d.get('_percent_str', '0%')
            # Remove ANSI color codes and extract the percentage
            clean_percent = re.sub(r'\x1b\[[0-9;]*m', '', percent_str)
            percent = float(clean_percent.strip('%'))
            self.progress_bar['value'] = percent
            root.update_idletasks()

def download_video():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL.")
        return
    
    save_path = filedialog.askdirectory()
    if not save_path:
        messagebox.showerror("Error", "Please select a save location.")
        return
    
    progress_bar['value'] = 0
    download_button['state'] = 'disabled'
    url_entry['state'] = 'disabled'
    
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
        'progress_hooks': [DownloadProgress(progress_bar).update],
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_title = info['title']
        messagebox.showinfo("Success", f"Video '{video_title}' downloaded successfully to {save_path}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
    finally:
        download_button['state'] = 'normal'
        url_entry['state'] = 'normal'
        progress_bar['value'] = 0

# Create the main window
root = tk.Tk()
root.title("YouTube MP4 Downloader")
root.geometry("400x200")

# Create and place widgets
url_label = tk.Label(root, text="Enter YouTube URL:")
url_label.pack(pady=10)

url_entry = tk.Entry(root, width=50)
url_entry.pack()

download_button = tk.Button(root, text="Download", command=download_video)
download_button.pack(pady=20)

# Create and place the progress bar
progress_bar = ttk.Progressbar(root, orient='horizontal', length=300, mode='determinate')
progress_bar.pack(pady=10)

# Configure the progress bar style
style = ttk.Style()
style.theme_use('default')
style.configure("TProgressbar", thickness=20, troughcolor='lightgray', background='purple')

# Start the GUI event loop
root.mainloop()
