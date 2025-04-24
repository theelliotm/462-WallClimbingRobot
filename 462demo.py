import RPi.GPIO as GPIO
import time
import sys

import pigpio  # importing GPIO library
import os  # importing os library so as to communicate with the system
import time  # importing time library to make Rpi wait
import pygame

os.system("sudo systemctl enable bluetooth")
os.system("sudo systemctl start bluetooth")

pygame.init()
pygame.joystick.init()

joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Joystick initialized: {joystick.get_name()}")

while True:
    pygame.event.pump()
    if joystick.get_button(5):  # PS Logo
        print("Start button pressed")
        break

    time.sleep(1)


os.system("sudo pigpiod")  # Launching GPIO library

time.sleep(1)

MOTOR_LEFT_FORWARD_PIN = 23
MOTOR_LEFT_BACKWARD_PIN = 24
MOTOR_LEFT_SPEED_CONTROL_PIN = 27
MOTOR_RIGHT_FORWARD_PIN = 25
MOTOR_RIGHT_BACKWARD_PIN = 17
MOTOR_RIGHT_SPEED_CONTROL_PIN = 22

ESC_PIN = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup([MOTOR_LEFT_FORWARD_PIN, MOTOR_LEFT_BACKWARD_PIN, MOTOR_LEFT_SPEED_CONTROL_PIN,
           MOTOR_RIGHT_FORWARD_PIN, MOTOR_RIGHT_BACKWARD_PIN, MOTOR_RIGHT_SPEED_CONTROL_PIN], GPIO.OUT)
GPIO.output([MOTOR_LEFT_FORWARD_PIN, MOTOR_LEFT_BACKWARD_PIN,
            MOTOR_RIGHT_FORWARD_PIN, MOTOR_RIGHT_BACKWARD_PIN], GPIO.LOW)

pwm_left = GPIO.PWM(MOTOR_LEFT_SPEED_CONTROL_PIN, 1000)
pwm_right = GPIO.PWM(MOTOR_RIGHT_SPEED_CONTROL_PIN, 1000)

pi = pigpio.pi()
pi.set_servo_pulsewidth(ESC_PIN, 0)

PROP_MAX_SPEED = 2000
PROP_MIN_SPEED = 750

inp = 'n'

if len(sys.argv) > 1:
    arg1 = sys.argv[1]
    print(f"Argument 1: {arg1}")
    if arg1 == 'arm':
        inp = 'y'
        print("Will arm ESC shortly.")
else:
    print("Assuming ESC is armed. Please rerun with 'arm' argument to arm ESC.")

buttons_pressed = set([])

stopped = False
stoppedToggle = False

if inp == 'y':
    print("Arming ESC...")
    pi.set_servo_pulsewidth(ESC_PIN, 0)
    time.sleep(1)
    pi.set_servo_pulsewidth(ESC_PIN, PROP_MAX_SPEED)
    time.sleep(1)
    pi.set_servo_pulsewidth(ESC_PIN, PROP_MIN_SPEED)
    time.sleep(1)
    print("Armed")

prop_speed = PROP_MIN_SPEED

while True:
    pygame.event.pump()

    left_x = joystick.get_axis(0)  # Left X
    left_y = -joystick.get_axis(1)  # Left Y
    right_x = joystick.get_axis(2)  # Right X
    right_y = -joystick.get_axis(3)  # Right Y

    x_button = joystick.get_button(0)  # X button

    button_toggle = False

    left_bumper = joystick.get_button(9)  # Left Bumper
    right_bumper = joystick.get_button(10)  # Right Bumper

    d_up = joystick.get_button(11)  # D-Pad Up
    d_down = joystick.get_button(12)  # D-Pad Down

    if stopped:
        prop_speed = PROP_MIN_SPEED

    # X is the emergency stop button
    if (x_button and not stopped and not stoppedToggle):
        stoppedToggle = True
        print("Stopping motors")
        pi.set_servo_pulsewidth(ESC_PIN, 0)
        pi.stop()
        pwm_left.stop()
        pwm_right.stop()
        GPIO.output(MOTOR_LEFT_FORWARD_PIN, GPIO.LOW)
        GPIO.output(MOTOR_LEFT_BACKWARD_PIN, GPIO.LOW)
        GPIO.output(MOTOR_RIGHT_FORWARD_PIN, GPIO.LOW)
        GPIO.output(MOTOR_RIGHT_BACKWARD_PIN, GPIO.LOW)
        stopped = True

    if not x_button:
        stoppedToggle = False

    if x_button and stopped and not stoppedToggle:
        stopped = False
        print("Starting motors")
        prop_speed = PROP_MIN_SPEED
        stoppedToggle = True

    if not stopped:

        # Propeller speed control using bumpers and dpad
        if (left_bumper and not button_toggle):
            prop_speed += 100
            button_toggle = True
            print(f"Propeller Speed: {prop_speed}")
        elif (right_bumper and not button_toggle):
            prop_speed -= 100
            button_toggle = True
            print(f"Propeller Speed: {prop_speed}")
        elif (d_up and not button_toggle):
            prop_speed += 10
            button_toggle = True
            print(f"Propeller Speed: {prop_speed}")
        elif (d_down and not button_toggle):
            prop_speed -= 10
            button_toggle = True
            print(f"Propeller Speed: {prop_speed}")
        elif (not left_bumper and not right_bumper and not d_up and not d_down):
            button_toggle = False

        # Ensure prop_speed is within bounds
        if prop_speed < PROP_MIN_SPEED:
            prop_speed = PROP_MIN_SPEED
        elif prop_speed > PROP_MAX_SPEED:
            prop_speed = PROP_MAX_SPEED

        # Set propeller speed
        pi.set_servo_pulsewidth(ESC_PIN, prop_speed)

        # Left stick controls forward/backward movement of left wheel
        if abs(left_y) > 0.1:  # Threshold to avoid noise
            speed = (abs(left_y) * 30) + 70  # Scale to 70 - 100
            pwm_left.start(speed)  # Scale to 0 - 100
            if left_y > 0:
                GPIO.output(MOTOR_LEFT_FORWARD_PIN, GPIO.LOW)
                GPIO.output(MOTOR_LEFT_BACKWARD_PIN, GPIO.HIGH)
            else:
                GPIO.output(MOTOR_LEFT_FORWARD_PIN, GPIO.HIGH)
                GPIO.output(MOTOR_LEFT_BACKWARD_PIN, GPIO.LOW)
        else:
            pwm_left.stop()
            GPIO.output(MOTOR_LEFT_FORWARD_PIN, GPIO.LOW)
            GPIO.output(MOTOR_LEFT_BACKWARD_PIN, GPIO.LOW)

        # Right stick controls forward/backward movement of right wheel
        if abs(right_y) > 0.1:
            speed = (abs(right_y) * 30) + 70
            pwm_right.start(speed)
            if right_y > 0:
                GPIO.output(MOTOR_RIGHT_FORWARD_PIN, GPIO.HIGH)
                GPIO.output(MOTOR_RIGHT_BACKWARD_PIN, GPIO.LOW)
            else:
                GPIO.output(MOTOR_RIGHT_FORWARD_PIN, GPIO.LOW)
                GPIO.output(MOTOR_RIGHT_BACKWARD_PIN, GPIO.HIGH)
        else:
            pwm_right.stop()
            GPIO.output(MOTOR_RIGHT_FORWARD_PIN, GPIO.LOW)
            GPIO.output(MOTOR_RIGHT_BACKWARD_PIN, GPIO.LOW)
