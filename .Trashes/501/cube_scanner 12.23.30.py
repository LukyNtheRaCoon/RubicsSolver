import robot_config
import math
import time
from cube_state import CubeState

class CubeScanner:
    def __init__(self, robot_control):
        self.robot = robot_control
        self.sensors = []

    def rgb_to_hsv(self, r, g, b):
        # Převod z rozsahu 0-1023 na 0.0-1.0
        r, g, b = r / 1023.0, g / 1023.0, b / 1023.0
        
        mx = max(r, g, b)
        mn = min(r, g, b)
        df = mx - mn
        
        # Výpočet Hue (odstínu)
        if mx == mn:
            h = 0
        elif mx == r:
            h = (60 * ((g - b) / df) + 360) % 360
        elif mx == g:
            h = (60 * ((b - r) / df) + 120) % 360
        elif mx == b:
            h = (60 * ((r - g) / df) + 240) % 360
            
        # Výpočet Saturation (sytosti)
        s = 0 if mx == 0 else (df / mx)
        
        # Výpočet Value (jasu)
        v = mx
        
        return h / 360.0, s, v  # Vracíme hodnoty v rozsahu 0-1

    def define_color(self, colors):
        hsv_colors = []
        for c in colors:
            hsv_colors.append(self.rgb_to_hsv(c.red, c.green, c.blue))

        reference = {
            "U": hsv_colors[4], "F": hsv_colors[13], "D": hsv_colors[22],
            "B": hsv_colors[31], "R": hsv_colors[40], "L": hsv_colors[49]
        }

        selected_colors = []

        for i, (h, s, v) in enumerate(hsv_colors):
            # 1. Ošetření bílé (pokud je sytost velmi nízká)
            if s < 0.18:
                selected_colors.append("U")
                continue

            best_match = None
            min_diff = float('inf')

            for name, (ref_h, ref_s, ref_v) in reference.items():
                dh = min(abs(h - ref_h), 1.0 - abs(h - ref_h))
                ds = abs(s - ref_s)
                dv = abs(v - ref_v)

                # ZVÝŠENÁ VÁHA: dh * 4.0 místo 2.0 extrémně zvýrazní rozdíl v barvě
                # ds (sytost) snížíme, protože červená i oranžová bývají obě hodně syté
                total_diff = math.sqrt((dh * 5.0)**2 + (ds * 1.5)**2 + (dv * 0.2)**2)

                if total_diff < min_diff:
                    min_diff = total_diff
                    best_match = name
            
            selected_colors.append(best_match)

        return selected_colors
        
    def one_side_scan(self):
        colors = []
        self.robot.move_sensor_arm(robot_config.SENSOR_SCAN1_ANGLE)
        rgb4 = self.robot.sensor_color_1.rgb_values_raw()
        rgb5 = self.robot.sensor_color_2.rgb_values_raw()
        rgb6 = self.robot.sensor_color_3.rgb_values_raw()
        time.sleep(0.5)
        self.robot.move_sensor_arm(robot_config.SENSOR_SCAN2_ANGLE)
        rgb7 = self.robot.sensor_color_1.rgb_values_raw()
        rgb8 = self.robot.sensor_color_2.rgb_values_raw()
        rgb9 = self.robot.sensor_color_3.rgb_values_raw()
        time.sleep(0.5)
        self.robot.rotate_platform_180()
        self.robot.move_sensor_arm(robot_config.SENSOR_SCAN3_ANGLE)
        rgb3 = self.robot.sensor_color_3.rgb_values_raw()
        rgb2 = self.robot.sensor_color_2.rgb_values_raw()
        rgb1 = self.robot.sensor_color_1.rgb_values_raw()
        time.sleep(0.5)
        self.robot.move_sensor_arm(0)
        self.robot.rotate_platform_180()


        colors.append(rgb1)
        colors.append(rgb2)
        colors.append(rgb3)
        colors.append(rgb4)
        colors.append(rgb5)
        colors.append(rgb6)
        colors.append(rgb7)
        colors.append(rgb8)
        colors.append(rgb9)
        return colors

    def scan_cube(self) -> CubeState:
        colors = []
        print("Scanning Cube...")
        
        for i in range(4):
            print(f"Scanning side {i+1}...")
            side_colors = self.one_side_scan()
            for color in side_colors:
                colors.append(color)
            self.robot.flip_cube()
        
        self.robot.rotate_platform_clockwise()
        self.robot.flip_cube()

        side_colors = self.one_side_scan()
        for color in side_colors:
            colors.append(color)

        self.robot.flip_cube()
        self.robot.flip_cube()

        side_colors = self.one_side_scan()
        for color in side_colors:
            colors.append(color)

        self.robot.flip_cube()

        print("Scan complete.")

        defined_colors = self.define_color(colors)

        return defined_colors