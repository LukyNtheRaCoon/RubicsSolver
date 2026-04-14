import brian.sensors as sensors
import brian.motors as motors
import time

color = sensors.EV3.ColorSensorEV3(sensors.SensorPort.S4)
color.set_mode(color.Mode.REFLECT_RAW)

servo = motors.NXTMotor(motors.MotorPort.A)
left_motor = motors.NXTMotor(motors.MotorPort.C)   # left wheel
right_motor = motors.NXTMotor(motors.MotorPort.B)  # right wheel
left_motor.wait_until_ready()
right_motor.wait_until_ready()
servo.wait_until_ready()

speed = -300

left_motor.run_at_speed(speed)
right_motor.run_at_speed(speed+1)
time.sleep(1)

left_motor.brake()
right_motor.brake()
servo.rotate_by_angle(90, 300)
time.sleep(1)
servo.rotate_by_angle(-90, 100)
time.sleep(0.1)

left_motor.run_at_speed(speed+15)
right_motor.run_at_speed(speed)
time.sleep(2.1)
left_motor.brake()
right_motor.brake()

right_motor.rotate_by_angle(-200, 200)
left_motor.rotate_by_angle(200, 200)

servo.rotate_by_angle(40, 100)