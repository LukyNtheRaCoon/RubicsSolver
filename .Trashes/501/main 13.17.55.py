from rubik_solver_robot import RubikSolverRobot

def main():
    print("--- Rubik's Cube Solver Robot Starting ---")
    
    # Initialize the robot
    # This will set up motors and sensors
    robot = RubikSolverRobot()
    
    try:
        # Start the Scan -> Solve -> Execute loop
        robot.run()
    except KeyboardInterrupt:
        print("\nProgram stopped by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
    finally:
        # Ensure hardware is released safely
        robot.cleanup()
        print("Robot resources cleaned up.")

if __name__ == "__main__":
    main()
