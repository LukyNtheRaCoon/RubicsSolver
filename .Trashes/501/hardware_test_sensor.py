#!/usr/bin/env python3
import time
from brian.sensors import SensorPort
from brian.sensors.EV3 import ColorSensorEV3
from robot_config import SENSOR_PORT_COLOR_1, SENSOR_PORT_COLOR_2, SENSOR_PORT_COLOR_3

def main():
    print("--- Hardware Test: Sensors ---")
    
    sensors = []
    ports = [SENSOR_PORT_COLOR_1, SENSOR_PORT_COLOR_2, SENSOR_PORT_COLOR_3]
    
    print("Initializing sensors...")
    for i, port in enumerate(ports):
        try:
            print(f"Initializing Sensor {i+1} on port {port.name}...")
            sensor = ColorSensorEV3(port)
            if sensor.wait_until_ready(timeout_ms=5000):
                print(f"Sensor {i+1} is READY.")
                sensors.append(sensor)
            else:
                print(f"Sensor {i+1} timed out waiting for ready.")
                sensors.append(None)
        except Exception as e:
            print(f"Failed to initialize Sensor {i+1}: {e}")
            sensors.append(None)

    print("\nReading colors for 10 iterations...")
    input("Press Enter to start reading...")
    
    try:
        for i in range(10):
            readings = []
            for idx, sensor in enumerate(sensors):
                if sensor:
                    try:
                        color = sensor.detected_color()
                        readings.append(f"S{idx+1}:{color.name}")
                    except Exception as e:
                        readings.append(f"S{idx+1}:Err")
                else:
                    readings.append(f"S{idx+1}:None")
            
            print(f"Iter {i+1}: " + " | ".join(readings))
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nAborted by user.")
    
    print("\nCleaning up...")
    for sensor in sensors:
        if sensor:
            try:
                sensor.close_sensor()
            except:
                pass
    print("Test Complete.")

if __name__ == "__main__":
    main()
