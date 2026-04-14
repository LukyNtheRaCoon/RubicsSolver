import brian.sensors as sensors
import brian.motors as motors
import time

# --- sensors & motors ---
color = sensors.EV3.ColorSensorEV3(sensors.SensorPort.S4)
color.set_mode(color.Mode.REFLECT)   # calibrated 0..100
color.wait_until_ready()

left_motor = motors.NXTMotor(motors.MotorPort.C)
right_motor = motors.NXTMotor(motors.MotorPort.B)
left_motor.wait_until_ready()
right_motor.wait_until_ready()

# --- params (yours + turning helpers) ---
BASE_SPEED = -500        # forward for your geometry (negative per your code)
Kp = 0.6
Kd = 0.3
MAX_SPEED = 500          # allow more headroom so the outer wheel can speed up in turns
DEADBAND = 1.0           # % reflect; zero-out tiny errors
DT_FLOOR = 0.0008          # min dt for derivative (tighter than 0.08 so D isn't too weak)
DERIV_CAP = 400.0        # cap derivative term magnitude
SLEW_PER_SEC = 40000.0    # deg/s^2; limits how fast speed changes
EMA_ALPHA = 1          # 0..1; lower = smoother

# --- turn boosters ---
STEER_GAIN = 1.0         # >1 = stronger yaw (1.5–2.5 typical)
NONLIN_P = 1.25          # >1 boosts big errors, gentle near center (1.15–1.35)
PIVOT_ERR = 5.0          # |error| to start pivot behavior (in reflect %)
PIVOT_BRAKE = 0.0        # 0..1: inner wheel scale; 0 = full stop for max turn-in
CURVE_SLOW_ERR = 4.0     # |error| to start auto slow-down
CURVE_SLOW_FACTOR = 0.75 # multiply BASE_SPEED magnitude in curves (0.6–0.85)

def clamp(v, lo, hi):
    return lo if v < lo else hi if v > hi else v

def avg_reflect(n=8, delay=0.01):
    s = 0.0
    for _ in range(n):
        s += color.reflected_value()
        time.sleep(delay)
    return s / n

# --- improved calibration (average a few samples) ---
print("Calibrating... hold on BLACK")
time.sleep(0.5)
BLACK = avg_reflect()

left_motor.rotate_by_angle(-220, 250)  # move to WHITE slowly
time.sleep(0.5)
WHITE = avg_reflect()

left_motor.rotate_by_angle(+220, 250)  # return
time.sleep(0.3)

THRESHOLD = (BLACK + WHITE) / 2.0
print(f"BLACK={BLACK:.1f} WHITE={WHITE:.1f} THRESHOLD={THRESHOLD:.1f}")

# --- control loop helpers ---
ema = None
last_error = 0.0
last_time = time.time()
last_left = 0.0
last_right = 0.0

while True:
    raw = color.reflected_value()                 # 0..100
    # initialize EMA on first run
    ema = raw if ema is None else (EMA_ALPHA*raw + (1-EMA_ALPHA)*ema)
    value = ema

    now = time.time()
    dt = max(now - last_time, DT_FLOOR)

    # If steering is reversed for your build, flip the sign:
    # error = value - THRESHOLD
    error = THRESHOLD - value

    # deadband to suppress micro-oscillation
    if abs(error) < DEADBAND:
        error = 0.0

    # derivative on error, with cap against spikes
    d = (error - last_error) / dt
    if d > DERIV_CAP: d = DERIV_CAP
    if d < -DERIV_CAP: d = -DERIV_CAP

    # --- TURN BOOSTERS ---
    # Non-linear error: gentle near center, stronger when far
    e_mag = abs(error)
    e_nl  = (e_mag ** NONLIN_P) * (1 if error >= 0 else -1)

    # Stronger steering overall
    correction = STEER_GAIN * (Kp * e_nl + Kd * d)

    # Auto slow in curves so correction dominates
    base = BASE_SPEED
    if e_mag >= CURVE_SLOW_ERR:
        base = BASE_SPEED * CURVE_SLOW_FACTOR

    # target speeds with saturation
    tgt_left  = clamp(base + correction,  -MAX_SPEED, MAX_SPEED)
    tgt_right = clamp(base - correction,  -MAX_SPEED, MAX_SPEED)

    # Optional: pivot/brake inner wheel for max turn-in on big error
    if e_mag >= PIVOT_ERR:
        if correction > 0:
            # turning left hard -> slow/stop left (inner) wheel
            tgt_left = PIVOT_BRAKE * tgt_left
        else:
            # turning right hard -> slow/stop right (inner) wheel
            tgt_right = PIVOT_BRAKE * tgt_right

    # slew-rate limit (avoid instant big jumps)
    max_step = SLEW_PER_SEC * dt
    cmd_left  = clamp(tgt_left,  last_left - max_step,  last_left + max_step)
    cmd_right = clamp(tgt_right, last_right - max_step, last_right + max_step)

    left_motor.run_at_speed(int(cmd_left))
    right_motor.run_at_speed(int(cmd_right))

    last_left, last_right = cmd_left, cmd_right
    last_error, last_time = error, now
    time.sleep(0.01)
