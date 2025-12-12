import struct
import binascii

PACKET_SIZE = 50
STRUCT_FORMAT = '<H B I f f h h h h h h H B f f f h h h'
STRUCT_FORMAT = STRUCT_FORMAT.replace(' ', '')

def crc16_ccitt(data: bytes, crc: int = 0xFFFF) -> int:
    return binascii.crc_hqx(data, crc) & 0xFFFF

def decode_packet(packet: bytes) -> dict:

    if len(packet) != PACKET_SIZE:
        raise ValueError(f"Invalid packet length: {len(packet)} expected {PACKET_SIZE}")

    payload = packet[:-2]
    crc_recv = int.from_bytes(packet[-2:], 'little')

    crc_calc = crc16_ccitt(payload)
    if crc_calc != crc_recv:
        raise ValueError(f"CRC mismatch: calc=0x{crc_calc:04X} recv=0x{crc_recv:04X}")

    fields = struct.unpack(STRUCT_FORMAT, payload)

    decoded = {
        "header":       fields[0],
        "packet_id":    fields[1],
        "timestamp_ms": fields[2],
        "alt_baro":     fields[3],
        "velocity":     fields[4],
        "accel_x":      fields[5],
        "accel_y":      fields[6],
        "accel_z":      fields[7],
        "gyro_x":       fields[8],
        "gyro_y":       fields[9],
        "gyro_z":       fields[10],
        "battery_mv":   fields[11],
        "state":        fields[12],
        "gps_lat":      fields[13],
        "gps_lon":      fields[14],
        "gps_alt":      fields[15],
        "pitch":        fields[16],
        "yaw":          fields[17],
        "roll":         fields[18],
        "crc16":        crc_recv
    }

    return decoded
