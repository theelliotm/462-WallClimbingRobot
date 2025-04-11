import RPi.GPIO as GPIO
import time

import pigpio  # importing GPIO library
import os  # importing os library so as to communicate with the system
import time  # importing time library to make Rpi wait
from evdev import InputDevice, categorize, ecodes

os.system("sudo pigpiod")  # Launching GPIO library

time.sleep(1)

MOTOR_LEFT_FORWARD_PIN = 0
MOTOR_LEFT_BACKWARD_PIN = 0
MOTOR_LEFT_SPEED_CONTROL_PIN = 0
MOTOR_RIGHT_FORWARD_PIN = 0
MOTOR_RIGHT_BACKWARD_PIN = 0
MOTOR_RIGHT_SPEED_CONTROL_PIN = 0

ESC_PIN = 4

pi = pigpio.pi()
pi.set_servo_pulsewidth(ESC_PIN, 0)

# TEST THESE!
MAX_SPEED = 2000
MIN_SPEED = 700

GPIO.setmode(GPIO.BCM)
GPIO.setup([MOTOR_LEFT_FORWARD_PIN, MOTOR_LEFT_BACKWARD_PIN, MOTOR_LEFT_SPEED_CONTROL_PIN,
           MOTOR_RIGHT_FORWARD_PIN, MOTOR_RIGHT_BACKWARD_PIN, MOTOR_RIGHT_SPEED_CONTROL_PIN], GPIO.OUT)
GPIO.output(MOTOR_LEFT_FORWARD_PIN, MOTOR_LEFT_BACKWARD_PIN,
            MOTOR_RIGHT_FORWARD_PIN, MOTOR_RIGHT_BACKWARD_PIN, GPIO.LOW)

pwm_left = GPIO.PWM(MOTOR_LEFT_SPEED_CONTROL_PIN, 1000)
pwm_right = GPIO.PWM(MOTOR_RIGHT_SPEED_CONTROL_PIN, 1000)

print("Make sure the ESC is callibrated. If it has been, connect the battery and press Enter")
inp = input()
if inp == '':
    pi.set_servo_pulsewidth(ESC_PIN, 0)
    time.sleep(1)
    pi.set_servo_pulsewidth(ESC_PIN, MAX_SPEED)
    time.sleep(1)
    pi.set_servo_pulsewidth(ESC_PIN, MIN_SPEED)
    time.sleep(2)

pi.set_servo_pulsewidth(ESC_PIN, 0)

print("Awaiting Command... Options: (c)ontroller, (t)ests")
inp = input()
if inp == 'c' or inp == 'controller':
    # Replace 'event3' with your actual event number
    gamepad = InputDevice('/dev/input/event3')
    print(f"Using device: {gamepad.name}")

    LEFT_STICK_Y = ecodes.ABS_Y
    RIGHT_STICK_Y = ecodes.ABS_RY
    BUTTON_A = ecodes.BTN_SOUTH

    for event in gamepad.read_loop():
        if event.type == ecodes.EV_ABS:
            if event.code == LEFT_STICK_Y:
                print(f"Left Stick Y: {event.value}")
            elif event.code == RIGHT_STICK_Y:
                print(f"Right Stick Y: {event.value}")

        elif event.type == ecodes.EV_KEY:
            if event.code == BUTTON_A:
                if event.value == 1:
                    print("A button pressed")
                elif event.value == 0:
                    print("A button released")
else:
    while True:
        print("Available Tests: (1) Drive Forward for X seconds (2) Drive backwards for X seconds (3) Enable prop motor for X seconds (4) Turn left one rotation (5) Turn right one rotation")
        inp = input()
        if inp == 1:
            print("How many seconds?")
            secs = input()
            print("Speed %? (0 - 100)")
            speed = input()

            if speed < 10:
                speed = 10
            elif speed > 100:
                speed = 100

            pwm_left.start(speed)
            pwm_right.start(speed)

            GPIO.output(MOTOR_LEFT_FORWARD_PIN, GPIO.HIGH)
            GPIO.output(MOTOR_LEFT_BACKWARD_PIN, GPIO.LOW)
            GPIO.output(MOTOR_RIGHT_FORWARD_PIN, GPIO.HIGH)
            GPIO.output(MOTOR_RIGHT_BACKWARD_PIN, GPIO.LOW)

            time.sleep(secs)

            pwm_left.stop()
            pwm_right.stop()

        elif inp == 2:
            print("How many seconds?")
            secs = input()
            print("Speed %? (0 - 100)")
            speed = input()

            pwm_left.start(speed)
            pwm_right.start(speed)

            GPIO.output(MOTOR_LEFT_FORWARD_PIN, GPIO.LOW)
            GPIO.output(MOTOR_LEFT_BACKWARD_PIN, GPIO.HIGH)
            GPIO.output(MOTOR_RIGHT_FORWARD_PIN, GPIO.LOW)
            GPIO.output(MOTOR_RIGHT_BACKWARD_PIN, GPIO.HIGH)

            time.sleep(secs)

            pwm_left.stop()
            pwm_right.stop()

        elif inp == 3:
            print("How many seconds?")
            secs = input()
            print("Speed %? (0 - 100)")
            speed = input()

            pi.set_servo_pulsewidth(ESC_PIN, MIN_SPEED +
                                    ((MAX_SPEED - MIN_SPEED) * (speed / 100)))

            time.sleep(secs)

            pi.set_servo_pulsewidth(ESC_PIN, 0)
            pi.stop()

        elif inp == 4:
            print("Speed %? (0 - 100)")
            speed = input()

            if speed < 10:
                speed = 10
            elif speed > 100:
                speed = 100

            pwm_left.start(speed)
            pwm_right.start(speed)

            GPIO.output(MOTOR_LEFT_FORWARD_PIN, GPIO.LOW)
            GPIO.output(MOTOR_LEFT_BACKWARD_PIN, GPIO.HIGH)
            GPIO.output(MOTOR_RIGHT_FORWARD_PIN, GPIO.HIGH)
            GPIO.output(MOTOR_RIGHT_BACKWARD_PIN, GPIO.LOW)

            time.sleep(3)

            pwm_left.stop()
            pwm_right.stop()

        elif inp == 5:
            print("Speed %? (0 - 100)")
            speed = input()

            if speed < 10:
                speed = 10
            elif speed > 100:
                speed = 100

            pwm_left.start(speed)
            pwm_right.start(speed)

            GPIO.output(MOTOR_LEFT_FORWARD_PIN, GPIO.HIGH)
            GPIO.output(MOTOR_LEFT_BACKWARD_PIN, GPIO.LOW)
            GPIO.output(MOTOR_RIGHT_FORWARD_PIN, GPIO.LOW)
            GPIO.output(MOTOR_RIGHT_BACKWARD_PIN, GPIO.HIGH)

            time.sleep(3)

            pwm_left.stop()
            pwm_right.stop()
