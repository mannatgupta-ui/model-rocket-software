#include "includes.h"

// This file ONLY encodes packets and sends them

void sendPacketA(HardwareSerial &ser, uint8_t pid) {
    PacketA p = {
        HEADER, pid, 0x01, millis(),
        alt_baro, velocity,
        ax, ay, az,
        gx, gy, gz
    };

    uint8_t buf[PACKET_SIZE];
    memcpy(buf, &p, sizeof(PacketA));

    uint16_t crc = crc16_ccitt(buf, sizeof(PacketA));
    buf[30] = crc & 0xFF;
    buf[31] = crc >> 8;

    ser.write(buf, PACKET_SIZE);
}

void sendPacketB(HardwareSerial &ser, uint8_t pid) {
    PacketB p = {
        HEADER, pid, 0x02, millis(),
        gps_lat, gps_lon, gps_alt,
        0, 0, 0,
        3700,
        0
    };

    uint8_t buf[PACKET_SIZE];
    memcpy(buf, &p, sizeof(PacketB));

    uint16_t crc = crc16_ccitt(buf, sizeof(PacketB));
    buf[30] = crc & 0xFF;
    buf[31] = crc >> 8;

    ser.write(buf, PACKET_SIZE);
}
