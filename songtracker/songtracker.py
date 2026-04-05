from winrt.windows.media.control import (
    GlobalSystemMediaTransportControlsSessionManager as MediaManager,
)
import asyncio


class SongTracker:
    def __init__(self) -> None:
        self.current_song: dict[str, str] | None = None
        self.session: MediaManager | None = None

    async def get_new_session(self) -> bool:
        """
        ask MediaManager for a new session.\n
        returns True on sucess False on fail.\n
        session can be found under Songtracker.session
        """
        self.session = await MediaManager.request_async()
        if self.session:
            return True
        return False

    async def update_current_song(self) -> bool:
        """
        ask MediaManager for the currently playing media
        and turns it into a dict.\n
        """
        if self.session:
            current_media = self.session.get_current_session()
            if current_media:
                song = await current_media.try_get_media_properties_async()
                if song:
                    self.current_song = {
                        "title": song.title,
                        "artist": song.artist,
                    }
                    return True
        return False
