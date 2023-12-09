# Record-Audio-Program

## Getting Started

1. Clone the repository
2. Join to the correct path of the clone
3. Install requirements.txt
4. Use `python record_audio_program.py` to execute program

## Description

I made a program in python with tkinter as the user interface that allows the user to enter the name of a future audio, start recording an audio and save it when the stop button is tapped. Basically I made a voice recorder with python and tkinter.

## Technologies used

1. Python

## Libraries used

1. Tkinter
2. pyaudio
3. wave

## Portfolio Link

[`https://www.diegolibonati.com.ar/#/project/84`](https://www.diegolibonati.com.ar/#/project/84)

## Video

https://user-images.githubusercontent.com/99032604/198900280-02b26523-e7b3-4c0a-91f5-c325b49270ea.mp4

## Documentation

These variables correspond to the initial state of the stopwatch that is displayed once we start recording:

```
sec = 0
mins = 0
interval_crono = None
```

These variables correspond to the pyAudio library configuration:

```
chunk = 1024
sample_format = pyaudio.paInt16
channels = 1
fs = 44100
filename = StringVar()
py_audio = None
stream = None
frames = []
```

Once we click on `Start Record` the py_audio object will be initialized, initializing the class itself. Then we will execute the `crono_init()` function, we will reassign the pyaudio configuration, finally we will start saving the frames in the list properly named: `frames`:

```
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
```

In this place the `crono_init()` function will be executed. This function initializes the count in seconds at the moment of recording the audio. It also parses those seconds into minutes depending if 60 seconds have already passed. This function will be executed every 1 second:

```
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
```

Once the `Stop Record` button is tapped, this `crono_finish()` function will be executed. Basically it will stop the stopwatch count, it will also go through and join frame by frame the data saved in the location we set by default with the extension we set by default as well:

```
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
```
