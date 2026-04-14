from robot_arm_control import RobotArmControl
import time
import sys

def main():
    print("--- Rubik's Robot Manual Control ---")
    print("Initializing motors (Check ports in robot_config.py)...")
    
    try:
        robot = RobotArmControl()
    except Exception as e:
        print(f"Failed to initialize robot: {e}")
        return

    print("\nInitialization Complete.")
    print("Use this tool to verify motor connections and movement directions.")

    while True:
        print("\n--- MENU ---")
        print("1: Flip Cube (Motor B)")
        print("2: Rotate Platform 90 deg CW (Motor A)")
        print("3: Rotate Platform 90 deg CCW (Motor A)")
        print("4: Rotate Platform 180 deg (Motor A)")
        print("5: Move Sensor Arm (Motor C) - Test Position")
        print("6: Move Sensor Arm (Motor C) - Home Position")
        print("q: Quit")

        if sys.version_info[0] < 3:
            choice = raw_input("Enter choice: ")
        else:
            choice = input("Enter choice: ")

        print(f"Executing option {choice}...")

        try:
            if choice == '1':
                robot.flip_cube()
            elif choice == '2':
                robot.rotate_platform_clockwise()
            elif choice == '3':
                robot.rotate_platform_counter_clockwise()
            elif choice == '4':
                robot.rotate_platform_180()
            elif choice == '5':
                # Test moving arm to 45 degrees
                robot.move_sensor_arm(45)
            elif choice == '6':
                # Move back to 0
                robot.move_sensor_arm(0)
            elif choice == 'q':
                print("Exiting...")
                robot.cleanup()
                break
            else:
                print("Invalid selection.")
            
            # Brief pause to let messages print
            time.sleep(0.5)

        except KeyboardInterrupt:
            print("\nOperation stopped by user.")
            break
        except Exception as e:
            print(f"Error during execution: {e}")

if __name__ == "__main__":
    main()
