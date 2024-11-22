# Record Audio Program

## Getting Started

1. Clone the repository
2. Join to the correct path of the clone
3. Execute: `python -m venv venv`
4. Execute in Windows: `venv\Scripts\activate`
5. Execute: `pip install -r requirements.txt`
6. Execute: `pip install -r requirements.test.txt`
7. Use `python -m src.app` to execute program

## Description

I made a program in python with tkinter as the user interface that allows the user to enter the name of a future audio, start recording an audio and save it when the stop button is tapped. Basically I made a voice recorder with python and tkinter.

## Technologies used

1. Python

## Libraries used

#### Requirements.txt

```
PyAudio==0.2.12
```

#### Requirements.test.txt

```
pytest
```

## Portfolio Link

[`https://www.diegolibonati.com.ar/#/project/Record-Audio-Program`](https://www.diegolibonati.com.ar/#/project/Record-Audio-Program)

## Video

https://user-images.githubusercontent.com/99032604/198900280-02b26523-e7b3-4c0a-91f5-c325b49270ea.mp4

## Testing

1. Join to the correct path of the clone
2. Execute in Windows: `venv\Scripts\activate`
3. Execute: `pytest --log-cli-level=INFO`