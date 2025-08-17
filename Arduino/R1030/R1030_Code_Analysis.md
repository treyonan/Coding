# R1030 Combat Robot - Code Analysis

## Overview
This document provides a comprehensive analysis of the R1030 combat robot Arduino project. The system implements a sophisticated control architecture with custom library extensions for competitive robotics applications.

## Project Structure
```
R1030/
├── R1030.ino          # Main Arduino sketch
├── Channel.h/.cpp     # RC receiver interface (extends IBusBM)
├── Motor.h/.cpp       # ESC control with ramping (extends Servo)
├── IMU.h/.cpp         # Inertial measurement (extends LSM6DS3)
├── Drive.h/.cpp       # Locomotion control system
├── Timer.h/.cpp       # Non-blocking timing operations
├── PID.h/.cpp         # Control system feedback
└── ReadMe.adoc        # Project documentation
```

## Core Architecture

### 1. Channel Class (extends IBusBM)
**File**: `Channel.h` (lines 6-21), `Channel.cpp`

**Purpose**: RC receiver interface for remote control communication

**Key Features**:
- Handles 8-channel IBUS protocol communication via `Serial1`
- Maps raw PWM signals (1000-2000μs) to scaled values with deadband zones
- Configurable per-channel scaling, cutoff points, and scale factors

**Channel Assignments** (from `R1030.ino:48-56`):
- Channel 0: Right joystick left/right (right=2000, left=1000)
- Channel 1: Right joystick up/down (up=2000, down=1000)
- Channel 2: Left joystick up/down (up=2000, down=1000)
- Channel 3: Left joystick left/right (right=2000, left=1000)
- Channel 4: Not used
- Channel 5: Front button/calibration (pressed=2000, released=1000)
- Channel 6: Switch A - Weapon control (up=1000, down=2000)
- Channel 7: Switch B - Failsafe signal (up=1000, down=2000)

**Key Methods**:
- `ReadChannels()`: Reads all 8 channels from receiver
- `Map(channelNum)`: Scales raw values with deadband logic
- `Init()`: Configures channel parameters

### 2. Motor Class (extends Servo)
**File**: `Motor.h` (lines 7-27), `Motor.cpp`

**Purpose**: ESC control with smooth ramping functionality

**State Machine**:
```
STOPPED → RAMP_UP → RUNNING → RAMP_DOWN → STOPPED
```

**Key Features**:
- Smooth acceleration/deceleration to prevent mechanical damage
- Dynamic ramp timing based on current motor state
- Safety ramping for weapon motor (3s up, 1s down)
- State transitions handle direction changes mid-ramp

**Key Methods**:
- `Output(signalLevel, MotorName)`: Direct ESC control
- `RampMotor(Direction, PT, MotorName)`: Smooth ramping control
- `PrintMotorInfo()`: Debug information

### 3. IMU Class (extends LSM6DS3)
**File**: `IMU.h` (lines 7-56), `IMU.cpp`

**Purpose**: Inertial measurement for orientation detection

**Key Features**:
- Weighted averaging filter (99.9% previous, 0.1% new reading)
- Upside-down detection for drive direction correction
- Nested classes for orientation debouncing and signal averaging
- Real-time gyroscope and accelerometer data processing

**Nested Classes**:
- `IMU_Orientation`: Debounced orientation state detection
- `Average`: Weighted averaging for sensor smoothing

**Key Methods**:
- `GyroX/Y/Z()`: Filtered gyroscope readings
- `AccelX/Y/Z()`: Filtered accelerometer readings
- `IsUpsideDown()`: Robot orientation detection

### 4. Drive Class
**File**: `Drive.h` (lines 8-51), `Drive.cpp`

**Purpose**: Locomotion control system

**Key Features**:
- Dual drive modes: Tank drive and Arcade drive
- Automatic orientation compensation (upside-down operation)
- Calibration system for drive motor neutral points
- PID control integration for stability
- Button-based calibration with timeout protection

**Key Methods**:
- `Init()`: Initialize drive system
- `TankDrive(Direction)`: Traditional tank steering
- `ArcadeDrive(Direction)`: Single-stick driving
- `StartCalibration()`, `StopCalibration()`: Calibration control
- `Calibrated()`: Calibration status check

