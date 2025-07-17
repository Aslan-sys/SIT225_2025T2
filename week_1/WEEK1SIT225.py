import serial
import random
from datetime import datetime
import time

# Setting baud rate will run into problems if its not the same as ardunio rate
baud_rate = 9600
# Set serial port
port = '/dev/cu.usbmodem11101'
try:
    ser = serial.Serial(port, baud_rate, timeout=5)
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit(1)

# Ensure serial buffer is clear
ser.reset_input_buffer()
ser.reset_output_buffer()

while True:
    # Generates at random (1-5)
    data_send = random.randint(1, 5)
    # sends it to the ardunio 
    ser.write(f"{data_send}\n".encode('utf-8'))
    # by loging it time stamps date and time
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Sent: {data_send}")

    # Pauses til ardunio sends something back
    while True:
        try:
            response = ser.readline().decode('utf-8').strip()
            if response.isdigit():
                sleep_time = int(response)
                break
        except UnicodeDecodeError:
            print("Error decoding response, retrying...")
            continue

    # Log received number with timestamp
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Received: {sleep_time}")
    # Log sleep event
    print(f"Sleeping for {sleep_time} seconds...\n")
    # Sleep for the specified duration
    time.sleep(sleep_time)

    # Pause to avoid overwhelming the Arduino
    time.sleep(0.1)
    