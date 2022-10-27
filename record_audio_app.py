from tkinter import *
import pyaudio
import wave

# Tkinter
root = Tk()
root.title('Record Audio APP')
root.geometry('400x400')
root.config(bg="#09f")
root.resizable(False, False)

# Timer
sec = 0
mins = 0
interval_crono = None

# PyAudio Config
chunk = 1024
sample_format = pyaudio.paInt16
channels = 1
fs = 44100
filename = StringVar()
py_audio = None
stream = None
frames = []

mic_image = PhotoImage(file="./mic.png")
mic_image_on = PhotoImage(file="./micon.png")
 
label_image = Label(root, image=mic_image, border=0)
label_image.place(x=200, y = 100, anchor="center")

entry_name_audio = Entry(width=15, font=("Roboto 15"), textvariable=filename)
entry_name_audio.place(x = 200, y = 200, anchor="center")

start_button = Button(root, width=15, text="Start Record", font=("Roboto 15"), bg="#e43a3a", fg="#fff", border=0, command=lambda:record(), state=NORMAL)
start_button.place(x = 200, y = 250, anchor="center")
stop_button = Button(root, width=15, text="Stop Record", font=("Roboto 15"), bg="#e43a3a", fg="#fff", border=0, state=DISABLED, command=lambda:crono_finish())
stop_button.place(x = 200, y = 300, anchor="center")
crono_label = Label(root, width=25, bg="#09f", fg="#fff", font=("Roboto 12"))
crono_label.place(x = 200, y = 350, anchor="center")
crono_label.config(text="Inicia")

def record():

    global interval_crono, py_audio, stream, frames

    py_audio = pyaudio.PyAudio()

    crono_init()

    stream = py_audio.open(format = sample_format,
    channels = channels,
    rate = fs,
    frames_per_buffer = chunk,
    input = True)

    def save_data():

        if interval_crono:
            data = stream.read(chunk)
            frames.append(data)
            root.after(1, save_data)

    save_data()
        

def crono_init():

    global sec, mins, interval_crono

    stop_button['state'] = NORMAL 
    start_button['state'] = DISABLED 
    label_image['image'] = mic_image_on

    sec+=1

    if sec < 10:
        crono_label["text"] = f"{mins}:0{sec}" 
    elif sec >= 10:
        crono_label["text"] = f"{mins}:{sec}"  
    elif sec >= 60:
        mins += 1
        sec = 0
        crono_label["text"] = f"{mins}:0{sec}"  
        

    interval_crono = root.after(1000, crono_init)


def crono_finish():

    global interval_crono, py_audio, stream, frames, mins, sec

    if sec < 10:
        crono_label["text"] = f"Finished in: {mins}:0{sec}. {filename.get()} saved."
    else:
        crono_label["text"] = f"Finished in: {mins}:{sec}. {filename.get()} saved."

    stop_button['state'] = DISABLED
    start_button['state'] = NORMAL 
    label_image['image'] = mic_image

    stream.stop_stream()
    stream.close()
    py_audio.terminate()

    wf = wave.open(f"{filename.get()}.wav", "wb")
    wf.setnchannels(channels)
    wf.setsampwidth(py_audio.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b"".join(frames))
    wf.close()

    if interval_crono is not None:
        root.after_cancel(interval_crono)
        interval_crono = None
        filename.set("Insert a new one")
        py_audio = None
        stream = None
        frames = []
        sec = 0
        mins = 0



root.mainloop()