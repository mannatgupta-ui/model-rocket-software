from fastapi import FastAPI, WebSocket
from serialReader import telemetry_queue

app = FastAPI()

@app.websocket("/ws/telemetry")
async def telemetry_ws(websocket: WebSocket):
    await websocket.accept()
    print("Client connected")

    while True:
        data = await telemetry_queue.get()
        await websocket.send_json(data)
