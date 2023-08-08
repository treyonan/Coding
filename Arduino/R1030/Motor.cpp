#include "Motor.h"

void Motor::Arm(int signalLevel, int delayTime) {
  writeMicroseconds(signalLevel);  // send "stop" signal to Motor ESC
  delay(delayTime);                // delay to allow the Motor ESC to recognize the stopped signal
}
void Motor::Resume(int signalLevel) {
  writeMicroseconds(signalLevel);
}
