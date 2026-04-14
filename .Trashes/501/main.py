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
