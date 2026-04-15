import robot_control
import time

robot = robot_control.RobotControl()
print("Polož složenou kostku: Bílá NAHORU, Zelená DOPŘEDU")
time.sleep(3)

# --- TEST 1: FLIP ---
#robot.flip_cube()
# Zkontroluj: Je teď nahoře ČERVENÁ (bývalá pravá)?

# --- TEST 2: TURN ---
# robot.rotate_platform_clockwise()
# Zkontroluj: Je teď dopředu (k senzoru) natočená ORANŽOVÁ (bývalá levá)?

# --- TEST 3: D MOVE ---
robot.hold_cube()
time.sleep(0.5)
robot.rotate_platform_counter_clockwise()
time.sleep(0.5)
robot.release_cube()
# Zkontroluj: Když se podíváš na kostku zespodu, otočila se žlutá po směru hodinových ručiček?

robot.cleanup()