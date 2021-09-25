import tkinter
from threading import Thread
from time import sleep
from tkinter import DISABLED, END, Tk, Label, TOP, Entry, CENTER, X, NORMAL, Button, ACTIVE, BOTTOM
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showinfo

from pytube import YouTube

file_size = 0
start = False


def launch():
    global start
    start = True


def download_progression(stream=None, chunk=None, file_handle=None):
    file_downloaded = (file_size - file_handle)
    percentage = float((file_downloaded / file_size) * 100)
    download2_button.config(text="{:00.3f} % downloaded".format(percentage), state=DISABLED)


def download():
    global file_size, n, quality
    try:
        url = url_entry.get()
        path = askdirectory()
        download_button.config(text="Loading...", state=DISABLED)
        if url is None:
            return
        obj = YouTube(url, on_progress_callback=download_progression)

        download_button.config(text="Loaded", state=DISABLED)
        stream = obj.streams.filter(type="video")

        qualities = list()
        for i in range(len(stream)):
            qualities += i, str(stream[i].resolution), str(stream[i].mime_type)

        qualities_bis = str()
        for i in range(0, len(qualities), 3):
            qualities_bis += str(qualities[i]) + " " + str(qualities[i + 1]) + " " + str(qualities[i + 2]) + str(" \n")
        quality = qualities_bis.split("\n")

        if quality:
            listbox = tkinter.Listbox(top)
            listbox.pack()
            for item in quality:
                listbox.insert(END, item)
            download2_button.config(state=NORMAL)
            while not start:
                n = listbox.get(ACTIVE)
                sleep(1)
            n = int(str(n[0:2]))

        file_size = stream[n].filesize
        stream[n].download(path)
        download_button.config(text="Downloaded", state=DISABLED)
        showinfo("Download finished", "Done !")
        url_entry.delete(0, END)
    except Exception as e:
        # Download Button
        download_button.config(text="Load file", state=NORMAL)
        download2_button.config(text="Download file", state=DISABLED)
        return


def download_thread():
    t = Thread(target=download)
    t.start()


top = Tk()

# Base conf
top.title("Py YTB DL")
top.geometry("600x300")
top.minsize(600, 300)
top.maxsize(600, 300)
top.resizable(0, 0)
top.configure(background="#ffffff")

# Label Input URL
welcome_label = Label(top)
welcome_label.pack(side=TOP)
welcome_label.configure(activebackground="#f0f0f0f0f0f0", background="#ffffff")
welcome_label.configure(disabledforeground="#a3a3a3", foreground="#000000", text='''Input an URL:''')

# URL Entry
url_entry = Entry(top, justify=CENTER)
url_entry.pack(side=TOP, fill=X, padx=10)
url_entry.configure(background="white", disabledforeground="#a3a3a3", font="TkFixedFont")
url_entry.configure(foreground="#000000", insertbackground="black")

# Download Button
download_button = Button(top, text="Load file", command=download_thread, state=NORMAL)
download_button.pack(side=TOP, pady=10)

download2_button = Button(top, text="Download file", command=launch, state=DISABLED)
download2_button.pack(side=BOTTOM, pady=10)

top.mainloop()
