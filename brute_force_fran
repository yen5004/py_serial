import serial
import time

# Function to initialize the serial connection
def init_serial_connection(port, baudrate=12500):
    try:
        ser = serial.Serial(port, baudrate, timeout=1)  # Timeout of 1 second
        print(f"Connected to {port} at {baudrate} baud.")
        return ser
    except Exception as e:
        print(f"Error connecting to the serial port: {e}")
        return None

# Function to send commands and read responses
def send_command(ser, command, expected_prompt):
    ser.write(command.encode())  # Send the command
    time.sleep(1)  # Wait for the response
    response = ser.read(ser.in_waiting).decode()  # Read the response
    print(f"Response: {response}")

    # Check if the expected prompt is in the response
    if expected_prompt in response:
        print("Prompt detected, proceeding.")
        return True
    else:
        print("Expected prompt not found.")
        return False

# Function to read username and password from file
def read_credentials(file_path):
    credentials = {}
    try:
        with open(file_path, "r") as f:
            lines = f.readlines()
            for line in lines:
                if '=' in line:
                    key, value = line.strip().split('=')
                    credentials[key.strip()] = value.strip()
        return credentials
    except Exception as e:
        print(f"Error reading credentials file: {e}")
        return None

# Function to login and check password
def login_to_switch(ser, username, password):
    # Send username and password prompts (assuming username is requested first)
    print(f"Sending username: {username}")
    if not send_command(ser, username + '\r', "Password:"):
        print("Username not accepted or login failed.")
        return False

    # Send password
    print(f"Sending password: {password}")
    if send_command(ser, password + '\r', "Switch#"):
        print("Password correct, login successful!")
        return True
    else:
        print("Incorrect password or login failed.")
        return False

def main():
    # Serial port settings (adjust these for your system)
    port = "COM3"  # Replace with your actual serial port
    baudrate = 12500

    # Path to the file containing username and password
    file_path = "credentials.txt"  # Change to your credentials file path

    # Read username and password from the file
    credentials = read_credentials(file_path)
    if not credentials:
        return

    username = credentials.get("username")
    password = credentials.get("password")

    if not username or not password:
        print("Username or password missing in the credentials file.")
        return

    # Initialize serial connection
    ser = init_serial_connection(port, baudrate)
    if not ser:
        return

    # Try to login to the switch with the provided username and password
    if login_to_switch(ser, username, password):
        print("Login successful.")
    else:
        print("Login failed.")

    # Close the serial connection
    ser.close()

if __name__ == "__main__":
    main()
