import struct
import time
import asyncio
from serialReader import telemetry_queue
from decoder import crc16_ccitt, STRUCT_FORMAT, PACKET_SIZE

HEADER = 0xA5A5

async def simulator_task():
    packet_id = 0
    print("Telemetry Simulator Started...")

    while True:
        # Example telemetry (change as you want)
        alt = 100.0 + (packet_id % 50)   # simulate altitude changing
        vel = 5.0 + (packet_id % 5)      # simulate velocity
        ax, ay, az = 10, -10, 980        # mg
        gx, gy, gz = 100, -200, 5        # deg/s * 100
        battery = 3700
        gps_lat = 12.9354
        gps_lon = 77.6789
        gps_alt = 900.0
        pitch, yaw, roll = 100, -50, 30

        # Build payload (without CRC)
        payload = struct.pack(
            STRUCT_FORMAT,
            HEADER,
            packet_id,
            int(time.time() * 1000) & 0xFFFFFFFF,  # timestamp_ms
            alt,
            vel,
            ax, ay, az,
            gx, gy, gz,
            battery,
            3,  # state
            gps_lat,
            gps_lon,
            gps_alt,
            pitch,
            yaw,
            roll
        )

        # Compute CRC
        crc = crc16_ccitt(payload)
        crc_bytes = crc.to_bytes(2, "little")

        # Final packet of 50 bytes
        packet = payload + crc_bytes

        # Decode packet (simulate receiving it)
        from decoder import decode_packet
        decoded = decode_packet(packet)

        # Send into WebSocket queue
        await telemetry_queue.put(decoded)

        print("SIM PACKET:", decoded)

        packet_id = (packet_id + 1) % 256
        await asyncio.sleep(0.05)  # 20 Hz update rate
