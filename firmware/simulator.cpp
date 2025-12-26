#include "includes.h"

void simulateSensors() {
    static uint32_t t = 0;

    alt_baro = 100 + 0.05 * t;
    velocity = 5.0;

    ax = 10; ay = -10; az = 980;
    gx = 100; gy = -200; gz = 5;

    gps_lat = 12.9354;
    gps_lon = 77.6789;
    gps_alt = 900.0;

    t++;
}
