import asyncio
import uvicorn
from websocket_server import app           # <-- IMPORTANT
from simulator import simulator_task        # <-- IMPORTANT

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(simulator_task())
    uvicorn.run(app, host="0.0.0.0", port=8000)
