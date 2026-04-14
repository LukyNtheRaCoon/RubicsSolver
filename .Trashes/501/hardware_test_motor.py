#!/usr/bin/env python3
import time
from robot_arm_control import RobotArmControl

def main():
    print("--- Hardware Test: Motors ---")
    print("Initializing RobotArmControl...")
    try:
        robot = RobotArmControl()
    except Exception as e:
        print(f"Failed to initialize RobotArmControl: {e}")
        return

    print("\nTest 1: Rotate Platform Clockwise 90 degrees")
    input("Press Enter to start movement...")
    try:
        robot.rotate_platform_clockwise()
        print("Movement command sent. Waiting 2 seconds...")
        time.sleep(2)
    except Exception as e:
        print(f"Error during rotation: {e}")

    print("\nTest 2: Rotate Platform Counter-Clockwise 90 degrees")
    input("Press Enter to return...")
    try:
        robot.rotate_platform_counter_clockwise()
        print("Movement command sent.")
    except Exception as e:
        print(f"Error during rotation: {e}")

    print("\nCleaning up...")
    robot.cleanup()
    print("Test Complete.")

if __name__ == "__main__":
    main()

