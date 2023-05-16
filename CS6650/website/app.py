from flask import Flask, render_template, jsonify, request, redirect
import csv

app = Flask(__name__)

devices = {}

def load_devices():
    # Load registered devices from a CSV file
    with open('registered_devices.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # skip header row
        for row in reader:
            mac_id = row[0]
            devices[mac_id] = {
                'name': row[1],
                'roll_number': row[2],
                'average_count': 0,
                'average_rssi': 0
            }

def update_device(mac_id, count, rssi, status):
    # Update the device information in the devices dictionary
    devices[mac_id]['average_count'] = count
    devices[mac_id]['average_rssi'] = rssi
    devices[mac_id]['status'] = status

@app.route('/')
def index():
    # Render the index.html template with devices data
    return render_template('index1.html', devices=devices)

@app.route('/register', methods=['POST'])
def register():
    # Handle device registration
    mac_id = request.form['mac_id']
    name = request.form['name']
    roll_number = request.form['roll_number']

    with open('registered_devices.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # skip header row
        for row in reader:
            if row[0] == mac_id:
                return 'Registration already exists'

    # writing the new registration into the csv file to save it permanently
    with open('registered_devices.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([mac_id, name, roll_number])

    devices[mac_id] = {
        'name': name,
        'roll_number': roll_number,
        'average_count': 0,
        'average_rssi': 0,
        'status': "Absent"
    }

    return redirect('/')

@app.route('/update', methods=['POST'])
def update():
    # Handle device status update
    mac_id = request.form['mac_id']
    count = int(request.form['count'])
    rssi = int(request.form['rssi'])

    update_device(mac_id, count, rssi, "Absent")

    return 'Success'

@app.route('/update_data', methods=['POST'])
def update_data():
    # Handle device data update via JSON
    data = request.json
    mac_id = data['mac_id']
    count = int(data['average_count'])
    rssi = int(data['average_rssi'])
    status = data['status']

    update_device(mac_id, count, rssi, status)

    return jsonify(success=True)

if __name__ == '__main__':
    load_devices()
    app.run(host='192.168.151.148', port=5000, debug=True)  # Run the Flask app on the RPi network IP address
    # This allows accessing the website from other devices on the same network as the RPi