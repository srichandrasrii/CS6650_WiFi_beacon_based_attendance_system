import csv
import serial
import time
import requests

# URL of the Flask app's API endpoint to receive the data
api_url = "http://192.168.151.148:5000/update_data" # rpi network ip address (running on network)

# Define the serial port and baud rate
ser = serial.Serial('/dev/ttyUSB1', 115200)  # Update with the appropriate port

# Dictionary to store registered MAC IDs, names, average count, and average RSSI
registered_mac_ids = {}

# Read the CSV file
csv_file_path = "website/registered_devices.csv"  # The csv file containing the registered students information
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
            'total_count': 0,
            'average_count': 0,
            'average_rssi': 0,
            'status': "Absent"
        }

# Time window parameters
window_size = 20  # Time window size in seconds
start_time = time.time()

# Flag to track if the first line has been skipped
first_line_skipped = False

start_time_global = time.time()

while True:
    # Read data from the serial port
    if ser.in_waiting > 0:
        data = ser.readline().decode().strip()
        # print("Received data:", data)

        # Skip the first line
        if not first_line_skipped:
            first_line_skipped = True
            continue

        # Split the data into variables
        parts = data.split()
        FT = parts[1] # Frame type
        FST = parts[3] # Frame subtype
        SRC = parts[5] # Source MACID
        DEST = parts[7] # Destination MACID
        RSSI = int(parts[9]) # Signal Strength

        # adding notion of time for averaging
        current_time = time.time()
        elapsed_time = current_time - start_time
        elapsed_time_global = current_time - start_time_global
        print(elapsed_time, "\n")
        
        # Update the unique MAC addresses, occurrence counts, and average RSSI
        if SRC in registered_mac_ids:
            total_count = registered_mac_ids[SRC]['total_count']
            count = registered_mac_ids[SRC]['average_count'] # for maintaining what is average number of times a device is sending frames per 20 sec
            average_rssi = registered_mac_ids[SRC]['average_rssi']

            # Update the status to 'Present' if the MAC ID is detected
            if count>=2:
                registered_mac_ids[SRC]['status'] = 'Present' # marks present if detected properly atleast 2 times
            print(total_count)
        else:
            total_count = 0
            count = 0
            average_rssi = 0

        if elapsed_time <= window_size:
            total_count += 1
            count += 1
            average_rssi = (average_rssi * (total_count - 1) + RSSI) / total_count
        else:
            start_time = current_time
            total_count += 1
            count = 1

            # So that average_count of all MACIds are set to 0 ; average_rssi is over entire count, so it is not changed
            for SRC in registered_mac_ids:
                registered_mac_ids[SRC]['total_count'] = total_count
                registered_mac_ids[SRC]['average_count'] = count
                registered_mac_ids[SRC]['average_rssi'] = average_rssi

        # Updating the dictionary and sending the data to localhost server        
        if SRC in registered_mac_ids:
            
            registered_mac_ids[SRC]['average_count'] = count
            registered_mac_ids[SRC]['average_rssi'] = average_rssi

            # Make a POST request to the Flask app's API endpoint
            response = requests.post(api_url, json= {"mac_id": SRC, 
                                                     "name": registered_mac_ids[SRC]['name'], 
                                                     "roll_number": registered_mac_ids[SRC]['roll_number'], 
                                                     "average_count": registered_mac_ids[SRC]['average_count'], 
                                                     "average_rssi": registered_mac_ids[SRC]['average_rssi'],
                                                     "status": registered_mac_ids[SRC]['status']
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