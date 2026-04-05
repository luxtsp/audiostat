import asyncio
import json
import websockets
from winrt.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager

#===========================
# Media Info part
#===========================
async def get_media_info(session):
	try:
		curr_sess = session.get_current_session()
	except:
		return {"title": "", "artist": "nobody 123456"}
	if curr_sess:
		try:
			info = await curr_sess.try_get_media_properties_async()
			info_dict = {song_attr: info.__getattribute__(song_attr) for song_attr in dir(info) if song_attr[0] != '_' and song_attr != 'thumbnail' and song_attr != 'genres'}
		except Exception as e:
			print(f"Error : {e}")
			return {"title": "", "artist": "nobody 123456"}
		finally:
			del info
		return info_dict
	return {"title": "", "artist": "nobody 123456"}

async def make_session():
	try:
		sessions = await MediaManager.request_async()
	except:
		print("error making session")
		return None
	return sessions

async def check_media(sessions):
	if sessions is None:
		return None
	return await get_media_info(sessions)

#========================
# Websocket part
#========================
async def broadcast_media(media_info):
	if connected_clients:
		message = json.dumps(media_info)
		dead_clients = set()
		for client in connected_clients:
			try:
				await client.send(message)
			except websockets.exceptions.ConnectionClosed:
				dead_clients.add(client)
			except Exception as e:
				print(f"Broadcast error: {e}")
				dead_clients.add(client)
		connected_clients.difference_update(dead_clients)

async def handler(websocket):
	connected_clients.add(websocket)
	try:
		async for message in websocket:
			pass 
	except websockets.exceptions.ConnectionClosed:
		pass
	except Exception as e:
		print(f"Handler error: {e}")
	finally:
		connected_clients.discard(websocket)

#======================
# Main
#======================
connected_clients = set()

async def main():
	last_song = "0"
	sessions = None
	
	async with websockets.serve(handler, "localhost", 8765):
		print("ws://localhost:8765")
		while True:
			try:
				if sessions is None:
					sessions = await make_session()
				current_song = await check_media(sessions)
				if current_song is not None and current_song["title"] != last_song:
					last_song = current_song["title"]
					if current_song["title"] == "":
						print("Nothing is playing")
					else:
						print(f"{current_song['title']} by {current_song['artist']}")
						await broadcast_media(current_song)
				
				await asyncio.sleep(1)
			except Exception as e:
				print(f"Main loop error: {e}")
				sessions = None
				await asyncio.sleep(2)

if __name__ == '__main__':
	asyncio.run(main())