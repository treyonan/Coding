#include "IMU.h"

IMU::IMU(uint8_t busType, uint8_t address)
  : LSM6DS3(busType, address) {
}
float IMU::GyroX() {
  float _GyroX = readFloatGyroX();
  return _GyroX;
}
float IMU::GyroY() {
  float _GyroY = readFloatGyroY();
  return _GyroY;
}
float IMU::GyroZ() {
  float _GyroZ = readFloatGyroZ();
  return _GyroZ;
}
float IMU::AccelX() {
  float _AccelX = readFloatAccelX();
  return _AccelX;
}
float IMU::AccelY() {
  float _AccelY = readFloatAccelY();
  return _AccelY;
}
float IMU::AccelZ() {
  float _AccelZ = readFloatAccelZ();
  return _AccelZ;
}
void IMU::printGyroInfo() {
  Serial.print(" X1 = ");
  Serial.print(GyroX(), 4);
  Serial.print(" Y1 = ");
  Serial.print(GyroY(), 4);
  Serial.print(" Z1 = ");
  Serial.println(GyroZ(), 4);
}
void IMU::printAccelInfo() {
  Serial.print(" X1 = ");
  Serial.print(AccelX(), 4);
  Serial.print(" Y1 = ");
  Serial.print(AccelY(), 4);
  Serial.print(" Z1 = ");
  Serial.println(AccelZ(), 4);
}

bool IMU::IMU_Orientation::Orientation(float Reading, float MinThreshold, float MaxThreshold, int Delay) {
  value = false;
  if (Reading >= MinThreshold && Reading <= MaxThreshold) {
    state = true;
  } else {
    state = false;
  }
  if (state != lastState) {
    lastDebounceTime = millis();
  }
  if ((millis() - lastDebounceTime) > Delay) {
    value = state;
  }
  lastState = state;
  return value;
}

IMU::IMU_Orientation Z;

bool IMU::IsUpsideDown() {
  float Reading = IMU::AccelZ();
  return Z.Orientation(Reading, -0.5, -0.25, 500);
}
