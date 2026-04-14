from brian.motors import Motor, MotorPort
import time

def main():
    print("Initializing motor on Port A...")
    try:
        # Initialize the motor on Port A
        motor = Motor(MotorPort.A)
        
        print("Waiting for motor to be ready...")
        if motor.wait_until_ready(timeout_ms=5000):
            print("Motor ready. Rotating 90 degrees clockwise...")
            
            # Rotate by 90 degrees at a speed of 360 deg/sec
            motor.rotate_by_angle(90, 360)
            
            # Wait for the movement to finish
            motor.wait_for_movement()
            print("Rotation complete.")
        else:
            print("Motor failed to become ready (check connection).")
            
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Ensure the motor port is released
        if 'motor' in locals():
            motor.close_motor()
            print("Motor closed.")

if __name__ == "__main__":
    main()
