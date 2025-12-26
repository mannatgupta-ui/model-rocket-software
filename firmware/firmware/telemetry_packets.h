#pragma once
#include <stdint.h>

#define HEADER 0xA5A5
#define PACKET_SIZE 32

#pragma pack(push,1)

struct PacketA {
    uint16_t header;
    uint8_t packet_id;
    uint8_t packet_type;
    uint32_t timestamp;
    float alt_baro;
    float velocity;
    int16_t ax, ay, az;
    int16_t gx, gy, gz;
};

struct PacketB {
    uint16_t header;
    uint8_t packet_id;
    uint8_t packet_type;
    uint32_t timestamp;
    float lat, lon, alt;
    int16_t pitch, yaw, roll;
    uint16_t battery_mv;
    uint8_t reserved;
};

#pragma pack(pop)
