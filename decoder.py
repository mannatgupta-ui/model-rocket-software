import struct
import binascii

# ---------------- CRC ---------------- 
def crc16_ccitt(data: bytes, crc: int = 0xFFFF) -> int:
    return binascii.crc_hqx(data, crc) & 0xFFFF


# ---------------- STRUCTS ----------------
# little-endian

FMT_PACKET_A = '<H B B I f f h h h h h h'   # 30 bytes
FMT_PACKET_B = '<H B B I f f f h h h H B'   # 30 bytes

SIZE_PACKET = 32  # payload(30) + crc(2)


# ---------------- ENCODERS ----------------
def encode_packet_a(
    header, packet_id, timestamp,
    alt_baro, velocity,
    ax, ay, az,
    gx, gy, gz
) -> bytes:
    payload = struct.pack(
        FMT_PACKET_A,
        header,
        packet_id,
        0x01,              # packet_type
        timestamp,
        alt_baro,
        velocity,
        ax, ay, az,
        gx, gy, gz
    )
    crc = crc16_ccitt(payload)
    return payload + crc.to_bytes(2, 'little')


def encode_packet_b(
    header, packet_id, timestamp,
    lat, lon, alt,
    pitch, yaw, roll,
    battery_mv, state
) -> bytes:
    payload = struct.pack(
        FMT_PACKET_B,
        header,
        packet_id,
        0x02,              # packet_type
        timestamp,
        lat, lon, alt,
        pitch, yaw, roll,
        battery_mv,
        state
    )
    crc = crc16_ccitt(payload)
    return payload + crc.to_bytes(2, 'little')


# ---------------- DECODER ----------------
def decode_packet(packet: bytes) -> dict:
    if len(packet) != SIZE_PACKET:
        raise ValueError("Invalid packet length")

    payload = packet[:-2]
    crc_recv = int.from_bytes(packet[-2:], 'little')

    if crc16_ccitt(payload) != crc_recv:
        raise ValueError("CRC mismatch")

    packet_type = payload[3]

    # ---------- PACKET A ----------
    if packet_type == 0x01:
        f = struct.unpack(FMT_PACKET_A, payload)
        return {
            "header": f[0],
            "packet_id": f[1],
            "packet_type": f[2],
            "timestamp": f[3],
            "alt_baro": f[4],
            "velocity": f[5],
            "accel_x": f[6],
            "accel_y": f[7],
            "accel_z": f[8],
            "gyro_x": f[9],
            "gyro_y": f[10],
            "gyro_z": f[11],
            "crc16": crc_recv
        }

    # ---------- PACKET B ----------
    elif packet_type == 0x02:
        f = struct.unpack(FMT_PACKET_B, payload)
        return {
            "header": f[0],
            "packet_id": f[1],
            "packet_type": f[2],
            "timestamp": f[3],
            "gps_lat": f[4],
            "gps_lon": f[5],
            "gps_alt": f[6],
            "pitch": f[7],
            "yaw": f[8],
            "roll": f[9],
            "battery_mv": f[10],
            "state": f[11],
            "crc16": crc_recv
        }

    else:
        raise ValueError("Unknown packet type")
