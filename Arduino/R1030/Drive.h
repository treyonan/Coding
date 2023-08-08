#ifndef Drive_h
#define Drive_h
#include "Channel.h"
#include "Motor.h"
#include "IMU.h"
#include "PID.h"

class Drive {
private:
  struct Calibrate {
    int ButtonState;
    int ButtonPreviousState;    
    unsigned long ButtonOnStartTime;
    unsigned long ButtonOffStartTime;
    bool ButtonPressed;        
  };
  Calibrate _Calibrate;
  Motor& _DriveMotorA;
  Motor& _DriveMotorB;
  int _MotorAChannel;
  int _MotorBChannel;
  int _CalibrateChannel;
  Channel& _Channels;
  IMU& _myIMU;
  float _DriveMotorA_CutOff;
  float _DriveMotorB_CutOff;
  bool _Calibrated;
  PID _PID;
  float bandwidth;
  float sp;
  float pvMin;
  float pvMax;
public:
  Drive(Motor& DriveMotorA, Motor& DriveMotorB, int MotorAChannel, int MotorBChannel, int CalibrateChannel, Channel& Channels, IMU& myIMU);
  void Init();
  bool StartCalibration();
  bool StopCalibration();
  bool Calibrated();
  void ResetCalibration();
  void TankDrive();
};

#endif