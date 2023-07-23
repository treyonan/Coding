#ifndef Motor_h
#define Motor_h
#include <Arduino.h>
#include <Servo.h>

class Motor : public Servo {
public:
  void Arm(int signalLevel, int delayTime);
  void Resume(int signalLevel);
};

#endif