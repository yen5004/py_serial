import serial
import time
import argparse
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to initialize the serial connection
def init_serial_connection(port, baudrate=9600):
    try:
        ser = serial.Serial(port, baudrate, timeout=1)  # Timeout of 1 second
        logging.info(f"Connected to {port} at {baudrate} baud.")
        return ser
    except Exception as e:
        logging.error(f"Error connecting to the serial port: {e}")
        return None

# Function to send commands and read responses
def send_command(ser, command, expected_prompt, wait_time=1):
    try:
        ser.write(command.encode())  # Send the command
        time.sleep(wait_time)  # Wait for the response
        response = ser.read(ser.in_waiting).decode()  # Read the response
        logging.info(f"Response: {response}")

        if expected_prompt in response:
            logging.info("Expected prompt detected.")
            return True
        else:
            logging.warning("Expected prompt not found.")
            return False
    except Exception as e:
        logging.error(f"Error during send_command: {e}")
        return False

# Function to read credentials from a file
def read_credentials(file_path):
    try:
        credentials = {}
        with open(file_path, "r") as f:
            lines = f.readlines()
            for line in lines:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    credentials[key.strip()] = value.strip()
        return credentials
    except Exception as e:
        logging.error(f"Error reading credentials file: {e}")
        return None

# Function to login and check password
def login_to_switch(ser, password):
    # Hardcoded username
    username = "Administrator"

    # Send username
    logging.info(f"Sending username: {username}")
    if not send_command(ser, username + '\r', "Password:"):
        logging.error("Username not accepted or login failed.")
        return False

    # Send password
    logging.info("Sending password.")
    if send_command(ser, password + '\r', "Switch#"):
        logging.info("Password correct, login successful!")
        return True
    else:
        logging.error("Incorrect password or login failed.")
        return False

def main():
    # Use argparse for flexibility
    parser = argparse.ArgumentParser(description="Serial Connection Script for Switch Login")
    parser.add_argument("--port", required=True, help="Serial port to connect to (e.g., COM3, /dev/ttyUSB0).")
    parser.add_argument("--baudrate", type=int, default=9600, help="Baud rate for the serial connection.")
    parser.add_argument("--file", required=True, help="Path to the credentials file.")
    args = parser.parse_args()

    # Read credentials from the provided file
    credentials = read_credentials(args.file)
    if not credentials:
        return

    password = credentials.get("password")
    if not password:
        logging.error("Password missing in the credentials file.")
        return

    # Initialize serial connection
    ser = init_serial_connection(args.port, args.baudrate)
    if not ser:
        return

    try:
        # Try to log in to the switch
        if login_to_switch(ser, password):
            logging.info("Login successful.")
        else:
            logging.error("Login failed.")
    finally:
        # Ensure the serial connection is closed
        ser.close()
        logging.info("Serial connection closed.")

if __name__ == "__main__":
    main()
