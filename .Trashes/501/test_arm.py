from robot_arm_control import RobotArmControl
import time

def test_arm():
    print("--- Sensor Arm Motor Test (No Input Required) ---")
    print("Initializing...")
    try:
        robot = RobotArmControl()
    except Exception as e:
        print(f"Initialization failed: {e}")
        return

    print("Motor initialized.")
    print("Arm will move to 45 degrees in 2 seconds.")
    time.sleep(2)
    
    print("Moving to 45...")
    robot.move_sensor_arm(45)
    
    time.sleep(2)
    
    print("Returning to 0...")
    robot.move_sensor_arm(0)
    
    print("Test complete. Cleaning up...")
    robot.cleanup()

if __name__ == "__main__":
    test_arm()
