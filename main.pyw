from infi.systray import SysTrayIcon
import win32clipboard
import youtube_dl as ydl
import json
import threading
import os

def open_options(systray):
    os.startfile("options.json")

def download(options: list, data: list):
    with ydl.YoutubeDL(options) as yd:
        yd.download(data)
    os.startfile(os.path.realpath("outputs/"))

def convert_from_clipboard(systray):
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()

    jsonFile = open("options.json")
    jsonOptions = json.load(jsonFile)

    ydl_opts = {}

    defaultpath = f'{jsonOptions["defaultOutput"]}/'

    if jsonOptions["preferedFormat"] == "audio":
        print("AUDIO ONLY!")
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': defaultpath+'%(title)s'+'.mp3',
        }
    elif jsonOptions["preferedFormat"] == "video":
        print("VIDEO AND AUDIO!")
        
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': defaultpath+'%(title)s',
        }

    #download(ydl_opts, [data])
    downloadMethod = threading.Thread(target=download, args=(ydl_opts, [data]))
    downloadMethod.start()

    print("Video is done downloading!")

menu_options = (("Convert From Clipboard", None, convert_from_clipboard), ("Options", None, open_options))
systray = SysTrayIcon(None, "Video Converter", menu_options)
systray.start()