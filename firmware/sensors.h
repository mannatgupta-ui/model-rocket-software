#pragma once

extern float alt_baro, velocity;
extern int16_t ax, ay, az, gx, gy, gz;
extern float gps_lat, gps_lon, gps_alt;

bool initSensors();
void readBMP();
void readMPU();
void readGPS();
