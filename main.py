import asyncio
from songtracker import SongTracker

async def main() -> None:
    tracker = SongTracker()
    if await tracker.get_new_session():
        await tracker.update_current_song()
        print(tracker.current_song)


asyncio.run(main())