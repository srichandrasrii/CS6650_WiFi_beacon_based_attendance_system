import csv
import serial
import time
import requests

# URL of the Flask app's API endpoint to receive the data
api_url = "http://127.0.0.1:5000/update_data"

# Define the serial port and baud rate
ser = serial.Serial('/dev/ttyUSB0', 115200)  # Update with the appropriate port

# Dictionary to store registered MAC IDs, names, average count, and average RSSI
registered_mac_ids = {}

# Read the CSV file
csv_file_path = "website/registered_devices.csv"  # Specify the path to the CSV file
with open(csv_file_path, "r") as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row if present
    for row in reader:
        mac_id = row[0]  # MAC ID is in the first column
        name = row[1]  # Name is in the second column
        roll_no = row[2]

        # Initialize average count and average RSSI to 0 for each registered MAC ID
        registered_mac_ids[mac_id] = {
            'name': name,
            'roll_number': roll_no,
            'average_count': 0,
            'average_rssi': 0
        }

# Time window parameters
window_size = 10  # Time window size in seconds
start_time = time.time()

# Flag to track if the first line has been skipped
first_line_skipped = False

start_time_global = time.time()

while True:
    # Read data from the serial port
    if ser.in_waiting > 0:
        data = ser.readline().decode().strip()
        print("Received data:", data)

        # Skip the first line
        if not first_line_skipped:
            first_line_skipped = True
            continue

        # Split the data into variables
        parts = data.split()
        FT = parts[1]
        FST = parts[3]
        SRC = parts[5]
        DEST = parts[7]
        RSSI = int(parts[9])

        # Update the unique MAC addresses, occurrence counts, and average RSSI
        current_time = time.time()
        elapsed_time = current_time - start_time
        elapsed_time_global = current_time - start_time_global
        print(elapsed_time)

        if SRC in registered_mac_ids:
            count = registered_mac_ids[SRC]['average_count']
            average_rssi = registered_mac_ids[SRC]['average_rssi']
        else:
            count = 0
            average_rssi = 0

        if elapsed_time <= window_size:
            count += 1
            average_rssi = (average_rssi * (count - 1) + RSSI) / count
        else:
            start_time = current_time
            count = 1
            average_rssi = RSSI
            for SRC in registered_mac_ids:
                registered_mac_ids[SRC]['average_count'] = count
                registered_mac_ids[SRC]['average_rssi'] = average_rssi

        if SRC in registered_mac_ids:
            registered_mac_ids[SRC]['average_count'] = count
            registered_mac_ids[SRC]['average_rssi'] = average_rssi

            # Make a POST request to the Flask app's API endpoint
            response = requests.post(api_url, json= {"mac_id": SRC, 
                                                     "name": registered_mac_ids[SRC]['name'], 
                                                     "roll_number": registered_mac_ids[SRC]['roll_number'], 
                                                     "average_count": registered_mac_ids[SRC]['average_count'], 
                                                     "average_rssi": registered_mac_ids[SRC]['average_rssi']
                                                     })

            # Check the response status
            if response.status_code == 200:
                print("Data sent successfully to Flask app!")
            else:
                print("Failed to send data to Flask app.")


        # Open the file in append mode
        file_path = "data_log.txt"  # Specify the file path and name
        file = open(file_path, "a")

        # Write the original data to the file
        file.write("Time: " + str(elapsed_time_global) + "Data:" + str(registered_mac_ids) + "\n")
        file.flush()  # Ensure data is written immediately

file.close()