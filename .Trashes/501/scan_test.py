import robot_control
import cube_scanner
import cube_state

if __name__ == "__main__":
    robot = robot_control.RobotControl()
    scanner = cube_scanner.CubeScanner(robot)
    cube = scanner.scan_cube()
    
    print("Cube scanning complete. Final cube state:")
    print(cube)
    for i in range(6):
        for j in range(9):
            print(cube[i*9 + j], end=' ')
        print()

    state = cube_state.CubeState(cube)
    solved = state.is_solved()
    print(solved)
    robot.cleanup()