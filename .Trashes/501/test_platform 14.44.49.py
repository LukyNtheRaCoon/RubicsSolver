from robot_control import RobotControl
import time

def test_platform():
    print("--- Platform Motor Test (No Input Required) ---")
    print("Initializing...")
    robot = RobotControl()
    print("Motor initialized.")
    print("Platform will rotate 90 CW in 2 seconds.")
    time.sleep(2)
    
    print("Rotating CW...")
    robot.rotate_platform_clockwise()
    
    time.sleep(2)
    
    print("Rotating CCW back to start...")
    robot.rotate_platform_counter_clockwise()
    
    print("Test complete. Cleaning up...")
    robot.cleanup()

if __name__ == "__main__":
    test_platform()