### 5. Timer Class
**File**: `Timer.h` (lines 5-17), `Timer.cpp`

**Purpose**: Non-blocking timing operations

**Key Features**:
- Industrial timer function (Enable/Timer/Done pattern)
- Millisecond-based timing with reset capability
- Used for motor ramping, RX monitoring, and calibration timeouts

**Key Methods**:
- `Init(PT)`: Set timer preset time
- `DN()`: Check if timer is done
- `RES()`: Reset timer

### 6. PID Class
**File**: `PID.h` (lines 4-30), `PID.cpp`

**Purpose**: Control system feedback

**Key Features**:
- Standard PID controller implementation
- Configurable gains (Kp, Ki, Kd)
- Output limiting and integral reset functionality

## Safety Systems

### Receiver Monitoring
**Implementation**: `R1030.ino:126-140`
- Continuously monitors RC signal reception via `cnt_rec` counter
- Declares disconnection after 5 consecutive failed checks (500ms)
- Immediately shuts down all motors on signal loss

### Motor Safety
**Implementation**: `R1030.ino:120-125`, `141-146`
- ESC arming sequence (1.5s neutral, 1.0s weapon minimum)
- Weapon motor ramp limiting prevents sudden starts
- Emergency shutdown function zeros all outputs

### Calibration Protection
**Implementation**: `R1030.ino:80-100`
- 20-second timeout prevents infinite calibration loops
- Button state monitoring prevents accidental activation

## Operational Flow

### Initialization (`setup()` - lines 148-181)
1. Configure 8 RC channels with scaling parameters
2. Initialize IMU with I2C communication (address 0x6A)
3. Arm ESCs with proper startup sequence
4. Enable receiver monitoring timer

### Main Loop (`loop()` - lines 182-207)
1. **Standby Mode**: Waits for calibration button activation
2. **Active Mode**: Enters main control loop with:
   - Continuous channel reading
   - Optional drive calibration
   - Orientation-aware drive control (`RunDriveMotors()`)
   - Weapon motor management (`RunWeaponMotor()`)
   - Receiver disconnection monitoring

### Control Logic

#### Drive Control (`RunDriveMotors()` - lines 101-111)
- Checks IMU orientation via `IsUpsideDown()`
- Sets direction flag (0=right-side-up, 1=upside-down)
- Uses arcade drive mode with automatic compensation

#### Weapon Control (`RunWeaponMotor()` - lines 112-119)
- Binary on/off control via channel 6
- Smooth ramping (3s up, 1s down) for safety
- Prevents sudden weapon activation

## Technical Specifications

- **Microcontroller**: Arduino-compatible with multiple PWM outputs
- **Communication**: IBUS protocol at 115200 baud
- **Motors**: 3 ESC-controlled motors (2 drive + 1 weapon)
- **Sensors**: LSM6DS3 IMU via I2C (address 0x6A)
- **Control**: 8-channel RC receiver with failsafe
- **Pin Assignments**:
  - Motor A: Pin 9
  - Motor B: Pin 8
  - Weapon: Pin 10

## Key Design Patterns

1. **Inheritance-based Extensions**: All major classes extend Arduino libraries
2. **State Machine Control**: Motor ramping uses explicit state management
3. **Safety-First Design**: Multiple failsafe mechanisms and timeouts
4. **Real-time Processing**: Non-blocking timers and continuous monitoring
5. **Modular Architecture**: Separated concerns across multiple classes

## Areas for Future Enhancement

1. **Telemetry**: Add wireless data logging capabilities
2. **Advanced Control**: Implement more sophisticated drive algorithms
3. **Diagnostics**: Enhanced debugging and system health monitoring
4. **Configuration**: Runtime parameter adjustment via RC channels
5. **Autonomous Features**: Basic self-righting or obstacle avoidance

## Notes

- This is a defensive robotics project for competitive combat robotics
- All safety systems are designed to prevent damage and ensure operator safety
- The code demonstrates advanced Arduino programming techniques
- The modular design makes the system easily maintainable and extensible