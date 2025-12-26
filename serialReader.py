import serial
import asyncio
from decoder import decode_packet

HEADER = b'\xA5\xA5'
PACKET_SIZE = 32   # 🔥 FIXED
PORT = "COM5"
BAUD = 115200

telemetry_queue = asyncio.Queue()

def serial_thread():
    ser = serial.Serial(PORT, BAUD, timeout=0.01)
    buffer = bytearray()
    loop = asyncio.get_event_loop()

    while True:
        buffer.extend(ser.read(1024))

        while True:
            idx = buffer.find(HEADER)
            if idx == -1:
                buffer.clear()
                break

            if len(buffer) < idx + PACKET_SIZE:
                break

            packet = bytes(buffer[idx: idx + PACKET_SIZE])
            del buffer[: idx + PACKET_SIZE]

            try:
                decoded = decode_packet(packet)
                asyncio.run_coroutine_threadsafe(
                    telemetry_queue.put(decoded),
                    loop
                )
            except:
                continue
