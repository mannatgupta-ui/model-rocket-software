#include "includes.h"

// ================= SENSOR OBJECTS =================
Adafruit_BMP280 bmp;        // Barometer
Adafruit_MPU6050 mpu;       // IMU
TinyGPSPlus gps;            // GPS parser

// ================= GLOBAL SENSOR VALUES =================
// These variables are declared in sensors.h as extern
// They are UPDATED here and READ by telemetry_send.cpp

float alt_baro = 0.0f;      // meters
float velocity = 0.0f;      // m/s

int16_t ax = 0, ay = 0, az = 0;   // acceleration (scaled)
int16_t gx = 0, gy = 0, gz = 0;   // gyro (scaled)

float gps_lat = 0.0f;
float gps_lon = 0.0f;
float gps_alt = 0.0f;

// ================= ALTITUDE HISTORY (for velocity) =================
static uint32_t lastAltTime = 0;
static float lastAlt = 0.0f;

// ================= INITIALIZE SENSORS =================
bool initSensors() {

    // Start I2C bus
    Wire.begin();

    // ---------- BMP280 ----------
    if (!bmp.begin(0x76)) {
        return false;   // sensor not detected
    }

    bmp.setSampling(
        Adafruit_BMP280::MODE_NORMAL,
        Adafruit_BMP280::SAMPLING_X2,     // temperature oversampling
        Adafruit_BMP280::SAMPLING_X16,    // pressure oversampling
        Adafruit_BMP280::FILTER_X16,      // noise filter
        Adafruit_BMP280::STANDBY_MS_0_5   // fast update
    );

    // ---------- MPU6050 ----------
    if (!mpu.begin()) {
        return false;   // sensor not detected
    }

    mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
    mpu.setGyroRange(MPU6050_RANGE_500_DEG);
    mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

    // ---------- Initial altitude reference ----------
    lastAltTime = millis();
    lastAlt = bmp.readAltitude(1013.25);   // sea-level pressure

    return true;   // all sensors OK
}

// ================= READ BAROMETER =================
void readBMP() {

    uint32_t now = millis();
    float currentAlt = bmp.readAltitude(1013.25);

    float dt = (now - lastAltTime) / 1000.0f;  // seconds
    if (dt > 0.0f) {
        velocity = (currentAlt - lastAlt) / dt;
    }

    alt_baro = currentAlt;
    lastAlt = currentAlt;
    lastAltTime = now;
}

// ================= READ IMU =================
void readMPU() {

    sensors_event_t accel, gyro, temp;
    mpu.getEvent(&accel, &gyro, &temp);

    // Scale to int16 for telemetry packet
    ax = (int16_t)(accel.acceleration.x * 100);
    ay = (int16_t)(accel.acceleration.y * 100);
    az = (int16_t)(accel.acceleration.z * 100);

    gx = (int16_t)(gyro.gyro.x * 100);
    gy = (int16_t)(gyro.gyro.y * 100);
    gz = (int16_t)(gyro.gyro.z * 100);
}

// ================= READ GPS =================
void readGPS() {

    // Read incoming GPS bytes from UART
    while (Serial1.available()) {
        gps.encode(Serial1.read());
    }

    // Update values only if valid
    if (gps.location.isValid()) {
        gps_lat = gps.location.lat();
        gps_lon = gps.location.lng();
    }

    if (gps.altitude.isValid()) {
        gps_alt = gps.altitude.meters();
    }
}
