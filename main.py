import asyncio

# Ensure an asyncio event loop exists in MainThread before importing Pyrogram
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

import config
import time
import logging
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from pyrogram import Client, idle
from pyromod import listen  # type: ignore
from pyrogram.errors import ApiIdInvalid, ApiIdPublishedFlood, AccessTokenInvalid, FloodWait

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"status": "ok", "service": "STRING_BOT"}')

    def log_message(self, format, *args):
        return

def run_web_server():
    port = int(os.getenv("PORT", 8080))
    try:
        server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
        print(f"⬤ Web server started on port {port} for Render/Railway health check...")
        server.serve_forever()
    except Exception as e:
        print(f"⬤ Web server error: {e}")

StartTime = time.time()
app = Client(
    "Anonymous",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    in_memory=True,
    plugins=dict(root="ROYEDITX"),
)

def start_bot_with_retry():
    while True:
        try:
            print("⬤ sᴛᴀʀᴛᴇᴅ ʏᴏᴜʀ ʙᴏᴛ...♥︎")
            app.start()
            uname = app.get_me().username
            print(f"⬤ @{uname} sᴛᴀʀᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ...🏵️")
            idle()
            app.stop()
            print("⬤ ʙᴏᴛ sᴛᴏᴘᴇᴅ...🪴")
            break
        except FloodWait as e:
            wait_time = int(e.value)
            print(f"⬤ Telegram FloodWait: Waiting {wait_time} seconds (~{round(wait_time/60, 1)} minutes) before retrying...")
            time.sleep(wait_time + 5)
        except (ApiIdInvalid, ApiIdPublishedFlood):
            logging.error("⬤ ʏᴏᴜʀ API_ID/API_HASH ɪs ɴᴏᴛ ᴠᴀʟɪᴅ...🌺")
            break
        except AccessTokenInvalid:
            logging.error("⬤ ʏᴏᴜʀ BOT_TOKEN ɪs ɴᴏᴛ ᴠᴀʟɪᴅ...🌸")
            break
        except Exception as e:
            logging.error(f"⬤ Bot error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    web_thread = threading.Thread(target=run_web_server, daemon=True)
    web_thread.start()

    start_bot_with_retry()

    # Keep process alive so web server thread stays active for Render health check
    while True:
        time.sleep(3600)
