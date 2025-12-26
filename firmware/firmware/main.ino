#include "includes.h"

// 1 = simulation, 0 = real sensors
#define USE_SIMULATION 1

uint8_t packet_id = 0;
uint32_t slowCounter = 0;

void setup() {
    Serial.begin(115200);                         // Telemetry output
    Serial1.begin(9600, SERIAL_8N1, 16, 17);      // GPS UART

#if !USE_SIMULATION
    // Fail-safe: stop program if sensors are not detected
    if (!initSensors()) {
        while (1);   // infinite halt
    }
#endif
}

void loop() {

#if USE_SIMULATION
    simulateSensors();    // fake data
#else
    readBMP();
    readMPU();
    readGPS();            // real sensors
#endif

    // FAST packet (50 Hz)
    sendPacketA(Serial, packet_id);

    // SLOW packet (5 Hz)
    if (++slowCounter >= 10) {
        sendPacketB(Serial, packet_id);
        slowCounter = 0;
    }

    packet_id++;
    delay(20);
}
