import time
import brian.sensors as sensors
import brian.motors as motors

# -----------------------------
# Hardware
# -----------------------------
color = sensors.EV3.ColorSensorEV3(sensors.SensorPort.S4)
color.set_mode(color.Mode.REFLECT_RAW)

# Ultrasonic (set your real port)
ULTRASONIC_PORT = sensors.SensorPort.S1
us = sensors.EV3.UltrasonicSensorEV3(ULTRASONIC_PORT)
us.wait_until_ready()

left  = motors.NXTMotor(motors.MotorPort.C)  # left wheel
right = motors.NXTMotor(motors.MotorPort.B)  # right wheel
left.wait_until_ready()
right.wait_until_ready()

# -----------------------------
# Tunables
# -----------------------------
DRIVE_SPEED      = -350    # forward (flip sign if needed)
REVERSE_SPEED    =  350
ROTATE_SPEED     =  250
SETTLE           = 0.05

# ultrasonic: consider "detected" if closer than this
DETECT_DISTANCE_MM   = 400    # 40 cm (tweak for your arena)

# how much "more than half" we reverse when homing to center earlier
CENTER_BIAS   = 1.1

# reduce backtrack slightly vs forward probe (compensate for accel/slip/delays)
PROBE_RETURN_GAIN = 0.80   # try 0.85–0.95 if needed

# color threshold (raw reflect 0..1023)
BLACK_THRESHOLD = 350

# rotation calibration
WHEEL_DEGREES_FOR_360_SPIN = 2000

# side-push angle step (instructions: 250/6 to the left, then -2*(250/6), then back by + (250/6))
ANGLE_STEP = 250 / 6.0

# optional cap for side pushes (safety)
SIDE_PUSH_TIMEOUT_S = 3.0

# optional safety cap for a single probe (avoid infinite run if sensor misreads)
PROBE_MAX_TIME_S = 6.0

# -----------------------------
# Helpers
# -----------------------------
def stop_motors():
    left.brake()
    right.brake()

def drive(speed):
    left.run_at_speed(speed)
    right.run_at_speed(speed)

def rotate_by_body_degrees(wheel_deg, speed):
    left.rotate_by_angle(wheel_deg, speed)
    right.rotate_by_angle(-wheel_deg, speed)

def read_reflect():
    return color.reflected_value_raw()

def on_black():
    return read_reflect() <= BLACK_THRESHOLD

def wait_until_black(timeout=None):
    t0 = time.time()
    while True:
        if on_black():
            return True
        if timeout and (time.time() - t0) > timeout:
            return False
        time.sleep(0.003)

def wait_until_white(timeout=None):
    t0 = time.time()
    while True:
        if not on_black():
            return True
        if timeout and (time.time() - t0) > timeout:
            return False
        time.sleep(0.003)

def us_distance_mm():
    # Continuous distance read (0..~2550mm; 2550 can mean "no echo")
    return us.distance_mm()

def forward_with_black_guard(max_time_s):
    """
    Drive forward up to max_time_s or until black is seen.
    Returns the actual forward time (s).
    """
    drive(DRIVE_SPEED)
    start = time.time()
    while True:
        if on_black():
            break
        if (time.time() - start) >= max_time_s:
            break
        time.sleep(0.005)
    stop_motors()
    time.sleep(SETTLE)
    return time.time() - start

def backtrack_time(forward_elapsed_s):
    """
    Convert forward time to reverse time, accounting for speed ratio and return gain.
    """
    return forward_elapsed_s * (abs(DRIVE_SPEED) / abs(REVERSE_SPEED)) * PROBE_RETURN_GAIN

def side_push_from_center(angle_wheel_deg, forward_cap_s):
    """
    From CENTER:
      - rotate by angle_wheel_deg
      - go forward with black guard (up to forward_cap_s)
      - go back to center (time-symmetric with PROBE_RETURN_GAIN)
    Leaves robot at the rotated heading (does NOT restore heading).
    """
    rotate_by_body_degrees(angle_wheel_deg, ROTATE_SPEED)
    time.sleep(SETTLE)

    fwd = forward_with_black_guard(forward_cap_s)
    bt = backtrack_time(fwd)
    drive(REVERSE_SPEED)
    time.sleep(bt)
    stop_motors(); time.sleep(SETTLE)

# -----------------------------
# Main
# -----------------------------
def main():
    # ---------- existing "find center" routine ----------
    if on_black():
        drive(DRIVE_SPEED)
        wait_until_white(timeout=1.5)
        stop_motors()
        time.sleep(SETTLE)

    drive(DRIVE_SPEED)
    wait_until_black()
    stop_motors(); time.sleep(SETTLE)

    rotate_by_body_degrees(250, ROTATE_SPEED)  # ~180°
    time.sleep(SETTLE)

    drive(DRIVE_SPEED)
    wait_until_white(timeout=1.0)
    t0 = time.time()
    wait_until_black()
    t_diam = time.time() - t0
    stop_motors(); time.sleep(SETTLE)

    print(f"Diameter time: {t_diam:.3f} s at |speed|={abs(DRIVE_SPEED)}")

    reverse_time = 0.5 * (abs(DRIVE_SPEED) / abs(REVERSE_SPEED)) * CENTER_BIAS * t_diam
    drive(REVERSE_SPEED)
    time.sleep(reverse_time)
    stop_motors(); time.sleep(SETTLE)

    print("Arrived at (estimated) circle center.")

    # ---------- Probing loop with object-handling & side pushes ----------
    wheel_deg_90 = int(WHEEL_DEGREES_FOR_360_SPIN / 4)

    while True:
        # PROBE: drive forward UNTIL BLACK (with black guard) — watch ultrasonic meanwhile
        drive(DRIVE_SPEED)
        probe_start = time.time()
        saw_object = False

        while True:
            if on_black():
                break
            # optional safety to avoid infinite loop if sensors misread
            if (time.time() - probe_start) > PROBE_MAX_TIME_S:
                break
            d = us_distance_mm()
            if d > 0 and d < DETECT_DISTANCE_MM:
                # mark that we saw something during the probe
                saw_object = True
            time.sleep(0.01)

        stop_motors()
        time.sleep(SETTLE)

        # how long we moved forward during the probe
        forward_elapsed = time.time() - probe_start

        # Return to center after each probe
        back_time = backtrack_time(forward_elapsed)
        drive(REVERSE_SPEED)
        time.sleep(back_time)
        stop_motors(); time.sleep(SETTLE)

        if saw_object:
            # ---- SIDE PUSHES from center ----
            # Left side push: +ANGLE_STEP
            side_push_from_center(+ANGLE_STEP, SIDE_PUSH_TIMEOUT_S)

            # Right side push: -2 * ANGLE_STEP (from current left-heading)
            side_push_from_center(-2 * ANGLE_STEP, SIDE_PUSH_TIMEOUT_S)

            # Restore original heading: +ANGLE_STEP
            rotate_by_body_degrees(+ANGLE_STEP, ROTATE_SPEED)
            time.sleep(SETTLE)
            # then loop back to a new probe (same heading as before)
        else:
            # No object seen during that probe: rotate 90° and probe a new direction
            rotate_by_body_degrees(250/4, ROTATE_SPEED)
            time.sleep(SETTLE)

if __name__ == "__main__":
    try:
        main()
    finally:
        stop_motors()
