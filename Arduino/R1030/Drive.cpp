#include "Drive.h"

Drive::Drive(Motor& DriveMotorA, Motor& DriveMotorB, int MotorAChannel, int MotorBChannel, int CalibrateChannel, Channel& Channels, IMU& myIMU)
  : _DriveMotorA(DriveMotorA), _DriveMotorB(DriveMotorB), _MotorAChannel(MotorAChannel), _MotorBChannel(MotorBChannel), _CalibrateChannel(CalibrateChannel), _Channels(Channels), _myIMU(myIMU) {
  _DriveMotorA_CutOff = _Channels.CutOff[_MotorAChannel];
  _DriveMotorB_CutOff = _Channels.CutOff[_MotorBChannel];
}
void Drive::Init() {
  _PID.SetCV(_Channels.ScaledMin[_MotorAChannel], _Channels.ScaledMax[_MotorAChannel]);
  _PID.SetGain(1.00, 0, 0);
}
bool Drive::StartCalibration() {  // 3 second button press or more
  _Calibrate.ButtonState = _Channels.Reading[_CalibrateChannel]; 
  if (_Calibrate.ButtonState == 2000 && _Calibrate.ButtonState != _Calibrate.ButtonPreviousState) {
    _Calibrate.ButtonOnStartTime = millis();    
  }
  _Calibrate.ButtonPreviousState = _Calibrate.ButtonState;  

  if (_Calibrate.ButtonState == 2000 && (millis() - _Calibrate.ButtonOnStartTime) > 3000) {    
    return true;
  } else {
    return false;
  }
}

bool Drive::StopCalibration() {  // 500 ms button press or less
  _Calibrate.ButtonState = _Channels.Reading[_CalibrateChannel];  
  if (_Calibrate.ButtonState == 2000 && _Calibrate.ButtonState != _Calibrate.ButtonPreviousState) {
    _Calibrate.ButtonOnStartTime = millis();    
    _Calibrate.ButtonPressed = true;
  }
  if (_Calibrate.ButtonState == 1000 && _Calibrate.ButtonState != _Calibrate.ButtonPreviousState) {    
    _Calibrate.ButtonOffStartTime = millis();
  }
  _Calibrate.ButtonPreviousState = _Calibrate.ButtonState;
  if ((_Calibrate.ButtonOffStartTime - _Calibrate.ButtonOnStartTime) <= 500 && _Calibrate.ButtonPressed) {  
    _Calibrate.ButtonPressed = false;  
    return true;
  } else {
    return false;
  }
}

bool Drive::Calibrated() {
  Serial.println("Calibrating");
  return _Calibrated;
}
void Drive::ResetCalibration() {  // Set process variable minimum and maximum for PID loop based on current orientation
  bandwidth = 10;
  sp = _myIMU.GyroX();           // CHECK FOR CORRECT ONE
  pvMin = sp - (bandwidth / 2);  // CHECK MATH
  pvMax = sp + (bandwidth / 2);
  _PID.SetSP(sp);
  _PID.SetPV(pvMin, pvMax);
  _PID.ResetIntegral();
  _Calibrated = false;
  Serial.print("Reset calibration");
}
void Drive::TankDrive() {
  if (_myIMU.IsUpsideDown() == true) {
    _DriveMotorA.Resume(_DriveMotorA_CutOff);
  } else {
    _DriveMotorA.Resume(_Channels.Map(_MotorAChannel));
    _DriveMotorB.Resume(_Channels.Map(_MotorBChannel));
  }
}
