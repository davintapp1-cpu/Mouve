from machine import Pin, PWM
import time

button = Pin(0, Pin.IN, Pin.PULL_DOWN)

servo = PWM(Pin(1))
servo.freq(50)

previous_state = 0
check = 0

zero_pos = 2000
max_pos = 8000   # safer than 9000

servo.duty_u16(zero_pos)

while True:
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
    time.sleep(0.02)