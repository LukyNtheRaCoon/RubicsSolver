from robot_control import RobotControl
import robot_config
import time

def test_arm():
    print("--- Sensor Arm Motor Test (No Input Required) ---")
    print("Initializing...")
    robot = RobotControl()

    print("Motor initialized.")
    print("Arm will move to 45 degrees in 2 seconds.")
    time.sleep(2)
    
    robot.move_sensor_arm(robot_config.SENSOR_SCAN1_ANGLE)
    
    time.sleep(2)
    
    robot.move_sensor_arm(robot_config.SENSOR_SCAN2_ANGLE)
    
    time.sleep(2)

    print("Test complete. Cleaning up...")
    robot.move_sensor_arm(0)

    robot.cleanup()

if __name__ == "__main__":
    test_arm()
