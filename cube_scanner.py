import robot_config
import math
import time
from cube_state import CubeState

class CubeScanner:
    def __init__(self, robot_control):
        self.robot = robot_control

    def _get_rgb(self, c):
        # Bezpečná extrakce (podporuje objekt i raw EV3 tuple)
        if hasattr(c, 'red'):
            return c.red, c.green, c.blue
        return c[0], c[1], c[2]

    def define_color(self, colors):
        # 1. Definice středů podle aktuálního skenu (F, R, B, L, U, D)
        ref_names = ["F", "R", "B", "L", "U", "D"]
        ref_indices = [4, 13, 22, 31, 40, 49]
        
        # Extrakce RGB pro všech 54 políček
        rgb_colors = [self._get_rgb(c) for c in colors]
        references = {name: rgb_colors[idx] for name, idx in zip(ref_names, ref_indices)}

        scores = []
        for r1, g1, b1 in rgb_colors:
            # Výpočet celkové intenzity barvy (vektoru)
            mag1 = math.sqrt(r1**2 + g1**2 + b1**2)
            if mag1 == 0: mag1 = 1.0 # Ochrana proti dělení nulou
            
            pixel_scores = {}
            for name, (r2, g2, b2) in references.items():
                mag2 = math.sqrt(r2**2 + g2**2 + b2**2)
                if mag2 == 0: mag2 = 1.0
                
                # Normalizované složky (odstraní vliv stínů, zkoumá se jen čistý odstín)
                nr1, ng1, nb1 = r1/mag1, g1/mag1, b1/mag1
                nr2, ng2, nb2 = r2/mag2, g2/mag2, b2/mag2
                
                # Vzdálenost barevného poměru (Chromaticity)
                chroma_dist = math.sqrt((nr1-nr2)**2 + (ng1-ng2)**2 + (nb1-nb2)**2)
                
                # Vzdálenost absolutního jasu (pomůže rozlišit velmi světlou žlutou od bílé)
                lum_dist = abs(mag1 - mag2) / 1023.0
                
                # Celkové skóre (čím menší, tím podobnější barva)
                score = chroma_dist * 5.0 + lum_dist
                pixel_scores[name] = score
                
            scores.append(pixel_scores)

        # 3. Rozdělení do skupin po přesně 9 políčkách (Greedy approach s korekcí)
        final_assignment = [None] * 54
        counts = {name: 0 for name in ref_names}

        # Zjistíme "jistotu" senzoru pro každé políčko (rozdíl mezi nejlepší a druhou nejlepší shodou)
        certainty = []
        for i in range(54):
            pixel_scores = sorted(scores[i].items(), key=lambda x: x[1])
            best_color, best_val = pixel_scores[0]
            second_best_color, second_val = pixel_scores[1]
            diff = second_val - best_val
            certainty.append((i, best_color, diff, pixel_scores))

        # Nejdříve přiřadíme barvy políčkům, u kterých si je senzor nejvíce jistý
        certainty.sort(key=lambda x: x[2], reverse=True)

        for i, best_color, diff, pixel_scores in certainty:
            assigned = False
            for color_name, score_val in pixel_scores:
                if counts[color_name] < 9:
                    final_assignment[i] = color_name
                    counts[color_name] += 1
                    assigned = True
                    break
        
        return final_assignment

    def one_side_scan(self):
        self.robot.move_sensor_arm(robot_config.SENSOR_SCAN1_ANGLE)
        time.sleep(0.5)
        rgb2, rgb5, rgb8 = self.robot.sensor_color_1.rgb_values_raw(), self.robot.sensor_color_2.rgb_values_raw(), self.robot.sensor_color_3.rgb_values_raw()
        self.robot.move_sensor_arm(robot_config.SENSOR_SCAN2_ANGLE)
        time.sleep(0.5)
        rgb3, rgb6, rgb9 = self.robot.sensor_color_1.rgb_values_raw(), self.robot.sensor_color_2.rgb_values_raw(), self.robot.sensor_color_3.rgb_values_raw()
        self.robot.rotate_platform_180()
        self.robot.move_sensor_arm(robot_config.SENSOR_SCAN3_ANGLE)
        time.sleep(0.5)
        rgb7, rgb4, rgb1 = self.robot.sensor_color_3.rgb_values_raw(), self.robot.sensor_color_2.rgb_values_raw(), self.robot.sensor_color_1.rgb_values_raw()
        self.robot.move_sensor_arm(0)
        self.robot.rotate_platform_180()
        return [rgb1, rgb2, rgb3, rgb4, rgb5, rgb6, rgb7, rgb8, rgb9]
    
    def one_side_scan_spec(self):
        self.robot.move_sensor_arm(robot_config.SENSOR_SCAN1_ANGLE)
        time.sleep(0.5)
        rgb6, rgb5, rgb4 = self.robot.sensor_color_1.rgb_values_raw(), self.robot.sensor_color_2.rgb_values_raw(), self.robot.sensor_color_3.rgb_values_raw()
        self.robot.move_sensor_arm(robot_config.SENSOR_SCAN2_ANGLE)
        time.sleep(0.5)
        rgb3, rgb2, rgb1 = self.robot.sensor_color_1.rgb_values_raw(), self.robot.sensor_color_2.rgb_values_raw(), self.robot.sensor_color_3.rgb_values_raw()
        self.robot.rotate_platform_180()
        self.robot.move_sensor_arm(robot_config.SENSOR_SCAN3_ANGLE)
        time.sleep(0.5)
        rgb7, rgb8, rgb9 = self.robot.sensor_color_3.rgb_values_raw(), self.robot.sensor_color_2.rgb_values_raw(), self.robot.sensor_color_1.rgb_values_raw()
        self.robot.move_sensor_arm(0)
        self.robot.rotate_platform_180()
        return [rgb1, rgb2, rgb3, rgb4, rgb5, rgb6, rgb7, rgb8, rgb9]

    def scan_cube(self) -> str:
        all_colors = []
        for i in range(4):
            all_colors.extend(self.one_side_scan())
            self.robot.flip_cube()
        self.robot.rotate_platform_clockwise()
        self.robot.flip_cube()
        all_colors.extend(self.one_side_scan_spec())
        self.robot.flip_cube()
        self.robot.flip_cube()
        all_colors.extend(self.one_side_scan_spec())
        self.robot.flip_cube()
        self.robot.flip_cube()
        self.robot.rotate_platform_counter_clockwise()
        # 1. Získáme pole 54 přiřazených barev v pořadí F, R, B, L, U, D
        scanned_list = self.define_color(all_colors)
        
        # 2. Rozříznutí seznamu na jednotlivé strany (každá má 9 prvků)
        F = scanned_list[0:9]
        R = scanned_list[9:18]
        B = scanned_list[18:27]
        L = scanned_list[27:36]
        U = scanned_list[36:45]
        D = scanned_list[45:54]
        
        # 3. Poskládání do Kociemba standardu: U, R, F, D, L, B
        # Spojíme pole a uděláme z nich jeden dlouhý string
        kociemba_list = U + R + F + D + L + B
        kociemba_string = "".join(kociemba_list)
        
        return kociemba_string