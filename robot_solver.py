import sys
import time
from rubikscubesolvermicropython.cube import RubiksCube333


class RobotSolver:
    def __init__(self, robot_control):
        self.robot = robot_control
        
    def solve_from_string(self, cube_string):
        """Přijme string, najde řešení přes disk-based MicroPython solver a vykoná ho."""
        try:
            print(f"Hledám řešení pro: {cube_string}")
            print("Čtu vyhledávací tabulky z disku a počítám (Walton solver)...")
            
            # Inicializace kostky - Waltonův solver vyžaduje určení formátu
            my_cube = RubiksCube333(cube_string, "URFDLB")
            
            # Výpočet (Vrací list tahů, např. ['U', 'R2', 'F', ...])
            solution_moves = my_cube.solve()
            
            # Převedeme seznam na klasický souvislý string pro náš překladač
            if isinstance(solution_moves, list):
                raw_sol = " ".join(solution_moves)
            else:
                raw_sol = str(solution_moves)
                
            print(f"Nalezené tahy (Kociemba, {len(raw_sol.split())} tahů): {raw_sol}")
            
            # Vygenerování našich omezených robotických instrukcí
            instructions = self._generate_instructions(raw_sol)
            
            print("Zahajuji fyzické skládání...")
            self._execute_instructions(instructions)
            print("Skládání dokončeno! Kostka by měla být složená.")
            
        except Exception as e:
            print(f"Chyba při výpočtu (zkontrolujte formát stringu): {e}")

    def _execute_instructions(self, instructions):
        """Projde seznam příkazů a provede fyzické pohyby."""
        for step in instructions:
            if step == "FLIP":
                self.robot.flip_cube()
            elif step == "TURN_RIGHT":
                # OPRAVA PODLE KALIBRACE: Celá kostka doprava = platforma PROTI směru
                self.robot.rotate_platform_counter_clockwise()
            elif step == "TURN_LEFT":
                # OPRAVA PODLE KALIBRACE: Celá kostka doleva = platforma PO směru
                self.robot.rotate_platform_clockwise()
            elif step.startswith("D"):
                # Pro tah D musíme přidržet kostku ramenem
                self.robot.hold_cube()
                time.sleep(0.2) # Krátká pauza pro stabilitu
                
                # Tah D je podle Testu 3 zkalibrován správně
                if step == "D":
                    self.robot.rotate_platform_counter_clockwise()
                elif step == "D'":
                    self.robot.rotate_platform_clockwise()
                elif step == "D2":
                    self.robot.rotate_platform_180()
                    
                time.sleep(0.2)
                self.robot.release_cube()
            
            time.sleep(0.3) # Pauza mezi jednotlivými akcemi robota

    def _generate_instructions(self, raw_sol):
        """Převede standardní tahy na manipulační sekvenci robota (FLIP DO LEVA)."""
        steps = raw_sol.split()
        robot_steps = []
        
        # Výchozí pozice stran: U(0), R(1), F(2), D(3), L(4), B(5)
        curr = ["U", "R", "F", "D", "L", "B"]

        for move in steps:
            target = move[0]
            mod = "'" if "'" in move else ("2" if "2" in move else "")
            pos = curr.index(target)
            
            # --- PŘEKRESLENÁ KINEMATIKA (FLIP DO LEVA) ---
            if pos == 3: # Už je dole
                pass
            elif pos == 4: # Vlevo -> 1x Flip doleva
                robot_steps.append("FLIP")
                curr[0], curr[1], curr[3], curr[4] = curr[1], curr[3], curr[4], curr[0]
            elif pos == 0: # Nahoře -> 2x Flip doleva
                for _ in range(2):
                    robot_steps.append("FLIP")
                    curr[0], curr[1], curr[3], curr[4] = curr[1], curr[3], curr[4], curr[0]
            elif pos == 1: # Vpravo -> 3x Flip doleva
                for _ in range(3):
                    robot_steps.append("FLIP")
                    curr[0], curr[1], curr[3], curr[4] = curr[1], curr[3], curr[4], curr[0]
            elif pos == 2: # Vepředu -> Turn Left (F jde na L), pak 1x Flip doleva
                robot_steps.append("TURN_LEFT")
                curr[2], curr[4], curr[5], curr[1] = curr[1], curr[2], curr[4], curr[5]
                robot_steps.append("FLIP")
                curr[0], curr[1], curr[3], curr[4] = curr[1], curr[3], curr[4], curr[0]
            elif pos == 5: # Vzadu -> Turn Right (B jde na L), pak 1x Flip doleva
                robot_steps.append("TURN_RIGHT")
                curr[5], curr[4], curr[2], curr[1] = curr[1], curr[5], curr[4], curr[2]
                robot_steps.append("FLIP")
                curr[0], curr[1], curr[3], curr[4] = curr[1], curr[3], curr[4], curr[0]

            # Fyzické provedení tahu
            robot_steps.append(f"D{mod}")

        return robot_steps