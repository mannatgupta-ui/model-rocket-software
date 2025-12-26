import time
import asyncio
from serialReader import telemetry_queue
from decoder import encode_packet_a, encode_packet_b, decode_packet

HEADER = 0xA5A5

async def simulator_task():
    packet_id = 0
    print("Telemetry Simulator Started...")

    while True:
        ts = int(time.time() * 1000) & 0xFFFFFFFF

        # -------- PACKET A (FAST) --------
        pkt_a = encode_packet_a(
            HEADER,
            packet_id,
            ts,
            alt_baro=100.0 + (packet_id % 50),
            velocity=5.0 + (packet_id % 5),
            ax=10, ay=-10, az=980,
            gx=100, gy=-200, gz=5
        )

        decoded_a = decode_packet(pkt_a)
        await telemetry_queue.put(decoded_a)

        # -------- PACKET B (SLOW) --------
        pkt_b = encode_packet_b(
            HEADER,
            packet_id,
            ts,
            lat=12.9354,
            lon=77.6789,
            alt=900.0,
            pitch=100,
            yaw=-50,
            roll=30,
            battery_mv=3700,
            state=3
        )

        decoded_b = decode_packet(pkt_b)
        await telemetry_queue.put(decoded_b)

        packet_id = (packet_id + 1) % 256
        await asyncio.sleep(0.05)
