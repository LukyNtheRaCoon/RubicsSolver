from brian.sensors.EV3 import ColorSensorEV3
from brian.sensors import SensorPort
from brian.motors import EV3LargeMotor
from brian.motors import MotorPort

levy = None
pravy = None
target = None
K = None
error = None
change = None
light = None

def retry(sensor, call_fun):
  while True:
    try:
      sensor.wait_until_ready()
      return call_fun()
    except SensorIsNotReadyError:
      # Sensor can fail while reading, retry on exception
      pass


light = ColorSensorEV3(SensorPort.S1)
levy = EV3LargeMotor(MotorPort.B)
pravy = EV3LargeMotor(MotorPort.C)
levy.wait_until_ready()
pravy.wait_until_ready()
target = 20
K = 1
while True:
  error = retry(light, light.reflected_value) - target
  change = K * error
  levy.run_at_speed(200 - change)
  pravy.run_at_speed(200 + change)

import brian.sensors as sensors
import brian.motors as motors
import time

def setColor(motor_a, color):
    cerna = color.reflected_value()
    motor_a.rotate_by_angle(180, 200)
    bila = color.reflected_value()
    motor_a.rotate_by_angle(-180, 200)
    return (bila + cerna) / 2

rychle = 70
toci = 35
netoc = 3000
celka = 210

MAX_SPEED = 720
SCALE = 4.1  #

# minimální dopředná rychlost, aby se kolo NIKDY nezastavilo
MIN_PWM = 40

laster = 0
po = 0

color = sensors.EV3.ColorSensorEV3(sensors.SensorPort.S1)
motor_a = motors.NXTMotor(motors.MotorPort.C)  # levé kolo
motor_a.wait_until_ready()
motor_b = motors.NXTMotor(motors.MotorPort.B)  # pravé kolo
motor_b.wait_until_ready()

dobre = setColor(motor_a, color)

while True:
    svetlo = color.reflected_value()

    vychylka = dobre - svetlo
    pred = vychylka - laster
    rychlost = (toci * vychylka) + (netoc * pred) + (celka * po)
    rychlost = int(rychlost / 100)

    motorC = rychle + rychlost   # levé
    motorB = rychle - rychlost   # pravé

    # OŘEZ: místo 0..100 držíme ⟨MIN_PWM, 100⟩, aby se kolo nikdy nezastavilo
    if motorC < MIN_PWM:
        motorC = MIN_PWM
    if motorB > 100:
        motorB = 100
    if motorB < MIN_PWM:
        motorB = MIN_PWM
    if motorC > 100:
        motorC = 100

    motor_a.run_at_speed(int(motorC * SCALE))  # levé (C)
    motor_b.run_at_speed(int(motorB * SCALE))  # pravé (B)

    po = +vychylka
    laster = vychylka
    time.sleep(0.01)