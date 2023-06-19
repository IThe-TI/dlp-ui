#!/usr/bin/env python3
import json
import os
import subprocess
import time
import tkinter as tk
import yt_dlp

from tkinter import filedialog


"""
Tries to open and read the config. Generates one if it is invalid or it does not exist.
"""

try:
    with open("config.json", "r") as config_file:
        config = json.load(config_file)

        audio_directory = config["audio_directory"]
        video_directory = config["video_directory"]

        if not os.path.isdir(audio_directory) or not os.path.isdir(video_directory):
            raise FileNotFoundError
except:
    print("Config not found or invalid! Please select a folder to save music to and a folder to save videos to.")
    time.sleep(1)

    root = tk.Tk()
    root.withdraw()

    audio_directory = filedialog.askdirectory(title="Select music directory")
    video_directory = filedialog.askdirectory(title="Select video directory")

    if not os.path.isdir(audio_directory) or not os.path.isdir(video_directory):
        os._exit(2) #Closes in case the dirs don't exist, ie. above prompts got closed before selecting directory

    print(audio_directory)
    with open("config.json", "w") as config_file:
        config_file.write(f'''{{"audio_directory": "{audio_directory}", "video_directory": "{video_directory}"}}''')
    config_file.close()
    root.destroy()


"""
Miscelaneous helper functions
"""

def clear_screen():
    os.system('cls||clear')

def banner():
    print('''
     █████ ████                                   ███ 
    ░░███ ░░███                                  ░░░  
  ███████  ░███  ████████             █████ ████ ████ 
 ███░░███  ░███ ░░███░░███ ██████████░░███ ░███ ░░███ 
░███ ░███  ░███  ░███ ░███░░░░░░░░░░  ░███ ░███  ░███ 
░███ ░███  ░███  ░███ ░███            ░███ ░███  ░███ 
░░████████ █████ ░███████             ░░████████ █████
 ░░░░░░░░ ░░░░░  ░███░░░               ░░░░░░░░ ░░░░░ 
                 ░███                                 
                 █████                                
                ░░░░░                                 
    ''')

def invalid_selection(selection):
    if selection == '':
        selection = 'An empty string'
    elif selection.isspace():
         selection = 'A space'
                 
    print(f"{selection} is not a valid option!")
    time.sleep(1)


"""
------------------------------------
Selection screen
------------------------------------
"""
def selection_display():
    clear_screen()
    banner()
    selection = input('''
    -------------------
    [1] Download audio
    [2] Download video
    [3] Options
    [4] Exit
    -------------------
    ''')
    selection.strip()

    if selection == '1':
        audio_display()
    elif selection == '2':
        video_display()
    elif selection == '3':
        options_display()
    elif selection == '4':
        clear_screen()
        os._exit(0)
    else:
        invalid_selection(selection)
        selection_display()                


"""
------------------------------------
Dowload audio screen
------------------------------------
"""
def audio_display():
    clear_screen()
    url = input(f'''
      _         
     /_|   _/'  
    (  |(/(//() 
            
    Audio will be downloaded to {audio_directory}
    Input video link or leave empty to return: 
    ''')

    url.strip()
    if url.isspace():
        clear_screen()
        selection_display()
    else:
        ydl_opts = {
            'outtmpl': audio_directory + '%(title)s.%(ext)s',
            'format': 'm4a/bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',  
            }]  
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(url)

        time.sleep(0.5)
        selection_display()


"""
------------------------------------
Dowload video screen
------------------------------------
"""
def video_display():
    clear_screen()
    url = input(f'''  
    (  /'_/_   
    |_//(/(-() 
           
    Video will be downloaded to {video_directory}
    Input video link or leave empty to return: 
    ''')

    url.strip()
    if url.isspace():
        clear_screen()
        selection_display()
    else:
        ydl_opts = {
            'outtmpl': video_directory + '%(title)s.%(ext)s',
            'format': 'mp4/bestaudio/best',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(url)

        time.sleep(0.5)
        selection_display()


"""
------------------------------------
Options screen
------------------------------------
"""
def options_display():
    clear_screen()
    selection = input(f'''
      __            
     /  ) _/'     _ 
    (__//)//()/)_)  
       /   

    -------------------
    [1] Change audio output directory (Currently {audio_directory})
    [2] Change video output directory (Currently {video_directory})
    [3] Update yt-dlp
    [4] Back
    ''')

    if selection == '1':
        change_dir_display('audio')
    elif selection == '2':
        change_dir_display('video')
    elif selection == '3':
        subprocess.run("python3 -m pip install -U yt-dlp")
        time.sleep(1)
        options_display()
    elif selection == '4':
        selection_display()
    else:
        invalid_selection(selection)
        options_display()

"""
------------------------------------
Change download directory screen
------------------------------------
Saves to ./config.json
"""
def change_dir_display(option):
    clear_screen()

    root = tk.Tk()
    root.withdraw()

    if option == 'audio':
        global audio_directory
        audio_directory_temp = filedialog.askdirectory(title="Select music directory")

        if not audio_directory_temp.isspace() and os.path.isdir(audio_directory_temp):
            audio_directory = audio_directory_temp
        else:
            print("Please select a valid directory")
            time.sleep(1)
            options_display()

    elif option == 'video':   
        global video_directory
        video_directory_temp = filedialog.askdirectory(title="Select video directory")

        if not video_directory_temp.isspace() and os.path.isdir(video_directory_temp):
            video_directory = video_directory_temp
        else:
            print("Please select a valid directory")
            time.sleep(1)
            options_display()  

    with open("config.json", "w") as config_file:
        config_file.write(f'''{{"audio_directory": "{audio_directory}", "video_directory": "{video_directory}"}}''')
        config_file.close()
        options_display()  


def main():
    selection_display()

if __name__ == "__main__":
    main()