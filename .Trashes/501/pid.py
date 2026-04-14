import brian.sensors as sensors
import brian.motors as motors
import time

color = sensors.EV3.ColorSensorEV3(sensors.SensorPort.S4)
color.set_mode(color.Mode.REFLECT_RAW)

left_motor = motors.NXTMotor(motors.MotorPort.C)   # left wheel
right_motor = motors.NXTMotor(motors.MotorPort.B)  # right wheel
left_motor.wait_until_ready()
right_motor.wait_until_ready()

BASE_SPEED = -350                   # forward drive speed
Kp = 45                         # proportional gain
Kd = 25                          # derivative gain
d = 100
last_error = 0
last_time = time.time()

BLACK = color.reflected_value_raw()
print("Black:", BLACK)
left_motor.rotate_by_angle(-200, 300)
time.sleep(1)
WHITE = color.reflected_value_raw()
print("White:", WHITE)
left_motor.rotate_by_angle(200, 300)
time.sleep(1)

WHITE = WHITE/d
BLACK = BLACK/d
THRESHOLD = (BLACK + WHITE) // 2   # midpoint ~55


while True:
    value = color.reflected_value_raw() 
    value = value/d       # sensor reading (0–100)
    current_time = time.time()

    error = value - THRESHOLD                     # how far off the line we are
    dt = current_time - last_time
    derivative = (error - last_error) / dt if dt > 0 else 0

    correction = Kp * error + Kd * derivative     # PD output

    # Compute individual wheel speeds
    left_speed = BASE_SPEED + correction
    right_speed = BASE_SPEED - correction

    # Run motors at the computed speeds
    left_motor.run_at_speed(left_speed)
    right_motor.run_at_speed(right_speed)

    # Update previous values for next loop
    last_error = error
    last_time = current_time
