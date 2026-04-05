# SongTracker
![License](https://img.shields.io/badge/license-GPL--3.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.13-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)

A python package for windows made to track the current song being listened to.

## usage
Intended usage:
```python 3.13
from songtracker import SongTracker
import asyncio

# Songtracker().run(callable)
# also possible to do SongTracker().run(callable, check_delay=5)
# default delay is 2.5sec
# Ex:
def broadcast(song):
    print(song) # song object __repr__ is f"{self.title} - {self.artist}"

asyncio.run(SongTracker().run(broadcast)) # will run infinitely and execute broadcast on song change
```
Manual usage:
```python 3.13
from songtracker import SongTracker
import asyncio

# /!\ Use try/Except statement to catch OSError on winrt error
# must be run inside an async function Ex: async def main() asyncio.run(main)

tracker = Songtracker()
if await tracker.get_new_session():
    #generates a winrt session and returns a bool (True = Success)
    if await tracker.update_current_song(): 
        #generates new song object if song has changed and returns bool (True = Success)
        if not tracker.current_song.error:
            # checks if song object is usable (song.error = 1 means artist or title is None)
            # do something
            print(tracker.currentsong) # song object __repr__ is f"{self.title} - {self.artist}"
```