from robot_arm_control import RobotArmControl
import time

def test_flip():
    print("--- Flipper Motor Test (No Input Required) ---")
    print("Initializing...")
    try:
        robot = RobotArmControl()
    except Exception as e:
        print(f"Initialization failed: {e}")
        return

    print("Motor initialized.")
    print("Flipper will move in 2 seconds. PLEASE CLEAR THE MECHANISM.")
    time.sleep(2)
    
    print("Flipping NOW...")
    try:
        robot.flip_cube()
        print("Flip command finished.")
    except Exception as e:
        print(f"Movement failed: {e}")
    
    time.sleep(1)
    print("Test complete. Cleaning up...")
    robot.cleanup()

if __name__ == "__main__":
    test_flip()
    

