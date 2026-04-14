# cube_scanner.py

from brian.sensors import SensorPort
from brian.sensors.EV3 import ColorSensorEV3
from robot_config import SENSOR_PORT_COLOR_1, SENSOR_PORT_COLOR_2, SENSOR_PORT_COLOR_3
from robot_arm_control import RobotArmControl
from cube_state import CubeState

class CubeScanner:
    """
    Manages the color sensors to scan the Rubik's Cube and determine its state.
    Uses three color sensors and coordinates with RobotArmControl for movements.
    """

    # Mapping from ColorSensorEV3.Color enum to CubeState single-character representation
    COLOR_MAP = {
        ColorSensorEV3.Color.WHITE: 'W',
        ColorSensorEV3.Color.RED: 'R',
        ColorSensorEV3.Color.GREEN: 'G',
        ColorSensorEV3.Color.YELLOW: 'Y',
        ColorSensorEV3.Color.ORANGE: 'O',
        ColorSensorEV3.Color.BLUE: 'B',
        ColorSensorEV3.Color.BLACK: 'K', # Black is usually not a cube color, but good for diagnostics
        ColorSensorEV3.Color.BROWN: 'N', # Brown is usually not a cube color
        ColorSensorEV3.Color.NO_COLOR: 'X' # No color detected
    }

    # Sensor arm positions for scanning. These are placeholders and must be calibrated.
    # Assuming the 3 sensors are arranged to read 3 stickers in a row.
    # We need 3 distinct arm positions to read all 9 stickers of a face.
    SENSOR_ARM_POSITIONS = {
        "ROW1": 0,    # Angle for the first row of stickers
        "ROW2": 30,   # Angle for the second row of stickers
        "ROW3": 60    # Angle for the third row of stickers
    }

    def __init__(self, robot_control: RobotArmControl):
        """
        Initializes ColorSensorEV3 instances and takes a RobotArmControl instance
        to orchestrate cube movements during scanning.
        """
        self.color_sensor_1 = None
        self.color_sensor_2 = None
        self.color_sensor_3 = None
        self.robot_control = robot_control
        self._initialize_sensors()

    def _initialize_sensors(self):
        """
        Attempts to initialize the three color sensors.
        """
        try:
            self.color_sensor_1 = ColorSensorEV3(SENSOR_PORT_COLOR_1)
            print(f"Color sensor 1 initialized on port {SENSOR_PORT_COLOR_1.name}")
            self.color_sensor_1.wait_until_ready(timeout_ms=5000)
        except Exception as e:
            print(f"Could not initialize Color Sensor 1 on port {SENSOR_PORT_COLOR_1.name}: {e}")

        try:
            self.color_sensor_2 = ColorSensorEV3(SENSOR_PORT_COLOR_2)
            print(f"Color sensor 2 initialized on port {SENSOR_PORT_COLOR_2.name}")
            self.color_sensor_2.wait_until_ready(timeout_ms=5000)
        except Exception as e:
            print(f"Could not initialize Color Sensor 2 on port {SENSOR_PORT_COLOR_2.name}: {e}")

        try:
            self.color_sensor_3 = ColorSensorEV3(SENSOR_PORT_COLOR_3)
            print(f"Color sensor 3 initialized on port {SENSOR_PORT_COLOR_3.name}")
            self.color_sensor_3.wait_until_ready(timeout_ms=5000)
        except Exception as e:
            print(f"Could not initialize Color Sensor 3 on port {SENSOR_PORT_COLOR_3.name}: {e}")

    def get_current_colors(self) -> list[str]:
        """
        Reads the colors from all three sensors at their current positions.
        Returns a list of single-character representations of the detected colors.
        Order in the list corresponds to sensor 1, 2, 3.
        """
        detected_colors = []
        sensors = [self.color_sensor_1, self.color_sensor_2, self.color_sensor_3]

        for i, sensor in enumerate(sensors):
            if sensor and sensor.is_ready():
                detected_brian_color = sensor.detected_color()
                detected_colors.append(self.COLOR_MAP.get(detected_brian_color, self.COLOR_MAP[ColorSensorEV3.Color.NO_COLOR]))
            else:
                print(f"Warning: Color sensor {i+1} not ready. Returning 'X' for this sticker.")
                detected_colors.append(self.COLOR_MAP[ColorSensorEV3.Color.NO_COLOR])
        return detected_colors

    def scan_cube(self) -> CubeState:
        """
        Orchestrates the scanning of all 54 stickers to determine the cube's initial state.
        This method uses the robot_control's motors to position the cube and sensor arm.
        """
        print("Starting cube scan (using 3 sensors and robot movements)...")
        scanned_colors_list = []

        # Assuming a specific order of scanning faces: Up, Right, Front, Down, Left, Back
        # And assuming the robot starts in a known orientation, e.g., Up face facing top, Front face facing robot.

        # The core idea is:
        # 1. Position sensor arm for row 1. Read 3 stickers.
        # 2. Position sensor arm for row 2. Read 3 stickers.
        # 3. Position sensor arm for row 3. Read 3 stickers.
        # This completes one face (9 stickers).
        # 4. Rotate platform to expose next face.
        # 5. Repeat until all faces are scanned.
        # If some faces are not accessible by platform rotation alone, 'flip_cube' will be needed.

        # For this implementation, let's assume we can scan 6 faces by rotating the platform 4 times
        # and maybe flipping once.

        # --- Scan the first 4 faces (e.g., U, R, D, L in a cycle by platform rotation) ---
        for face_num in range(4): # Will cover 4 faces assuming initial face + 3 rotations
            print(f"Scanning Face {face_num + 1}...")
            # Move sensor arm to position 1 for first row of 3 stickers
            self.robot_control.move_sensor_arm_to_position(self.SENSOR_ARM_POSITIONS["ROW1"])
            scanned_colors_list.extend(self.get_current_colors())

            # Move sensor arm to position 2 for second row of 3 stickers
            self.robot_control.move_sensor_arm_to_position(self.SENSOR_ARM_POSITIONS["ROW2"])
            scanned_colors_list.extend(self.get_current_colors())

            # Move sensor arm to position 3 for third row of 3 stickers
            self.robot_control.move_sensor_arm_to_position(self.SENSOR_ARM_POSITIONS["ROW3"])
            scanned_colors_list.extend(self.get_current_colors())

            if face_num < 3: # After scanning 4 faces, we rotate the platform for the next one
                self.robot_control.rotate_platform_clockwise() # Rotate 90 degrees to next face

        # --- Scan the remaining 2 faces (Back and perhaps another after a flip) ---
        # This part is highly dependent on the robot's physical access and needs calibration.
        # For simplicity, let's assume we can scan Face 5 and Face 6 after a flip and/or another rotation.
        # This is a major simplification and likely needs more sophisticated robot movements.

        # Placeholder for scanning the 5th face (e.g., Back face)
        print("Scanning Face 5...")
        # (Example: maybe needs a flip first to expose the back face properly)
        # self.robot_control.flip_cube()
        self.robot_control.move_sensor_arm_to_position(self.SENSOR_ARM_POSITIONS["ROW1"])
        scanned_colors_list.extend(self.get_current_colors())
        self.robot_control.move_sensor_arm_to_position(self.SENSOR_ARM_POSITIONS["ROW2"])
        scanned_colors_list.extend(self.get_current_colors())
        self.robot_control.move_sensor_arm_to_position(self.SENSOR_ARM_POSITIONS["ROW3"])
        scanned_colors_list.extend(self.get_current_colors())

        # Placeholder for scanning the 6th face (e.g., Down face, if not covered by initial 4)
        print("Scanning Face 6...")
        # (Example: maybe needs another platform rotation after the flip)
        # self.robot_control.rotate_platform_clockwise()
        self.robot_control.move_sensor_arm_to_position(self.SENSOR_ARM_POSITIONS["ROW1"])
        scanned_colors_list.extend(self.get_current_colors())
        self.robot_control.move_sensor_arm_to_position(self.SENSOR_ARM_POSITIONS["ROW2"])
        scanned_colors_list.extend(self.get_current_colors())
        self.robot_control.move_sensor_arm_to_position(self.SENSOR_ARM_POSITIONS["ROW3"])
        scanned_colors_list.extend(self.get_current_colors())


        # Ensure 54 stickers were collected. If not, there's an issue with the scanning logic.
        if len(scanned_colors_list) != 54:
            print(f"Error: Scanned {len(scanned_colors_list)} stickers, expected 54.")
            # Fallback to a solved state or raise an error
            return CubeState("WWWWWWWWWRRRRRRRRRGGGGGGGGGYYYYYYYYYOOOOOOOOOBBBBBBBBB")

        scanned_cube_string = "".join(scanned_colors_list)
        print(f"Scanned cube string: {scanned_cube_string}")
        return CubeState(scanned_cube_string)

    def cleanup(self):
        """
        Releases sensor resources.
        """
        print("Cleaning up sensor resources.")
        if self.color_sensor_1:
            self.color_sensor_1.close_sensor()
        if self.color_sensor_2:
            self.color_sensor_2.close_sensor()
        if self.color_sensor_3:
            self.color_sensor_3.close_sensor()

