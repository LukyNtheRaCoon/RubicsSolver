import brian.sensors as sensors
import brian.motors as motors
import time

# --- Sensor & Motor setup ---
color = sensors.EV3.ColorSensorEV3(sensors.SensorPort.S4)
color.set_mode(color.Mode.REFLECT_RAW)
ultra = sensors.EV3.UltrasonicSensorEV3(sensors.SensorPort.S1)

left_motor = motors.NXTMotor(motors.MotorPort.C)
right_motor = motors.NXTMotor(motors.MotorPort.B)
left_motor.wait_until_ready()
right_motor.wait_until_ready()
color.wait_until_ready()
ultra.wait_until_ready()

# --- Parameters ---
BASE_SPEED = -350
Kp = 19.5
Kd = 7
d = 46
OBSTACLE_DISTANCE = 200  # mm
obstacle = False

dur_s = 1
dur_t = 0.3

def go_straight(duration,speed):
    left_motor.run_at_speed(speed)
    right_motor.run_at_speed(speed)
    time.sleep(duration)
    left_motor.run_at_speed(0)
    right_motor.run_at_speed(0)

def turn_right(duration, speed):
    left_motor.run_at_speed(speed)
    right_motor.run_at_speed(-speed)
    time.sleep(duration)
    left_motor.run_at_speed(0)
    right_motor.run_at_speed(0)

def turn_left(duration, speed):
    left_motor.run_at_speed(-speed)
    right_motor.run_at_speed(speed)
    time.sleep(duration)
    left_motor.run_at_speed(0)
    right_motor.run_at_speed(0)

# --- Calibrate black & white ---
BLACK = color.reflected_value_raw()
print("Black:", BLACK)
left_motor.rotate_by_angle(-200, 300)
time.sleep(1)
WHITE = color.reflected_value_raw()
print("White:", WHITE)
left_motor.rotate_by_angle(200, 300)
time.sleep(1)

WHITE = WHITE / d
BLACK = BLACK / d
THRESHOLD = (BLACK + WHITE) / 2

# --- PD setup ---
last_error = 0
last_time = time.time()

print("Starting line following...")

# --- Main loop ---
while True:
    distance = ultra.distance_mm()
    value = color.reflected_value_raw() / d
    current_time = time.time()

    error = value - THRESHOLD
    dt = current_time - last_time
    derivative = (error - last_error) / dt if dt > 0 else 0
    correction = Kp * error + Kd * derivative

    # --- OBSTACLE AVOIDANCE ---
    if distance < OBSTACLE_DISTANCE and distance > 0:
        obstacle = True
        print("Obstacle detected!")

    if(obstacle):
        # Stop briefly
        left_motor.run_at_speed(0)
        right_motor.run_at_speed(0)
        time.sleep(0.3)

        # Turn right
        turn_left(dur_t, 300)

        #  Move forward (around obstacle)
        go_straight(dur_s, -300)

        # Turn left
        turn_right(dur_t, 300)

        # Move forward to pass obstacle
        go_straight(dur_s, -300)

        # Turn left to face original line direction
        turn_right(dur_t, 300)

        #  Reacquire line
        print("Searching for line...")
        go_straight(0.5, -300)
        while True:
            val = color.reflected_value_raw() / d
            if val < THRESHOLD:  # line found
                break
            left_motor.run_at_speed(BASE_SPEED)
            right_motor.run_at_speed(BASE_SPEED)
        time.sleep(0.3)

        #  Stop and reorient
        left_motor.run_at_speed(0)
        right_motor.run_at_speed(0)
        time.sleep(0.5)

        #  Turn right to resume original heading
        turn_left(dur_t, 300)

        obstacle = False
        continue

        # Reset PD state
        #last_error = error
        #last_time = time.time()
        obstacle = False

    # --- PD Line following ---
    left_speed = BASE_SPEED + correction
    right_speed = BASE_SPEED - correction

    left_motor.run_at_speed(left_speed)
    right_motor.run_at_speed(right_speed)

    # --- Update PD memory ---
    last_error = error
    last_time = current_time