from flask import Flask, render_template, jsonify, request
import csv

app = Flask(__name__)

devices = {}

def load_devices():
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

def update_device(mac_id, count, rssi):
    devices[mac_id]['average_count'] = count
    devices[mac_id]['average_rssi'] = rssi

@app.route('/')
def index():
    return render_template('index1.html', devices=devices)

@app.route('/register', methods=['POST'])
def register():
    mac_id = request.form['mac_id']
    name = request.form['name']
    roll_number = request.form['roll_number']

    with open('registered_devices.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # skip header row
        for row in reader:
            if row[0] == mac_id:
                return 'Registration already exists'

    with open('registered_devices.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([mac_id, name, roll_number])

    devices[mac_id] = {
        'name': name,
        'roll_number': roll_number,
        'average_count': 0,
        'average_rssi': 0
    }

    return render_template('index1.html', devices=devices)

@app.route('/update', methods=['POST'])
def update():
    mac_id = request.form['mac_id']
    count = int(request.form['count'])
    rssi = int(request.form['rssi'])

    update_device(mac_id, count, rssi)

    return 'Success'

@app.route('/update_data', methods=['POST'])
def update_data():
    data = request.json
    mac_id = data['mac_id']
    count = int(data['average_count'])
    rssi = int(data['average_rssi'])

    update_device(mac_id, count, rssi)

    return jsonify(success=True)

if __name__ == '__main__':
    load_devices()
    app.run(debug=True)