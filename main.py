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

print("Awaiting Command... Options: (c)ontroller, (t)ests")
inp = input()
if inp == 'c' or inp == 'controller':
    
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
        
        # BUTTON 0 - A, 1 - B, 2- X, 3 - Y, 4 - minus, 5 - home, 6 - plus, 
        # 7 - left stick, 8 - right stick, 9 - left shoulder, 10 - right shoulder
        # 11 - dpad up, 12 - dpad down, 13 - dpad left, 14 - dpad right
        
        # for i in range(joystick.get_numbuttons()):
        #     button = joystick.get_button(i)
        #     if button and not buttons_pressed.__contains__(i):
        #         buttons_pressed.add(i)
        #         print(f"Button {i} pressed")
        #     elif not button and buttons_pressed.__contains__(i):
        #         buttons_pressed.remove(i)
        #         print(f"Button {i} released")
        
        # AXIS 0 - Left X, 1 - Left Y (inverse), 2 - Right X, 3 - Right Y (inverse)
        # RANGE (-1, 1) 
        
        # AXIS 4 - Left Trigger, 5 - Right Trigger
        # Either -1 or 0.9999...
        
        # for i in range(joystick.get_numaxes()):
        #     axis = joystick.get_axis(i)
        #     if abs(axis) > 0.1:
        #         print(f"Axis {i} value: {axis}")
        
        
        
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
                speed = ((speed / 100) * 30) + 70;

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
                speed = ((speed / 100) * 30) + 70;

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
                speed = ((speed / 100) * 30) + 70;

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
                speed = ((speed / 100) * 30) + 70;

            pwm_left.start(speed)
            pwm_right.start(speed)

            GPIO.output(MOTOR_LEFT_FORWARD_PIN, GPIO.LOW)
            GPIO.output(MOTOR_LEFT_BACKWARD_PIN, GPIO.HIGH)
            GPIO.output(MOTOR_RIGHT_FORWARD_PIN, GPIO.LOW)
            GPIO.output(MOTOR_RIGHT_BACKWARD_PIN, GPIO.HIGH)

            time.sleep(secs)

            pwm_left.stop()
            pwm_right.stop()
