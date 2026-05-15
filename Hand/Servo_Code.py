import sys
from machine import Pin, PWM
import time
import select

poll = select.poll()
poll.register(sys.stdin, select.POLLIN)

button = Pin(0, Pin.IN, Pin.PULL_DOWN)

servo = PWM(Pin(1))
servo.freq(50)

previous_state = 0
check = 0

zero_pos = 2000
max_pos = 8000   

servo.duty_u16(zero_pos)

while True:

    #button tester block
    current_state = button.value()

    if current_state == 1 and previous_state == 0:
        check += 1
        print("Pressed. Check:", check)

        if check % 2 == 1:
            print("ON")
            servo.duty_u16(max_pos)
        else:
            print("OFF")
            servo.duty_u16(zero_pos)

        time.sleep(0.2)  # debounce

    previous_state = current_state

    if poll.poll(0):
        try:
            TrackerValue = float(sys.stdin.readline().strip())
            print("Received TrackerValue:", TrackerValue)

            if TrackerValue >= 1:
                degree_spin = 1 * (max_pos - zero_pos) + zero_pos
                servo.duty_u16(int(degree_spin))
                print("TrackerValue is 1, servo set to max position.")
            elif TrackerValue >= 0.75:
                degree_spin = 0.75 * (max_pos - zero_pos) + zero_pos
                servo.duty_u16(int(degree_spin))
                print("TrackerValue is 0.75, servo set to 75% position.")
            elif TrackerValue >= 0.5:
                degree_spin = 0.5 * (max_pos - zero_pos) + zero_pos
                servo.duty_u16(int(degree_spin))
                print("TrackerValue is 0.5, servo set to mid position.")
            elif TrackerValue >= 0.25:
                degree_spin = 0.25 * (max_pos - zero_pos) + zero_pos
                servo.duty_u16(int(degree_spin))
                print("TrackerValue is 0.25, servo set to 25% position.")
            elif TrackerValue >= 0:
                degree_spin = 0 * (max_pos - zero_pos) + zero_pos
                servo.duty_u16(int(degree_spin))
                print("TrackerValue is 0, servo set to zero position.")
            else:
                print("TrackerValue is out of range. Must be between 0 and 1.")
        except ValueError:
            print("Invalid input. Cant convert line to flaot number.")
            continue
    time.sleep(0.02)
    
