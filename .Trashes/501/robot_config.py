# robot_config.py

from brian.motors import MotorPort
from brian.sensors import SensorPort


# --- Motor Configuration ---
# User-specified setup:
# - 1 motor for flipping the cube
# - 1 motor for rotating the cube (e.g., a turntable)
# - 1 motor for moving color sensors (e.g., an arm that positions sensors)

# Assigning arbitrary ports for now; these would need to be physically matched.
MOTOR_PORT_FLIP_CUBE = MotorPort.B
MOTOR_PORT_ROTATE_PLATFORM = MotorPort.A
MOTOR_PORT_SENSOR_ARM = MotorPort.C

# --- Sensor Configuration ---
# User-specified setup: 3 color sensors.
# These sensors will likely be positioned to view different parts of the cube
# or used in conjunction with the sensor arm to scan individual stickers.

# Assigning arbitrary ports for now; these would need to be physically matched.
SENSOR_PORT_COLOR_1 = SensorPort.S1
SENSOR_PORT_COLOR_2 = SensorPort.S2
SENSOR_PORT_COLOR_3 = SensorPort.S3


# --- Physical Dimensions/Assumptions ---
# (These would be determined by the robot's physical design)
# - Angle for a 90-degree platform rotation.
# - Angle for a cube flip.
# - Incremental movements for the sensor arm to scan individual stickers.

# For initial implementation, we'll assume:
# - The 'flip cube' motor can perform a reliable 180-degree flip.
# - The 'rotate platform' motor can perform 90-degree rotations of the cube.
# - The 'sensor arm' motor can move the 3 color sensors across a face, or position them over specific stickers.
# - The 3 color sensors are positioned to efficiently scan a face (e.g., 3 stickers at once, or positioned to reduce arm movement).
# - The mapping from Kociemba moves (U, F, R, etc.) to combinations of these robot actions will be defined in rubik_solver_robot.py.
