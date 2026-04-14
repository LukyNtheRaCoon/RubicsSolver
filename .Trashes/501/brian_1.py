# imports
import brian.sensors as sensors
import brian.motors as motors
from time import sleep

# define I/O
color = sensors.EV3.ColorSensorEV3(sensors.SensorPort.S4)
color.set_mode(color.Mode.REFLECT_RAW)
motor_a = motors.NXTMotor(motors.MotorPort.C)       # leve kolo
motor_a.wait_until_ready()
motor_b = motors.NXTMotor(motors.MotorPort.B)       # prave kolo
motor_b.wait_until_ready()

# variables and const
Kp = 0.45
voltage = -3
turn = 0
turnFactor = 1.14
valueRange = 19           

# functions
def readLight():
    read = color.reflected_value_raw()
    # todo ambient reading
    value = (read - black) * (1 - -1) / (white - black) + -1
    return value

def proportional():
    error = 0 - readLight()
    p = Kp * error
    return p

black = color.reflected_value_raw()
print("Black:", black)
motor_a.rotate_by_angle(-200, 300)
sleep(1)
white = color.reflected_value_raw()
print("White:", white)
motor_a.rotate_by_angle(200, 300)
sleep(1)


# ---------------main---------------
while True:
    for i in range(0, valueRange):
        turn += proportional()
    turn /= valueRange
    print(turn)

    motor_a.run_at_voltage(voltage-((-voltage/turnFactor)*turn))
    motor_b.run_at_voltage(voltage+((-voltage/turnFactor)*turn))

