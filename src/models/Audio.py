import threading
import pyaudio
import wave
import time


class Audio:
    def __init__(self, chunk: int, sample_format: int, channels: int, fs: int) -> None:
        self.__chunk: int = chunk
        self.__sample_format: int = sample_format
        self.__channels: int = channels
        self.__fs: int = fs
    
        self.__seconds: int = 0
        self.__minutes: int = 0

        self.__stream: pyaudio.Stream = None
        self.__py_audio: pyaudio.PyAudio = pyaudio.PyAudio()
        self.__frames: list[bytes] = []

        self.__end_audio: bool = False
        self.__recording_thread: threading.Thread = None
        self.__timer_thread: threading.Thread = None

    @property
    def chunk(self) -> int:
        return self.__chunk

    @property
    def sample_format(self) -> int:
        return self.__sample_format
    
    @property
    def channels(self) -> int:
        return self.__channels
    
    @property
    def fs(self) -> int:
        return self.__fs
    
    @property
    def seconds(self) -> int:
        return self.__seconds
    
    @property
    def minutes(self) -> int:
        return self.__minutes

    @property
    def stream(self) -> pyaudio.Stream:
        return self.__stream

    @property
    def py_audio(self) -> pyaudio.PyAudio:
        return self.__py_audio
    
    @property
    def frames(self) -> list[bytes]:
        return self.__frames
    
    @property
    def end_audio(self) -> bool:
        return self.__end_audio

    @property
    def recording_thread(self) -> threading.Thread:
        return self.__recording_thread
    
    @property
    def timer_thread(self) -> threading.Thread:
        return self.__timer_thread

    def start_record(self, input: bool = True) -> None:
        self.__stream = self.py_audio.open(
            format = self.sample_format,
            channels = self.channels,
            rate = self.fs,
            frames_per_buffer = self.chunk,
            input = input
        )

        self.__recording_thread = threading.Thread(target=self._add_frame)
        self.__timer_thread = threading.Thread(target=self._run_timer)

        self.recording_thread.start()
        self.timer_thread.start()


    def _add_frame(self) -> None:
        while not self.end_audio:
            data = self.stream.read(self.chunk)
            self.__frames.append(data)


    def stop_record(self, filename: str) -> None:
        if not filename.strip():
            self._reset_state()
            raise ValueError("You must enter a valid name to save the file.")
        
        self.__end_audio = True

        if not self.recording_thread or not self.timer_thread:
            self._reset_state()
            raise RuntimeError("You must start an audio to be able to stop it.")

        self.recording_thread.join()
        self.timer_thread.join()
            
        self.stream.stop_stream()
        self.stream.close()
        self.py_audio.terminate()

        wave_write = wave.open(f"{filename}.wav", "wb")
        wave_write.setnchannels(self.channels)
        wave_write.setsampwidth(self.py_audio.get_sample_size(self.sample_format))
        wave_write.setframerate(self.fs)
        wave_write.writeframes(b"".join(self.frames))
        wave_write.close()

        self._reset_state()


    def _run_timer(self) -> None:
        next_time = time.time() + 1
        while not self.end_audio:
            time.sleep(max(0, next_time - time.time()))

            self.__seconds += 1

            if self.seconds >= 60:
                self.__seconds = 0
                self.__minutes += 1

            next_time += (time.time() - next_time) // 1 * 1 + 1


    def _reset_state(self) -> None:
        if self.recording_thread: self.recording_thread.join()
        if self.timer_thread: self.timer_thread.join()

        if self.stream:  
            self.stream.stop_stream()
            self.stream.close()
        
        if self.py_audio: self.py_audio.terminate()

        self.__seconds = 0
        self.__minutes = 0

        self.__stream = None
        self.__py_audio = pyaudio.PyAudio()
        self.__frames = []

        self.__end_audio = False
        self.__recording_thread = None
        self.__timer_thread = None


    def __str__(self) -> None:
        return (
            f"Chunk: {self.chunk}\n"
            f"SampleFormat: {self.sample_format}\n"
            f"Channels: {self.channels}\n"
            f"Fs: {self.fs}\n"
            f"Seconds: {self.seconds}\n"
            f"Minutes: {self.minutes}\n"
            f"Stream: {self.stream}\n"
            f"PyAudio: {self.py_audio}\n"
            # f"Frames: {self.frames}\n"
            f"End Audio: {self.end_audio}\n"
            f"Recording Thread: {self.recording_thread}\n"
            f"Timer Thread: {self.timer_thread}\n"
        )


if __name__ == "__main__":
    audio = Audio(chunk=1024, sample_format=16, channels=1, fs=44100)

    count = 0
    audio.start_record()

    while count <= 10:
        count +=1
        time.sleep(1)
        if count == 10: audio.stop_record("item")

    print(audio)
