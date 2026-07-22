Here’s a complete README based on your actual code and current prototype. You can paste it directly into `README.md`.

# Mouve

Mouve is a low-cost, camera-tracked robotic hand prototype that mirrors a user’s finger movements using computer vision, a Raspberry Pi Pico, servo motors, and tendon-style actuation.

The project combines:

* Computer vision using Python, OpenCV, and MediaPipe
* Serial communication between a computer and Raspberry Pi Pico
* MicroPython-based PWM servo control
* A custom mechanical hand with independently actuated fingers

## Goal

The goal of Mouve was to design and build a robotic hand capable of reproducing individual finger movement detected through a webcam.

The project was created as a proof-of-concept for integrating computer vision, embedded programming, electronics, and mechanical design into one functional mechatronics system.

The main objectives were to:

* Detect the movement of each finger using a webcam
* Track hand landmarks using MediaPipe
* Convert tracked finger movement into normalized control values
* Send finger values from a computer to a Raspberry Pi Pico
* Control five servo motors independently using PWM
* Use tendon-style strings to convert servo rotation into finger movement
* Build the system using low-cost and accessible components

## Hardware Used

* Raspberry Pi Pico
* Five servo motors
* Webcam
* External battery pack for servo power
* Breadboard
* Jumper wires
* Custom robotic hand structure
* String-based tendons
* Computer running Python

### Servo Pin Mapping

| Finger | Raspberry Pi Pico Pin |
| ------ | --------------------: |
| Index  |                   GP3 |
| Middle |                   GP2 |
| Ring   |                   GP1 |
| Pinky  |                   GP0 |
| Thumb  |                   GP4 |

## Software Used

* Python
* MicroPython
* OpenCV (`cv2`)
* MediaPipe
* PySerial
* SolidWorks

## How It Works

Mouve uses two connected software programs: a computer-vision tracking program running on a computer and a servo-control program running on the Raspberry Pi Pico.

### 1. Camera Input

OpenCV captures a mirrored webcam feed at a resolution of 1280 × 720.

Before tracking begins, the program displays a five-second countdown that allows the user to place their hand in a preferred starting position.

### 2. Hand Landmark Detection

MediaPipe Hands detects one hand and identifies landmarks including:

* Wrist
* Middle-finger MCP joint
* Thumb tip
* Index fingertip
* Middle fingertip
* Ring fingertip
* Pinky fingertip

The detected landmarks are also drawn and labelled on the live camera feed for visualization and debugging.

### 3. Finger Position Calculation

The distance between each fingertip and the wrist is calculated.

To reduce the effect of the user moving closer to or farther from the camera, each distance is divided by a hand-scale measurement calculated between the wrist and the middle-finger MCP joint.

The thumb is handled separately by measuring the distance between the thumb tip and the middle-finger MCP joint.

At startup, the program records the initial finger positions. Current finger positions are subtracted from these starting values to determine relative finger movement.

### 4. Serial Communication

The computer sends five commands to the Raspberry Pi Pico over USB serial communication:

```text
index <value>
middle <value>
ring <value>
pinky <value>
thumb <value>
```

The commands are sent approximately every 0.05 seconds, giving an update rate of about 20 Hz.

Serial communication uses a baud rate of 115200.

### 5. MicroPython Servo Control

The Raspberry Pi Pico continuously checks for incoming serial commands without blocking the rest of the program.

Each received tracking value is:

1. Matched to the corresponding finger
2. Converted into a floating-point number
3. Clamped between `0.0` and `1.0`
4. Mapped to a PWM duty-cycle range
5. Sent to the appropriate servo motor

The PWM range used by the current prototype is:

```python
zero_pos = 2000
max_pos = 5500
```

The servo duty cycle is calculated using:

```python
duty = zero_pos + (max_pos - zero_pos) * tracked_value
```

The thumb tracking value is multiplied by two before being clamped to compensate for its smaller detected movement range.

All servos operate at 50 Hz and initialize at the zero position when the Pico program starts.

### 6. Mechanical Actuation

