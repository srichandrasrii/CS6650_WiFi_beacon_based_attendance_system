# CS6650_WiFi_frames_based_attendance_system
This is our final project submission for Professor Ayon Chakraborty's course on sensing systems of IoT.

We have built a semi-automated way to mark attendance using WiFi frames emitted from students’ smartphones. 
Our solution leverages the proliferation of smartphones in universities and the use of WiFi technology, to mark students’ attendance automatically.

You can clone this repository with :
    
    git clone https://github.com/srichandrasrii/CS6650_WiFi_beacon_based_attendance_system.git

<br>

<h2> Our system </h2>
There are totally 3 parts to the system:

1. Esp8266/NodeMCU (or any other esp microcontroller with WiFi module)
2. Raspberry Pi
3. Laptop and mobile devices

<br>

<h3> ESP8266/NodeMCU </h3>

The esp8266/NodeMCU is a small yet powerful tool to sniff out WiFi packets/frames and process them to give us of information on the packet like Frame control, Duration, Source and destination address, BSSID, Sequence control, Frame Body, Frame check sequence. Our primary focus will be on the Source Address.</br>

</br>

<h3> Configuring and running the NodeMCU </h3>

1. Install the Arduino IDE (you can use any other IDE of your choice)
2. Download the neccesary board libraries (Nodemcu 1.0).
3. Attach the Nodemcu via USB. In the Arduino IDE, choose the appropriate port and board. Ensure to set the baud rate to 115200.
4. The code which has to be run on the Nodemcu resides in ./CS6650/esp32_promiscous
5. Upload the promiscous.ino file to the Nodemcu

Your Nodemcu will be able to sniff packets and send the data to its serial interface! :)


<br>


<h3> Configuring and running the Raspberry Pi </h3>
There are many things to be configured in the raspberry pi. We will break it down as follows:

1. Setting up the RPI: The raspberry pi should ideally have latest version of supported ubuntu installed. Also the username and password of the RPI should be remembered. By default it is, Username = "raspberrypi", Password = "raspberry". To connect the RPI to the laptop using headless mode, you need to find the IP address of the RPi and then use ssh to connect RPI terminal to your terminal. <br> [Useful resource to find IP address of RPI.](https://howchoo.com/pi/find-your-raspberry-pis-ip-address)


2. Creating the files on RPI: Once you connect to the RPI through laptop using ssh, create the files and directories as structured here on github. You can directly use git to download the folder on RPI or you can do it manually by creating all the files.

3. Installing all necessary packages: We are using flask as our web server which is being hosted locally. So make sure that flask is installed on the RPI. Also make sure if Pyserial, csv packages are installed on the RPI. Also, we have used `screen` to run multiple programs at once on the RPI. So you need to make sure 'screen' is also installed as well.

4. Changes in code: Don't forget to change the `api_url` in ```main.py``` and `host` in 
    
        app.run(host='192.168.151.148', port=5000, debug=True)``` 
    
    according to the IP address of your RPI and the port used for the webapplication. Do add your MACIDs, name, roll number in the `registered_devices.csv`.


<h4> Running the programs: </h4>

1. Connect via SSH to the RPI.</br>
2. Use `screen` to create the first terminal. </br>
3. Go the directory `CS6650/website` and run `app.py` to run the localhost server. </br>
4. Now create new terminal by entering `Ctrl+A and then press C`. A new terminal will be opened. Now go to the directory `CS6650` and run `main.py` to complete the process. You will see messages saying `"Data sent successfully to Flask app!"` if the program is running as intended (if you have added the MACID of atleast one device to registered_devices.)</br>


[Resource to understand using 'screen'](https://linuxize.com/post/how-to-use-linux-screen)

<h3> Laptop and mobile devices </h3>
The laptop is mostly used to setup the RPI, connect via SSH and run the python scripts. But the laptop and also other mobile devices can open the webserver by joining the same network which the RPI is connected to and go to http://192.168.x.x:5000 where (192.168.x.x) is the IP address of the RPI and '5000' is the port used in connection. </br></br>

This way you can see the registered data on the website from any device as long as you are connected to the same network as RPI. To see the updated statistics, you need to refresh the page. To add a new registration, fill the form and click submit, the data will be added to the csv file and will be shown on the website.
On the website you can see the entries of different registered people including their names, Roll number, average_count, average_RSSI, status (present/absent).

Note: A copy of logged data can be found in ./CS6650/data_log.txt (Its about 11MB in size).