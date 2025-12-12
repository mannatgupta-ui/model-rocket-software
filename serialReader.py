import serial
import threading
from decoder import decode_packet
import asyncio

HEADER = b'\xA5\xA5'
PACKET_SIZE = 50
PORT = "COM5"
BAUD = 115200

telemetry_queue = asyncio.Queue()

def serial_thread():
    ser = serial.Serial(PORT, BAUD, timeout=0.01)
    buffer = bytearray()

    while True:
        incoming = ser.read(1024)
        if incoming:
            buffer.extend(incoming)

        idx = buffer.find(HEADER)
        if idx == -1:
            continue

        if len(buffer) < idx + PACKET_SIZE:
            continue

        packet = bytes(buffer[idx: idx + PACKET_SIZE])
        del buffer[: idx + PACKET_SIZE]

        try:
            decoded = decode_packet(packet)
            asyncio.run_coroutine_threadsafe(telemetry_queue.put(decoded), asyncio.get_event_loop())
        except:
            continue
