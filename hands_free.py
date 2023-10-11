#!/usr/bin/env python3

import platform
import json
from vosk import Model, KaldiRecognizer
import sounddevice
import soundfile
import queue
import time
import pexpect

plat = platform.system()

if plat == 'Darwin':
    from speak_macos import Speak
elif plat == 'Linux':
    from speak_linux import Speak
else:
    print("Don't know how to set up for {}".format(plat))
    sys.exit(1)

class Listen:
    def __init__(self, model, input_device_index):
        self.input_device_index = input_device_index
        self.model = Model(model)
        device = sounddevice.query_devices(input_device_index, "input")
        self.samplerate = int(device['default_samplerate'])
        self.q = queue.Queue()
        self.rec = KaldiRecognizer(self.model, self.samplerate)

    def listen(self):
        with sounddevice.RawInputStream(samplerate=self.samplerate, blocksize=8192, device=self.input_device_index, dtype="int16", channels=1, callback=self._callback):
            while True:
                data = self.q.get()
                if self.rec.AcceptWaveform(data):
                    text = self.rec.Result()
                    data = json.loads(text)
                    return data['text']

    def _callback(self, indata, frames, time, status):
        self.q.put(bytes(indata))

import settings

speak = Speak(settings.voice)
listen = Listen(settings.model, settings.input_device_index)

child = pexpect.spawn(settings.game)

data, fs = soundfile.read(settings.beep, dtype='float32')

def get_text():
    output = child.before.decode()

    lines = []

    for line in output.splitlines()[1:]:
        if not line.startswith(settings.ignore_starts_with):
            lines.append(line)

    output = " ".join(lines)

    return output

speak.say("Setup complete. This program will allow you to run a text based game using speech to text for input and text to speech for output")
time.sleep(0.2)
speak.say("When you need to tell the program what to do you will hear a beep")
time.sleep(1.0)

while True:
    # Clear out the buffer before getting any input
    if child.before:
        child.expect(r".+")

    try:
        index = child.expect(pexpect.EOF, timeout=1)
        if index == 0:
            # EOF, the program has ended
            break
    except:
        # Timeout, which is normal
        pass

    output = get_text()

    if settings.print_text:
        print(output)
    speak.say(output)

    sounddevice.play(data, fs)
    sounddevice.wait()

    t = listen.listen()
    child.sendline(t)

output = get_text()
if settings.print_text:
    print(output)
speak.say(output)
