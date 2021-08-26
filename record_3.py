import pyaudio, wave
from settings import DEFAULT_SAMPLE_RATE, MAX_INPUT_CHANNELS, WAVE_OUTPUT_FILE, INPUT_DEVICE, CHUNK_SIZE, DURATION


class Sound():

    def __init__(self):
        
        self.format = pyaudio.paInt16
        self.channels = MAX_INPUT_CHANNELS
        self.sample_rate = DEFAULT_SAMPLE_RATE
        self.chunk = CHUNK_SIZE
        self.path = WAVE_OUTPUT_FILE
        self.device = INPUT_DEVICE
        self.frames = []
        self.audio = pyaudio.PyAudio()
        self.rec = 1
        self.duration = DURATION

    def record_audio(self):
        
        print('4')
        self.rec = 1        
        self.audio = pyaudio.PyAudio()
        stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk,
            input_device_index=self.device
        )
        self.frames = []
        print('5')
        # while self.rec == 1:
        #     data = stream.read(self.chunk)
        #     self.frames.append(data)

        for i in range(0, int(self.sample_rate / self.chunk * self.duration)):
            data = stream.read(self.chunk)
            print(min(data))
            self.frames.append(data)
        
        print('8')
        stream.stop_stream()
        stream.close()
        self.audio.terminate()
        print('9')
        self.save()

    def save(self):
        print('10')
        wavFile = wave.open(self.path,'wb')
        wavFile.setnchannels(self.channels)
        wavFile.setsampwidth(self.audio.get_sample_size(self.format))
        wavFile.setframerate(self.sample_rate)
        wavFile.writeframes(b''.join(self.frames))
        wavFile.close()
        print('11')
    
    def stop_recording(self):
        print('7')
        self.rec = 0


#sound = Sound()