# Example Usage (for testing purposes, if run directly)
if __name__ == "__main__":
    # This block assumes you have actual motors and sensors connected
    # and a CircuitPython environment.
    print("Initializing Cube Scanner for testing...")
    
    class DummyRobotControl:
        def __init__(self):
            print("Dummy Robot Control initialized.")
        def rotate_platform_clockwise(self):
            print("Dummy: Rotating platform clockwise.")
        def move_sensor_arm_to_position(self, angle):
            print(f"Dummy: Moving sensor arm to {angle} degrees.")
        def flip_cube(self):
            print("Dummy: Flipping cube.")
        def cleanup(self):
            print("Dummy: Cleaning up robot control.")

    class DummyColorSensorEV3:
        def __init__(self, port):
            self.port = port
            self._is_ready = True # Simulate ready state

        def wait_until_ready(self, timeout_ms=None):
            print(f"Dummy Sensor {self.port.name}: Waiting until ready.")
            return True

        def is_ready(self):
            return self._is_ready

        def detected_color(self):
            # Simulate returning different colors based on some logic or fixed pattern
            # For a real test, this would return actual scanned colors.
            # Here, let's just cycle through some colors for demonstration.
            colors = [
                ColorSensorEV3.Color.WHITE, ColorSensorEV3.Color.RED, ColorSensorEV3.Color.GREEN,
                ColorSensorEV3.Color.YELLOW, ColorSensorEV3.Color.ORANGE, ColorSensorEV3.Color.BLUE
            ]
            import random
            return random.choice(colors)

        def close_sensor(self):
            print(f"Dummy Sensor {self.port.name}: Closing sensor.")

    # Temporarily override ColorSensorEV3 for dummy testing
    _original_color_sensor_ev3 = ColorSensorEV3
    ColorSensorEV3 = DummyColorSensorEV3 
    
    dummy_robot = DummyRobotControl()
    scanner = CubeScanner(dummy_robot)

    # Test reading current colors (will use random for dummy)
    print(f"Current colors from sensors: {scanner.get_current_colors()}")
    
    scanned_cube_state = scanner.scan_cube()
    print("\nScanned Cube State (from dummy scan):")
    print(scanned_cube_state)

    scanner.cleanup()
    dummy_robot.cleanup()

    # Restore original ColorSensorEV3
    ColorSensorEV3 = _original_color_sensor_ev3

