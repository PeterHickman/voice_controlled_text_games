# Voice controlled text games

I was listening to a podcast and someone said that someone else had implemented zork as a voice controlled app. It spoke the output text and did speech to text for input. Sounded cool so I looked into doing this for myself

Well it is *interesting* but not quite an immersive experience I wanted. But here it is in all of it's Pythonic glory

You will need to set up a Python virtual environment (I used 3.8) and install the requirements for your platform. Run `voices_linux.py` or `voices_macos.py` to get a list of the available voices to use and add it to `settings.py`

Also run `mics.py` to get the index of the input device you want to use and put it in `settings.py` too

It is presently set up to run `advent`, the original Colossal Caves but you can change that, again in `settings.py`
