from websocket import WebSocketApp
from queue import Queue
import threading
import json


class EarthquakeWebSocketClient:
    def __init__(self,emsc_websocket_url):
        self.url = emsc_websocket_url
        self.queue = Queue()
        self.ws = None
        self.thread = None
        self.running = False
        

    def on_open(self,ws):
        print("Connected to Earthquake WebSocket")

    def on_message(self,ws,message):
        try:
            data = json.loads(message)
            # Received data  load into queue 
            self.queue.put(data)

        except json.JSONDecodeError:
            print("Invalid JSON recevied",message)

    def on_error(self,ws,error):
        print("Websocket Error:",error)

    def on_close(self,ws,close_status_code,close_msg):
        print("WebSocket Connection Closed")
        self.running = False

    def _run(self):
        self.ws = WebSocketApp(
            url=self.url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            
        )
        self.ws.run_forever()

    def stream(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(
                target=self._run,
                daemon=True
            )

            self.thread.start()
        while self.running:
            earthquake = self.queue.get()
            yield earthquake

    def close(self):
        self.running = False
        if self.ws:
            self.ws.close()
        print("Websocket client stopped")