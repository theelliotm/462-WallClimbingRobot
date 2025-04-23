import RPi.GPIO as GPIO
import time

import pigpio  # importing GPIO library
import os  # importing os library so as to communicate with the system
import time  # importing time library to make Rpi wait
import pygame

os.system("sudo pigpiod")  # Launching GPIO library

time.sleep(1)

# time.sleep(5)

MOTOR_LEFT_FORWARD_PIN = 23
MOTOR_LEFT_BACKWARD_PIN = 24
MOTOR_LEFT_SPEED_CONTROL_PIN = 27
MOTOR_RIGHT_FORWARD_PIN = 25
MOTOR_RIGHT_BACKWARD_PIN = 17
MOTOR_RIGHT_SPEED_CONTROL_PIN = 22

ESC_PIN = 4

# pi = pigpio.pi()
# pi.set_servo_pulsewidth(ESC_PIN, 0)

# TEST THESE!
# MAX_SPEED = 2000
# MIN_SPEED = 750

GPIO.setmode(GPIO.BCM)
GPIO.setup([MOTOR_LEFT_FORWARD_PIN, MOTOR_LEFT_BACKWARD_PIN, MOTOR_LEFT_SPEED_CONTROL_PIN,
           MOTOR_RIGHT_FORWARD_PIN, MOTOR_RIGHT_BACKWARD_PIN, MOTOR_RIGHT_SPEED_CONTROL_PIN], GPIO.OUT)
GPIO.output([MOTOR_LEFT_FORWARD_PIN, MOTOR_LEFT_BACKWARD_PIN,
            MOTOR_RIGHT_FORWARD_PIN, MOTOR_RIGHT_BACKWARD_PIN], GPIO.LOW)

pwm_left = GPIO.PWM(MOTOR_LEFT_SPEED_CONTROL_PIN, 1000)
pwm_right = GPIO.PWM(MOTOR_RIGHT_SPEED_CONTROL_PIN, 1000)

# print("Make sure the ESC is callibrated. If it has been, connect the battery and press Enter")
# inp = input()
# if inp == '':
#     pi.set_servo_pulsewidth(ESC_PIN, 0)
#     time.sleep(1)
#     pi.set_servo_pulsewidth(ESC_PIN, MAX_SPEED)
#     time.sleep(1)
#     pi.set_servo_pulsewidth(ESC_PIN, MIN_SPEED)
#     time.sleep(2)

# pi.set_servo_pulsewidth(ESC_PIN, 0)

print("Awaiting Command... Options: (c)ontroller, (t)ests, (d)emo inputs")
inp = input()
if inp == 'd' or inp == 'demo':

    os.system("sudo systemctl enable bluetooth")
    os.system("sudo systemctl start bluetooth")

    pygame.init()
    pygame.joystick.init()

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    print(f"Joystick initialized: {joystick.get_name()}")

    buttons_pressed = set([])

    while True:
        pygame.event.pump()

        # BUTTON 0 - X, 1 - Circle, 2 - Square, 3 - Triangle, 4 - Share, 5 - PS Logo, 6 - Select,
        # 7 - left stick, 8 - right stick, 9 - left shoulder, 10 - right shoulder
        # 11 - dpad up, 12 - dpad down, 13 - dpad left, 14 - dpad right

        for i in range(joystick.get_numbuttons()):
            button = joystick.get_button(i)
            if button and not buttons_pressed.__contains__(i):
                buttons_pressed.add(i)
                print(f"Button {i} pressed")
            elif not button and buttons_pressed.__contains__(i):
                buttons_pressed.remove(i)
                print(f"Button {i} released")

        # AXIS 0 - Left X, 1 - Left Y (inverse), 2 - Right X, 3 - Right Y (inverse)
        # RANGE [-1, 1]

        # AXIS 4 - Left Trigger, 5 - Right Trigger
        # Range: [-1, 1)

        for i in range(joystick.get_numaxes()):
            axis = joystick.get_axis(i)
            if abs(axis) > 0.1 and i < 4:
                print(f"Axis {i} value: {axis}")
            elif axis > -0.9 and i >= 4:
                print(f"Trigger {i - 3} value: {axis}")

elif inp == 'c' or inp == 'controller':
    os.system("sudo systemctl enable bluetooth")
    os.system("sudo systemctl start bluetooth")

    pygame.init()
    pygame.joystick.init()

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    print(f"Joystick initialized: {joystick.get_name()}")

    buttons_pressed = set([])

    stopped = False
    stoppedToggle = False

    while True:
        pygame.event.pump()

        left_x = joystick.get_axis(0)  # Left X
        left_y = -joystick.get_axis(1)  # Left Y
        right_x = joystick.get_axis(2)  # Right X
        right_y = -joystick.get_axis(3)  # Right Y

        x_button = joystick.get_button(0)  # X button

        # X is the emergency stop button
        if (x_button and not stopped and not stoppedToggle):
            stoppedToggle = True
            print("Stopping motors")
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
            stoppedToggle = True

        if not stopped:
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

