import sys
from machine import Pin, PWM
import time
import select

poll = select.poll()
poll.register(sys.stdin, select.POLLIN)

servos = {
    "index":PWM(Pin(0)),
    "middle":PWM(Pin(1)),
    "ring":PWM(Pin(2)),
    "pinky":PWM(Pin(3)),
    "thumb":PWM(Pin(4))
}

for servo in servos.values():
    servo.freq(50)

previous_state = 0
check = 0

zero_pos = 2000
max_pos = 5500   

for servo in servos.values():
    servo.duty_u16(zero_pos)

while True:

    while poll.poll(0):
        try:
            line = sys.stdin.readline().strip()
            print("Received TrackerValue:", line)

            parts = line.split()
            servo_name = parts[0]
            tracked_value = float(parts[1])
            if servo_name == "thumb":
                tracked_value = 2*tracked_value

            if tracked_value < 0.0:
                tracked_value = 0.0
            elif tracked_value > 1.0:
                tracked_value = 1.0
            
            if servo_name in servos:
                duty = int(zero_pos + (max_pos - zero_pos) * tracked_value)
                duty = max(zero_pos, min(max_pos, duty))
                servos[servo_name].duty_u16(duty)
                print(f"Updated {servo_name} servo to duty: {duty}")
            else:
                print(f"Unknown servo name: {servo_name}")
        except ValueError:
            print("Invalid input. Cant convert line to flaot number.")
            continue
    time.sleep(0.01)
    
