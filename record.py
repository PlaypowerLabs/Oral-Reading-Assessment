from sys import byteorder
from array import array
from struct import pack
import pyaudio, wave
from settings import RATE, MAX_INPUT_CHANNELS, WAVE_OUTPUT_FILE, INPUT_DEVICE, CHUNK_SIZE, THRESHOLD, TRIM_THRESHOLD

class Sound:

    def __init__(self):
        self.format = pyaudio.paInt16
        self.channels = MAX_INPUT_CHANNELS
        self.sample_rate = RATE
        self.chunk = CHUNK_SIZE
        self.path = WAVE_OUTPUT_FILE
        self.device = INPUT_DEVICE
        self.frames = array('h')
        self.audio_data = array('h')
        self.audio = pyaudio.PyAudio()
        self.threshold = THRESHOLD
        self.trim_threshold = TRIM_THRESHOLD

    
    def is_silent(self, snd_data):
        print(max(snd_data))
        return max(snd_data) < self.threshold
    
    def normalize(self):
        MAXIMUM = 16384
        times = float(MAXIMUM)/max(abs(i) for i in self.frames)

        self.audio_data = array('h')
        for i in self.frames:
            self.audio_data.append(int(i*times))

    def trim(self):

        def _trim(snd_data):
            snd_started = False
            r = array('h')

            for i in snd_data:
                if not snd_started and abs(i)>self.trim_threshold:
                    snd_started = True
                    r.append(i)

                elif snd_started:
                    r.append(i)
            return r

    # Trim to the left
        self.audio_data = _trim(self.audio_data)

    # Trim to the right
        self.audio_data.reverse()
        self.audio_data = _trim(self.audio_data)
        self.audio_data.reverse()
    
    def add_silence(self,seconds):
        silence = [0] * int(seconds * self.sample_rate)
        r = array('h', silence)
        r.extend(self.audio_data)
        r.extend(silence)
        self.audio_data = r

    
    def record(self):
        """
        Record a word or words from the microphone and 
        return the data as an array of signed shorts.

        Normalizes the audio, trims silence from the 
        start and end, and pads with 0.5 seconds of 
        blank sound.
        """

        self.audio = pyaudio.PyAudio()
        stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk,
            input_device_index=self.device
        )

        num_silent = 0
        snd_started = False

        self.frames = array('h')

        while 1:
            # little endian, signed short
            snd_data = array('h', stream.read(self.chunk))

            if byteorder == 'big':
                snd_data.byteswap()
            self.frames.extend(snd_data)

            silent = self.is_silent(snd_data)

            if silent and snd_started:
                num_silent += 1

            elif not silent and not snd_started:
                snd_started = True
            
            elif not silent and snd_started:
                num_silent=0

            if snd_started and num_silent > 32:
                break
        
        
        stream.stop_stream()
        stream.close()
        self.audio.terminate()
        
        self.normalize()
        self.trim()
        self.add_silence(0.5)
        


    def record_audio(self):
        self.record()
        data = pack('<' + ('h'*len(self.audio_data)), *self.audio_data)

        wf = wave.open(self.path, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.audio.get_sample_size(self.format))
        wf.setframerate(self.sample_rate)
        wf.writeframes(data)
        wf.close()