else:
    while True:
        print("Available Tests: (1) Drive Forward for X seconds (2) Drive backwards for X seconds (3) Enable prop motor for X seconds (4) Turn left for X secs  (5) Turn right X secs")
        inp = input()
        if int(inp) == 1:
            print("How many seconds?")
            secs = float(input())
            print("Speed %? (0 - 100)")
            speed = float(input())

            # convert speed (Scale 0 - 100) to scale 75 - 100. set speed to 0 if scale is 0
            if speed != 0:
                speed = ((speed / 100) * 30) + 70

            pwm_left.start(speed)
            pwm_right.start(speed)

            GPIO.output(MOTOR_LEFT_FORWARD_PIN, GPIO.LOW)
            GPIO.output(MOTOR_LEFT_BACKWARD_PIN, GPIO.HIGH)
            GPIO.output(MOTOR_RIGHT_FORWARD_PIN, GPIO.HIGH)
            GPIO.output(MOTOR_RIGHT_BACKWARD_PIN, GPIO.LOW)

            time.sleep(secs)

            pwm_left.stop()
            pwm_right.stop()

        elif int(inp) == 2:
            print("How many seconds?")
            secs = float(input())
            print("Speed %? (0 - 100)")
            speed = float(input())

            # convert speed (Scale 0 - 100) to scale 75 - 100. set speed to 0 if scale is 0
            if speed != 0:
                speed = ((speed / 100) * 30) + 70

            pwm_left.start(speed)
            pwm_right.start(speed)

            GPIO.output(MOTOR_LEFT_FORWARD_PIN, GPIO.HIGH)
            GPIO.output(MOTOR_LEFT_BACKWARD_PIN, GPIO.LOW)
            GPIO.output(MOTOR_RIGHT_FORWARD_PIN, GPIO.LOW)
            GPIO.output(MOTOR_RIGHT_BACKWARD_PIN, GPIO.HIGH)

            time.sleep(secs)

            pwm_left.stop()
            pwm_right.stop()

        elif int(inp) == 3:
            print("How many seconds?")
            secs = float(input())
            print("Speed %? (0 - 100)")
            speed = float(input())

            # pi.set_servo_pulsewidth(ESC_PIN, MIN_SPEED +
            #                         ((MAX_SPEED - MIN_SPEED) * (speed / 100)))

            # time.sleep(secs)

            # pi.set_servo_pulsewidth(ESC_PIN, 0)
            # pi.stop()

        elif int(inp) == 4:
            print("How many seconds?")
            secs = float(input())
            print("Speed %? (0 - 100)")
            speed = float(input())

            # convert speed (Scale 0 - 100) to scale 75 - 100. set speed to 0 if scale is 0
            if speed != 0:
                speed = ((speed / 100) * 30) + 70

            pwm_left.start(speed)
            pwm_right.start(speed)

            GPIO.output(MOTOR_LEFT_FORWARD_PIN, GPIO.HIGH)
            GPIO.output(MOTOR_LEFT_BACKWARD_PIN, GPIO.LOW)
            GPIO.output(MOTOR_RIGHT_FORWARD_PIN, GPIO.HIGH)
            GPIO.output(MOTOR_RIGHT_BACKWARD_PIN, GPIO.LOW)

            time.sleep(secs)

            pwm_left.stop()
            pwm_right.stop()

        elif int(inp) == 5:
            print("How many seconds?")
            secs = float(input())
            print("Speed %? (0 - 100)")
            speed = float(input())

            # convert speed (Scale 0 - 100) to scale 75 - 100. set speed to 0 if scale is 0
            if speed != 0:
                speed = ((speed / 100) * 30) + 70

            pwm_left.start(speed)
            pwm_right.start(speed)

            GPIO.output(MOTOR_LEFT_FORWARD_PIN, GPIO.LOW)
            GPIO.output(MOTOR_LEFT_BACKWARD_PIN, GPIO.HIGH)
            GPIO.output(MOTOR_RIGHT_FORWARD_PIN, GPIO.LOW)
            GPIO.output(MOTOR_RIGHT_BACKWARD_PIN, GPIO.HIGH)

            time.sleep(secs)

            pwm_left.stop()
            pwm_right.stop()
