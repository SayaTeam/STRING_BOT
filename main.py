import config
import time
import logging
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from pyrogram import Client, idle
from pyromod import listen  # type: ignore
from pyrogram.errors import ApiIdInvalid, ApiIdPublishedFlood, AccessTokenInvalid

logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
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

if __name__ == "__main__":
    web_thread = threading.Thread(target=run_web_server, daemon=True)
    web_thread.start()

    print("⬤ sᴛᴀʀᴛᴇᴅ ʏᴏᴜʀ ʙᴏᴛ...♥︎")
    try:
        app.start()
    except (ApiIdInvalid, ApiIdPublishedFlood):
        raise Exception("⬤ ʏᴏᴜʀ API_ID/API_HASH ɪs ɴᴏᴛ ᴠᴀʟɪᴅ...🌺")
    except AccessTokenInvalid:
        raise Exception("⬤ ʏᴏᴜʀ BOT_TOKEN ɪs ɴᴏᴛ ᴠᴀʟɪᴅ...🌸")
    uname = app.get_me().username
    print(f"⬤ @{uname} sᴛᴀʀᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ...🏵️")
    idle()
    app.stop()
    print("⬤ ʙᴏᴛ sᴛᴏᴘᴇᴅ...🪴")
