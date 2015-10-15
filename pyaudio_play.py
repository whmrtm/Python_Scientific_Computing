# -*- coding: utf-8 -*-
import pyaudio
import wave



wf = wave.open(r"sample.wav", 'rb')

CHUNK = 1024
RATE = wf.getframerate()




pread = pyaudio.PyAudio()
precord = pyaudio.PyAudio()
# Open stream
stream1 = pread.open(format = pread.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = RATE,
                output = True)

stream2 = precord.open(format = pread.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = RATE,
                input = True)
# write stream
print("* recording")

frames = []



while True:

    data = wf.readframes(CHUNK)
    if data == "": break
    stream1.write(data)
    read_data = stream2.read(CHUNK)
    frames.append(data)
print("* done recording")
    




stream1.close()
stream2.close()

pread.terminate()
precord.terminate()
print(frames)