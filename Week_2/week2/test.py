import serial           # PySerial: for serial communication
import csv              # CSV helper: to write rows easily
from datetime import datetime  # for timestamping

# 1. Configure & open the serial port
#    Change '/dev/cu.usbmodem14101' to whatever port your board uses.
ser = serial.Serial('/dev/cu.usbmodem11101', 115200, timeout=5)

# 2. Announce startup in the terminal
print("=== DHT22 Data Logger ===")
print("Logging once per minute to 'sunrise_humidity.csv'")
print("Press Ctrl+C to stop.\n")

# 3. Open (or create) the CSV file for appending
with open('sunrise_humidity.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Optional: write header if file is brand-new
    # writer.writerow(['timestamp', 'temperature_C', 'humidity_%'])

    try:
        while True:
            # 4. Read one line from Arduino
            raw = ser.readline()               # bytes from serial
            line = raw.decode('utf-8', errors='ignore').strip()

            # 5. Skip blanks or error messages
            if not line or line == "ERROR":
                continue

            # 6. Split into temperature and humidity
            temp_str, hum_str = line.split(',')

            # 7. Create a timestamp in YYYYMMDDhhmmss format
            ts = datetime.now().strftime('%Y%m%d%H%M%S')

            # 8. Write to CSV: [timestamp, temperature, humidity]
            writer.writerow([ts, temp_str, hum_str])
            csvfile.flush()  # ensure it's on disk immediately

            # 9. **New:** print confirmation to terminal
            print(f"[{ts}] Recorded  Temp={temp_str}°C  Humidity={hum_str}%")

            # 10. Wait for the remainder of the minute
            #     (we assume Arduino itself is delaying 60 s per reading,
            #      so this loop runs roughly once per minute)
            #     If you wanted, you could remove this delay and let the Arduino
            #     dictate exact timing.
            pass  

    except KeyboardInterrupt:
        # 11. User pressed Ctrl+C → exit cleanly
        print("\nLogging stopped by user.")

    finally:
        # 12. Always close the serial port
        ser.close()
        print("Serial port closed.")