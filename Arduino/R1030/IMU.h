#ifndef IMU_h
#define IMU_h
#include <Arduino.h>
#include "LSM6DS3.h"
#include "Wire.h"

class IMU : public LSM6DS3 {
public:
  IMU(uint8_t busType, uint8_t address);
  float GyroX();
  float GyroY();
  float GyroZ();
  float AccelX();
  float AccelY();
  float AccelZ();
  void printGyroInfo();
  void printAccelInfo();
  bool IsUpsideDown();
  class IMU_Orientation {
  private:
    bool state;
    bool lastState = false;
    bool value = false;
    unsigned long debounceDelay;
    unsigned long lastDebounceTime = 0;
  public:
    bool Orientation(float Reading, float MinThreshold, float MaxThreshold, int Delay);
  };
};

#endif