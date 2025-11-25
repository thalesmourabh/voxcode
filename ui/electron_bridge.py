import os
import threading
import asyncio
import json
import websockets

class ElectronBridge:
    """Bridge between Python backend and Electron UI.
    Starts a WebSocket server that the Electron app connects to.
    Provides simple methods to control the floating window.
    """
    def __init__(self, host='localhost', port=8765):
        self.host = host
        self.port = port
        self.clients = set()
        self.server = None
        self._start_server()

    def _start_server(self):
        # Start the event loop in a separate thread
        threading.Thread(target=self._run_event_loop, daemon=True).start()

    def _run_event_loop(self):
        # Create and set a new event loop for this thread
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        async def handler(ws):
            self.clients.add(ws)
            try:
                async for _ in ws:
                    pass  # we don't expect messages from Electron
            finally:
                self.clients.remove(ws)
        
        async def start_server():
            async with websockets.serve(handler, self.host, self.port):
                await asyncio.Future()  # run forever
        
        # Run the server
        self.loop.run_until_complete(start_server())

    async def _broadcast(self, message):
        if self.clients:
            # Create tasks for all clients
            tasks = [asyncio.create_task(client.send(message)) for client in self.clients]
            if tasks:
                await asyncio.wait(tasks)

    def _send(self, action, payload=None):
        msg = json.dumps({"action": action, "payload": payload})
        print(f"🔵 WebSocket send: {action}", flush=True)  # DEBUG
        # Schedule broadcast in the bridge thread loop
        if hasattr(self, 'loop') and self.loop.is_running():
            asyncio.run_coroutine_threadsafe(self._broadcast(msg), self.loop)
        else:
            print(f"⚠️ WebSocket loop not running!", flush=True)  # DEBUG

    # Public API used by VoxCodeApp
    def show_recording(self, auto_stop=True):
        print(f"📞 show_recording called", flush=True)  # DEBUG
        self._send('show-recording', {'auto_stop': auto_stop})

    def show_processing(self):
        print(f"📞 show_processing called", flush=True)  # DEBUG
        self._send('show-processing')

    def show_success(self, text):
        print(f"📞 show_success called: {text[:50]}...", flush=True)  # DEBUG
        self._send('show-success', {'text': text})

    def hide(self):
        print(f"📞 hide called", flush=True)  # DEBUG
        self._send('hide')

    def show_error(self, message):
        """Send an error message to the Electron UI."""
        print(f"📞 show_error called: {message}", flush=True)  # DEBUG
        self._send('show-error', {'message': message})