Each servo motor is connected to a finger through a string-based tendon.

When the servo rotates, it pulls the tendon and curls the corresponding finger. Because each finger has its own servo, all five fingers can be controlled independently.

## System Architecture

```text
Webcam Input
      ↓
Python + OpenCV
      ↓
MediaPipe Hand Landmark Detection
      ↓
Normalized Finger Position Calculation
      ↓
USB Serial Commands
      ↓
Raspberry Pi Pico + MicroPython
      ↓
PWM Servo Signals
      ↓
Servo Motors
      ↓
Tendon-Driven Finger Movement
```

## Code

The project consists of two main programs.

### Computer Tracking Program

The computer-side Python program is responsible for:

* Capturing the webcam feed
* Detecting hand landmarks
* Calculating normalized finger positions
* Recording the initial hand position
* Drawing landmarks and fingertip labels
* Sending finger values to the Pico through USB serial

Required Python packages:

```bash
pip install opencv-python mediapipe pyserial
```

The serial port may need to be changed depending on the computer:

```python
Port = "/dev/cu.usbmodem101"
Baud = 115200
```

### Raspberry Pi Pico Program

The MicroPython program is responsible for:

* Initializing five PWM-controlled servos
* Reading incoming commands through standard input
* Identifying the requested finger
* Clamping tracking values to a safe range
* Mapping values to calibrated PWM duty cycles
* Updating the corresponding servo position

## Challenges

### Passive Finger Return

The tendons actively pull the fingers closed, but the current prototype does not actively pull them open. Finger return depends on gravity, material stiffness, and the orientation of the hand.

A future version could use elastic tendons, springs, or a two-tendon system for active opening and closing.

### Tendon Tension

Small changes in string tension significantly affect finger movement. Each tendon requires manual adjustment to produce consistent movement without overloading the servo.

### Servo Calibration

Each servo and finger mechanism has a limited safe range. The PWM values had to be calibrated to avoid over-rotation, excessive string tension, and servo stalling.

### Camera-Distance Variation

Raw landmark distances change when the user moves toward or away from the camera. The program reduces this effect by normalizing fingertip distances using the wrist-to-middle-MCP distance.

### Tracking Stability

MediaPipe tracking can produce small variations between frames, which may cause servo jitter. The current version does not apply a dedicated smoothing filter.

A future version could use:

* Moving-average filtering
* Exponential smoothing
* Dead zones
* Rate limiting
* Improved handling when the hand is temporarily lost

### Mechanical Precision

The prototype was constructed using accessible materials rather than machined or 3D-printed components. This reduced the precision, stiffness, and repeatability of the finger mechanisms.

### Power Delivery

Five servos can draw more current than the Raspberry Pi Pico can safely provide. The servos therefore require an external power source with a shared ground connection between the external supply and the Pico.

## Current Status

Mouve currently functions as a proof-of-concept camera-controlled robotic hand.

The project successfully demonstrates:

* Webcam-based hand tracking
* Detection of individual finger movement
* Normalization of hand landmark measurements
* USB serial communication
* Independent control of five servos
* PWM-based servo calibration
* Tendon-driven robotic finger movement
* Integration of computer vision, embedded control, electronics, and mechanical design

The prototype is not intended to function as a finished prosthetic device. It serves as a platform for testing robotic hand control and vision-based human-machine interaction.

## Future Improvements

* Add active finger return using springs, elastics, or additional tendons
* Apply smoothing filters to reduce tracking and servo jitter
* Add reliable handling for lost camera tracking
* Improve tracking-to-servo calibration for each finger
* Redesign the hand using stronger or 3D-printed components
* Improve tendon routing and tension adjustment
* Add wrist movement
* Improve power distribution and wire management
* Rewrite the embedded servo-control layer in C or C++ for more precise low-level control

## Demo

* [Prototype 1](https://www.youtube.com/watch?v=KmWq7k10VRw)
* [Version 1.0](https://www.youtube.com/watch?v=EqYwuI-Awho&feature=youtu.be)
