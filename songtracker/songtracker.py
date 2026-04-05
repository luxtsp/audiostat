from winrt.windows.media.control import (
    GlobalSystemMediaTransportControlsSessionManager as MediaManager,
)
from typing import Callable
from time import sleep


class Song:
    def __init__(
        self, title: str | None = None, artist: str | None = None
    ) -> None:
        if not title or not artist:
            self.error = 1
        else:
            self.error = 0
        self.artist = artist
        self.title = title

    def __repr__(self) -> str:
        return f"{self.title} - {self.artist}"


class SongTracker:
    """
    This is SongTracker,
    a class communicating with the winrt package,
    creating a 'song' object.\n
    meant to be used with SongTracker.run(function(song))
    """

    def __init__(self) -> None:
        self.current_song: Song = Song()
        self.session: MediaManager | None = None

    def is_new_song(self, title: str, artist: str) -> bool:
        return (
            title != self.current_song.title
            or artist != self.current_song.artist
        )

    async def get_new_session(self) -> bool:
        """
        ask MediaManager for a new session.\n
        returns True on sucess False on fail.\n
        session can be found under Songtracker.session
        """
        self.session = await MediaManager.request_async()
        return True if self.session else None

    async def update_current_song(self) -> bool:
        """
        ask MediaManager for the currently playing media
        and turns it into a song object.\n
        song.title: str | song.artist: str |
        song.error: int (0 if good | 1 if error)
        """
        if not self.session:
            await self.get_new_session()
        if self.session:
            current_media = self.session.get_current_session()
            if current_media:
                media = await current_media.try_get_media_properties_async()
                if media and self.is_new_song(media.title, media.artist):
                    self.current_song = Song(
                        title=media.title, artist=media.artist
                    )
                    del media
                    return True
        return False

    async def run(
        self, function: Callable[[Song], None], check_delay: float = 2.5
    ) -> None:
        """
        runs indefinitely and calls given function
        on song change with song type as argument.\n

        function(song: song) - the function to be called on song change\n
        check_delay: float - the delay between checks for song change\n
        song.title: str | song.artist: str
        """
        while True:
            try:
                if await self.get_new_session():
                    if (
                        await self.update_current_song()
                        and not self.current_song.error
                    ):
                        function(self.current_song)
            except OSError as e:
                print(f"microslop says: {e}")
            sleep(check_delay)
