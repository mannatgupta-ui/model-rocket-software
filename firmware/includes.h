#pragma once

#include <Arduino.h>
#include <Wire.h>

#include <Adafruit_BMP280.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <TinyGPSPlus.h>

#include "telemetry_packets.h"
#include "crc16_ccitt.h"
#include "sensors.h"
#include "simulator.h"
