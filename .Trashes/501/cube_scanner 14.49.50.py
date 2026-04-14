import robot_config
import math
from cube_state import CubeState

class CubeScanner:
    def __init__(self, robot_control):
        self.robot = robot_control
        self.sensors = []

    import math

    def define_color(r, g, b):
        reference = {
            "w":    (900, 900, 900),
            "y":   (950, 850, 200),
            "o": (950, 400, 150),
            "r":  (800, 150, 150),
            "g":   (150, 700, 250),
            "b":    (100, 300, 800)
        }

        distance = float('inf')
        selected_color = None

        for name, ref_rgb in reference.items():
            actual_distance = math.sqrt(
                (r - ref_rgb[0])**2 + 
                (g - ref_rgb[1])**2 + 
                (b - ref_rgb[2])**2
            )

            if actual_distance < distance:
                distance = actual_distance
                selected_color = name

        return selected_color
    
    def one_side_scan(self):
        colors = []
        self.robot.move_sensor_arm(robot_config.SENSOR_SCAN1_ANGLE, 360)
        rgb4 = self.robot.sensor_color_1.rgb_values_raw()
        rgb5 = self.robot.sensor_color_2.rgb_values_raw()
        rgb6 = self.robot.sensor_color_3.rgb_values_raw()
        self.robot.move_sensor_arm(robot_config.SENSOR_SCAN2_ANGLE, 360)
        rgb7 = self.robot.sensor_color_1.rgb_values_raw()
        rgb8 = self.robot.sensor_color_2.rgb_values_raw()
        rgb9 = self.robot.sensor_color_3.rgb_values_raw()
        self.robot.rotate_platform_180()
        rgb3 = self.robot.sensor_color_3.rgb_values_raw()
        rgb2 = self.robot.sensor_color_2.rgb_values_raw()
        rgb1 = self.robot.sensor_color_1.rgb_values_raw()
        self.robot.rotate_platform_180()

        colors.append(  
            self.define_color(*rgb1),
            self.define_color(*rgb2),
            self.define_color(*rgb3),
            self.define_color(*rgb4),
            self.define_color(*rgb5),
            self.define_color(*rgb6),
            self.define_color(*rgb7),
            self.define_color(*rgb8),
            self.define_color(*rgb9),
        )

        return colors

    def scan_cube(self) -> CubeState:
        colors = []
        print("Scanning Cube...")
        
        for i in range(4):
            print(f"Scanning side {i+1}...")
            side_colors = self.one_side_scan()
            colors.append(side_colors)
            self.robot.flip_cube()
        
        self.robot.rotate_platform_clockwise()
        self.robot.flip_cube()

        side_colors = self.one_side_scan()
        colors.append(side_colors)

        self.robot.flip_cube()
        self.robot.flip_cube()

        side_colors = self.one_side_scan()
        colors.append(side_colors)

        self.robot.rotate_platform_counter_clockwise()
        self.robot.flip_cube()

        print("Scan complete.")

        return CubeState(colors)
