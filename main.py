# Icons made by <a href="https://www.flaticon.com/authors/bqlqn" title="bqlqn">bqlqn</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>

import tkinter as tk
from tkinter import ttk  # Normal Tkinter.* widgets are not themed!
from ttkthemes import ThemedTk
from tkinter import messagebox
import pygame
from tkinter.filedialog import askopenfilename
import os
from mutagen.mp3 import MP3

pygame.init()

root = ThemedTk(theme="radiance")
root.title("Melody")
root.iconbitmap('images/melody_icon.ico')
root.geometry('620x300')
root.maxsize(620, 300)
root.minsize(620, 300)
text = tk.Label(root, text="Melody Music Player", font='Helvetica 18 bold')
text.pack()

status = tk.Label(root, text="Status bar", font='Helvetica 9',
                  relief='sunken', anchor="w")
status.pack(side="bottom", fill='x')

mp3_len_show = ttk.Label(root, text="", font='Helvetica 11')
mp3_len_show.pack()


def about_us():
    tk.messagebox.showinfo("Message", "This is About Us!")


def open_file():
    global filename, file
    filename = tk.filedialog.askopenfilename()
    file = os.path.basename(filename)
    show_listbox(filename)
    open_file.has_been_called = True
    pass


open_file.has_been_called = False


menubar = tk.Menu(root)
file = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=file)
file.add_command(label='Add File', command=open_file)
file.add_separator()
file.add_command(label='Exit', command=root.destroy)

Help = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='Help', menu=Help)
Help.add_command(label='Support')
Help.add_command(label='About Us', command=about_us)

# Diving the whole window into two frames (left frame and right frame)

left_frame = tk.Frame(root)
left_frame.pack(side='left', padx=6)

right_frame = tk.Frame(root)
right_frame.pack(side='right')


# Creating a Frame for only the Music controlled (middle) elements.
middle_frame = tk.Frame(right_frame)
middle_frame.pack(pady=10, padx=20)

# Creating a Frame for only bottom elements.
bottom_frame = tk.Frame(right_frame)
bottom_frame.pack(pady=10, padx=20)

paused = False


def play_music():
    global paused, playlis_song
    if paused == False:
        try:
            select_cur_indx = listbox.curselection()
            playlis_song = playlis[select_cur_indx[0]]
            # pygame.mixer.music.load(filename)
            pygame.mixer.music.load(playlis_song)
            pygame.mixer.music.play()
            status['text'] = "Playing "+playlis_song
            mp3_length_cal()

        except:
            tk.messagebox.showerror("Error", "Oops! No MP3 File Selected ")

    else:
        pygame.mixer.music.unpause()
        paused = False
        status['text'] = "Playing "+playlis_song


def stop_music():
    pygame.mixer.music.stop()
    status['text'] = "Music Stopped"


paused = False


def pause_music():
    global paused
    pygame.mixer.music.pause()
    paused = True
    status['text'] = "Music Paused"


def set_volume(val):
    volume = float(val)/100
    pygame.mixer.music.set_volume(volume)


muted = False


def mute_music():
    global muted
    if muted:
        volume_btn.config(image=volume_photo)
        pygame.mixer.music.set_volume(0.4)
        scale.set(35)
        muted = False
    else:
        volume_btn.config(image=mute_photo)
        pygame.mixer.music.set_volume(0)
        scale.set(0)
        muted = True


def mp3_length_cal():
    def converter(seconds):
        seconds %= 3600
        mins = seconds // 60
        seconds %= 60
        return mins, seconds
    audio = MP3(playlis_song)
    audio_info = audio.info
    length_in_secs = int(audio_info.length)
    mins, seconds = converter(length_in_secs)
    mp3_len_show['text'] = f"Length of MP3 {mins}:{seconds}"


playlis = []


def show_listbox(f):
    global playlis, listbox
    f = os.path.basename(f)
    index = 0
    listbox.insert(index, f)
    playlis.insert(index, filename)
    index += 1


def del_playlis():
    try:
        if open_file.has_been_called:
            select_cur_indx = listbox.curselection()
            listbox.delete(select_cur_indx)
            playlis.pop(select_cur_indx[0])
            stop_music()
            status['text'] = "File Deleted"
            if playlis == []:
                status['text'] = "Status bar"

        else:
            tk.messagebox.showerror("Error", "No File Exist")

    except:
        tk.messagebox.showerror("Error", "File selection error")


play_photo = tk.PhotoImage(file='images/play-button.png')
play_btn = ttk.Button(middle_frame, image=play_photo, command=play_music)
play_btn.pack(side='left', padx=7)

stop_photo = tk.PhotoImage(file='images/stop.png')
stop_btn = ttk.Button(middle_frame, image=stop_photo, command=stop_music)
stop_btn.pack(side='left', padx=7)

pause_photo = tk.PhotoImage(file='images/pause.png')
pause_btn = ttk.Button(middle_frame, image=pause_photo, command=pause_music)
pause_btn.pack(side='left', padx=7)


scale = ttk.Scale(bottom_frame, from_=0, to=100,
                  orient='horizontal', command=set_volume)
scale.set(35)
scale.pack(side='right', padx=5)

volume_photo = tk.PhotoImage(file='images/volume.png')
mute_photo = tk.PhotoImage(file='images/mute.png')
volume_btn = ttk.Button(bottom_frame, image=volume_photo, command=mute_music)
volume_btn.pack(side='right', padx=5)

listbox = tk.Listbox(left_frame, relief="sunken",
                     borderwidth=6, height=9, width=36)
listbox.pack()

btn1 = ttk.Button(left_frame, text="Add", command=open_file)
btn1.pack(side='left', padx=15)
btn2 = ttk.Button(left_frame, text="Del", command=del_playlis)
btn2.pack(side='left')

root.config(menu=menubar)
root.mainloop()
