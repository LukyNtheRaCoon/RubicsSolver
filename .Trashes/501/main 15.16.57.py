import robot_control
import cube_scanner
import cube_state

if __name__ == "__main__":
    robot = robot_control.RobotControl()
    scanner = cube_scanner.CubeScanner(robot)
    cube = scanner.scan_cube()
    
    print("Cube scanning complete. Final cube state:")
    print(cube)
    robot.cleanup()