#include "Channel.h"
#include "Motor.h"
#include "IMU.h"
#include "Drive.h"

// This item toggles debugging behaviour on or off.
// Comment the item out to disable debugging messages.
/*
#define debug
// Set up debugging behaviours
#ifdef debug
#define debug_print(x) Serial.print (x)
#define debug_println(x) Serial.println (x)
#else
#define debug_print(x)
#define debug_println(x)
#endif
*/

#define MotorAChannel 1
#define MotorAPin 9
#define MotorBChannel 2
#define MotorBPin 8  // CHECK
#define CalibrateChannel 5
#define WeaponChannel 6
#define WeaponPin 10  // CHECK

Channel Channels;
Motor WeaponMotor;
Motor DriveMotorA;
Motor DriveMotorB;
IMU myIMU(I2C_MODE, 0x6A);  //I2C device address 0x6A

Drive Drive(DriveMotorA, DriveMotorB, MotorAChannel, MotorBChannel, CalibrateChannel, Channels, myIMU);

float _Reading[8];

void ReadChannels() {
  // Channel 0 - Right joystick left/right, right = 2000, left = 1000
  // Channel 1 - Right joystick up/down, up = 2000, down = 1000
  // Channel 2 - Left joystick up/down, up = 2000, down = 1000
  // Channel 3 - Left joystick left/right, right = 2000, left = 1000
  // Channel 4 - NU
  // Channel 5 - Front button, pressed = 2000, released = 1000
  // Channel 6 - Switch A (Left Switch), up = 1000, middle = cut off value, down = 2000
  // Channel 7 - Switch B (Right Switch), up = 1000, middle = cut off value, down = 2000
  Channels.ReadChannels();
  for (int i = 0; i < 9; i++) {
    _Reading[i] = Channels.Map(i);
  }
#ifdef debug
  debug_print(_Reading[0]);
  debug_print("    ");
  debug_print(_Reading[1]);
  debug_print("    ");
  debug_print(_Reading[2]);
  debug_print("    ");
  debug_print(_Reading[3]);
  debug_print("    ");
  debug_print(_Reading[4]);
  debug_print("    ");
  debug_print(_Reading[5]);
  debug_print("    ");
  debug_print(_Reading[6]);
  debug_print("    ");
  debug_println(_Reading[7]);
  delay(100);
#endif
}

void setup() {

  Serial.begin(115200);
  Channels.begin(Serial1, IBUSBM_NOTIMER);
  Channels.Init(0, 1000, 2000, 1000, 2000, 1475);
  Channels.Init(1, 1000, 2000, 1000, 2000, 1475);
  Channels.Init(2, 1000, 1994, 1000, 2000, 1475);
  Channels.Init(3, 1006, 1991, 1000, 2000, 1475);
  Channels.Init(4, 1000, 2000, 1000, 2000, 1475);
  Channels.Init(5, 1000, 2000, 1000, 2000, 1475);
  Channels.Init(6, 1000, 2000, 1000, 2000, 1475);
  Channels.Init(7, 1000, 2000, 1000, 2000, 1475);

  Drive.Init();

  // Attach and arm Motor ESCs
  DriveMotorA.attach(MotorAPin);
  DriveMotorA.Arm(900, 4000);
  WeaponMotor.attach(WeaponPin);
  WeaponMotor.Arm(900, 4000);

  while (!Serial)
    ;

  //Call .begin() to configure the IMUs

  if (myIMU.begin() != 0) {
    Serial.println("Device error");
  } else {
    Serial.println("Device OK!");
  }
}

void loop() {

  ReadChannels();

  if (Drive.StartCalibration() == true) {
    Drive.ResetCalibration();
    while (!Drive.Calibrated()) {
      ReadChannels();
      if (Drive.StopCalibration() == true) {
        Serial.println("Stop calibration");
        break;
      }
    }
  }

  Drive.TankDrive();
  WeaponMotor.Resume(_Reading[WeaponChannel]);

  delay(10);
}