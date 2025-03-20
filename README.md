# Serial Connection Script for Network Switch Login
This repository contains a Python script to establish a serial connection with a network switch, send commands, and log in using hardcoded or file-based credentials.

## Features
- Connect to a network switch over a serial connection.
- Send username and password for authentication.
- Validate responses to ensure successful login.
- Logs command and response interactions for debugging.

## Requirements

### Python
Ensure Python 3.6 or above is installed on your system. You can download it from Python.org.

### Required Libraries
This script requires the pyserial library for serial communication. Install it via pip:

```
pip install pyserial
```

## Setup

## Windows
1. Install Python: Download and install Python from the official site. During installation, check the option to add Python to your system PATH.
2. Install pySerial: Open the Command Prompt and run:

```
pip install pyserial
```
3. Verify Serial Port: Identify the correct COM port by checking the Device Manager (search for "Device Manager" in the Start Menu).

## Linux
1. Install Python: Most Linux distributions come with Python pre-installed. If not, install it using your package manager:

```
sudo apt update
sudo apt install python3 python3-pip
```
2. Install pySerial: Use pip to install the required library:

```
pip3 install pyserial
```

3. Identify Serial Port: Use the dmesg | grep tty command to identify your serial device (e.g., `/dev/ttyUSB0`).

4. Permissions: Grant access to the serial port:
```
sudo chmod a+rw /dev/ttyUSB0
```

## Usage

### Command-Line Arguments
The script accepts the following arguments:

- `--port`: Specify the serial port (e.g., COM3 for Windows or `/dev/ttyUSB0` for Linux).
- `--baudrate`: Specify the baud rate (default is `12500`).
- `--file`: Provide the path to the credentials file.

## Example Command
```
python3 brute_force_fran.py --port "COM3" --baudrate 12500 --file credentials.txt
```
or
```
python3 brute_force2.py --port "COM3" --baudrate 12500 --file rockyou.txt
```
or
```
python3 brute_force2.py --port "/dev/tty USB Port" --baudrate 12500 --file credentials.txt
```


### Credentials File Format
Create a file named `credentials.txt` (or any other name) and ensure it follows this format:

```
password=your_password_here
```
The username is hardcoded as "Administrator."

## Tutorial
1. Clone the Repository:

```
git clone https://github.com/yen5004/py_serial.git
cd py_serial
```

2. Prepare the Credentials File: Create a ```credentials.txt``` file in the same directory as the script, containing your login password.

3. Run the Script:

```
python3 bruteforceFromFile.py --port <your_serial_port> --baudrate 12500 --file credentials.txt
```

4. Login Process:
- The script sends the hardcoded username (`Administrator`) and the password from the credentials file to the switch.
- It validates the responses to ensure successful login.

## What the Code Does
1. Initialize Serial Connection:
    - Opens a serial port connection with the specified baud rate.
2. Send Commands and Validate Prompts:
    - Sends the username and password to the device and checks for expected responses.
3. Read Credentials:
    - Reads the password from a file in key-value format.
4. Login to Switch:
    - Hardcoded username ("Administrator") is sent first, followed by the password.
    - Prompts are validated to ensure authentication was successful.
5. Close Serial Connection:
    - Ensures the serial connection is safely closed.

## Contributing
Feel free to fork this repository, create a branch for your changes, and open a pull request. Contributions are welcome!

## License
This project is licensed under the MIT License.
