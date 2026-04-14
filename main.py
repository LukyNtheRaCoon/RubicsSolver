import robot_control
import robot_solver

if __name__ == "__main__":
    print("Inicializace robota...")
    robot = robot_control.RobotControl()
    
    # Inicializace našeho nového překladače a exekutora
    solver = robot_solver.RobotSolver(robot)
    
    # 1. ZDE VLOŽ MANUÁLNÍ STRING PRO TESTOVÁNÍ
    # Např. kostka zamíchaná tahem R U R' U'
    # test_string = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB" (srovnaná, nic neudělá)
    test_string = "UULUUFUUFRRUBRRURRFFDFFUFFFDDRDDDDDDBLLLLLLLLBRRBBBBBB" 
    
    print("Odesílám string do solveru...")
    # 2. Spuštění procesu
    solver.solve_from_string(test_string)
    
    print("Vypínám motory...")
    robot.cleanup()