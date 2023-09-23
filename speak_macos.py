##
# Macos cannot currently use pyttsx3 (it used to work but no longer) so
# we need to use a Macos specific way. Not a big issue as it's just for
# one platform
##

import time

from AppKit import NSSpeechSynthesizer

class Speak:
    def __init__(self, voice):
        self.nssp = NSSpeechSynthesizer.alloc().initWithVoice_(voice)

    def say(self, text):
        self.nssp.startSpeakingString_(text)
        while self.nssp.isSpeaking():
            time.sleep(0.01)
