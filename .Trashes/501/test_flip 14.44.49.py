from robot_control import RobotControl
import time

def test_flip():
    print("--- Flipper Motor Test (No Input Required) ---")
    print("Initializing...")
    robot = RobotControl()
   

    print("Motor initialized.")
    print("Flipper will move in 2 seconds. PLEASE CLEAR THE MECHANISM.")
    time.sleep(2)
    
    print("Flipping NOW...")
    robot.flip_cube()
    print("Flip command finished.")
    
    time.sleep(1)
    print("Test complete. Cleaning up...")
    robot.cleanup()

if __name__ == "__main__":
    test_flip()
    

