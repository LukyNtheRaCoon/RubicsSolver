import kociemba
import time

class RobotSolver:
    def __init__(self, robot_control):
        self.robot = robot_control
        
    def solve_from_string(self, cube_string):
        """Hlavní metoda: Přijme string, najde řešení a rovnou ho vykoná."""
        try:
            print(f"Hledám řešení pro: {cube_string}")
            raw_sol = kociemba.solve(cube_string)
            print(f"Kociemba tahy: {raw_sol}")
            
            # Vygenerujeme instrukce pro naše omezené pohyby
            instructions = self._generate_instructions(raw_sol)
            print("Zahajuji fyzické skládání...")
            self._execute_instructions(instructions)
            print("Skládání dokončeno!")
            
        except ValueError as e:
            print(f"Chyba Kociemba algoritmu (neplatný string): {e}")

    def _execute_instructions(self, instructions):
        """Projde seznam příkazů a provede fyzické pohyby."""
        for step in instructions:
            if step == "FLIP":
                self.robot.flip_cube()
            elif step == "TURN_RIGHT":
                # Celá kostka doprava = platforma po směru hodinových ručiček
                self.robot.rotate_platform_clockwise()
            elif step == "TURN_LEFT":
                # Celá kostka doleva = platforma proti směru
                self.robot.rotate_platform_counter_clockwise()
            elif step.startswith("D"):
                # Pro tah D musíme přidržet kostku
                self.robot.hold_cube()
                time.sleep(0.2) # Krátká pauza pro stabilitu
                
                # UPOZORNĚNÍ: Rotace D (dole) při pohledu shora je inverzní!
                # Tah 'D' (po směru zespoda) znamená, že platforma (shora) jede PROTI směru.
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
        """Převede standardní tahy na manipulační sekvenci s FLIPEM DO LEVA."""
        steps = raw_sol.split()
        robot_steps = []
        
        # Výchozí pozice stran: U(0), R(1), F(2), D(3), L(4), B(5)
        curr = ["U", "R", "F", "D", "L", "B"]

        for move in steps:
            target = move[0]
            mod = "'" if "'" in move else ("2" if "2" in move else "")
            pos = curr.index(target)
            
            # --- NOVÁ LOGIKA PŘESUNŮ (FLIP DO LEVA: R->U, U->L, L->D, D->R) ---
            if pos == 3: # Už je dole
                pass
                
            elif pos == 4: # Vlevo -> 1x Flip doleva ho hodí rovnou dospod
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
                # Rotace celé kostky doleva kolem osy Y (F->L, L->B, B->R, R->F)
                curr[2], curr[4], curr[5], curr[1] = curr[1], curr[2], curr[4], curr[5]
                
                # Nyní je cíl na pozici 4 (Vlevo), stačí 1x Flip!
                robot_steps.append("FLIP")
                curr[0], curr[1], curr[3], curr[4] = curr[1], curr[3], curr[4], curr[0]
                
            elif pos == 5: # Vzadu -> Turn Right (B jde na L), pak 1x Flip doleva
                robot_steps.append("TURN_RIGHT")
                # Rotace celé kostky doprava kolem osy Y (B->L, L->F, F->R, R->B)
                curr[5], curr[4], curr[2], curr[1] = curr[1], curr[5], curr[4], curr[2]
                
                # Nyní je cíl opět na pozici 4 (Vlevo), stačí 1x Flip!
                robot_steps.append("FLIP")
                curr[0], curr[1], curr[3], curr[4] = curr[1], curr[3], curr[4], curr[0]

            # Nakonec provedeme samotný tah spodní vrstvou
            robot_steps.append(f"D{mod}")

        return robot_steps