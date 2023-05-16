# CS6650_WiFi_frames_based_attendance_system
This is our final project submission for Professor Ayon Chakraborty's course on sensing systems of IoT.

We have built a semi-automated way to mark attendance using WiFi frames emitted from students’ smartphones. 
Our solution leverages the proliferation of smartphones in universities and the use of WiFi technology, to mark students’ attendance automatically.

<h2> How to run the system </h2>
There are totally 3 parts to the system:
1) Esp32/NodeMCU (or any other esp microcontroller with WiFi module)
2) Raspberry Pi 
3) Laptop and mobile devices

<h3> ESP32/NodeMCU </h3>
The esp32/NodeMCU is a small yet powerful tool to sniff out WiFi packets/frames and process them to give us a lot of information like Frame control, Duration, Source and destination address, BSSID, Sequence control, Frame Body, Frame check sequence. We don't need all this data for this project, but can be used for other use cases.</br>
</br>

   So firstly the libraries 'esppl_functions.h' and 'esppl_struct.h' need to be in the same folder as the .ino file. Before running the program make sure the necessary board libraries are downloaded and if the port and board selected are correct. Also make sure that the baud rate chosen matches the one in the code (115200).
   
   On running the program the esp32 will serially send data to whatever device it is connected to. (either laptop/Rpi). You can check if the program is working as intended on the laptop. The program should print the FT, FST, SRC, DEST, RSSI values continuosly. Note that the esp32 running in promiscous mode doesn't need to connect to WiFi. Also you may encounter error that says you don't access to USB0, then run the command:
    `sudo chmod 777 /dev/ttyusb0`

<h3> Raspberry Pi </h3>
There are many things to be configured in the raspberry pi. I will break it down as follows:

<h4> Setting up the RPI: </h4> The raspberry pi should ideally have latest version of supported ubuntu installed. Also the username and password of the RPI should be remembered. By default it is Username = "raspberrypi", Password = "raspberry". To connect the RPI to the laptop using headless mode, you need to find the ip address of the rpi and then use ssh to connect RPI terminal to your terminal.

[Useful resource to find ip address of RPI](https://howchoo.com/pi/find-your-raspberry-pis-ip-address)

<h4> Creating the files on RPI :</h4> Once you connect to the RPI through laptop using ssh, create the files and directories as structured here on github. You can directly use git to download the folder on RPI or you can do it manually by creating all the files.

<h4> Installing all necessary packages :</h4> We are using flask as our web server which is being hosted locally. So make sure that flask is installed on the RPI. Also make sure if Pyserial, csv packages are installed on the RPI. Also I have used `screen` to run multiple programs at once on the RPI. So you need to make sure 'screen' is also installed as well.

<h4> Changes in code: </h4> Don't forget to change the `api_url` in ```main.py``` and `host` in ```app.run(host='192.168.151.148', port=5000, debug=True)``` according to the IP address of your RPI and the port used for the webapplication. Do add your MACIDs, name, roll number in the `registered_devices.csv`.

<h4> Running the programs: </h4>
1) Connect via SSH to the RPI.</br>
2) Use `screen` to create the first terminal. </br>
3) Go the directory `CS6650/website` and run `app.py` to run the localhost server. </br>
4) Now create new terminal by entering `Ctrl+A and then press C`. A new terminal will be opened. Now go to the directory `CS6650` and run `main.py` to complete the process. You will see messages saying `"Data sent successfully to Flask app!"` if the program is running as intended (if you have added the MACID of atleast one device to registered_devices.</br>


[Resource to understand using 'screen'](https://linuxize.com/post/how-to-use-linux-screen)

<h3> Laptop and mobile devices </h3>
The laptop is mostly used to setup the RPI, connect via SSH and run the python scripts. But the laptop and also other mobile devices can open the webserver by joining the same network which the RPI is connected to and go to the website http://192.168.x.x:5000 where (192.168.x.x) is the ip address of the RPI and '5000' is the port used in connection. </br></br>

This way you can see the registered data on the website from any device as long as you are connected to the same network as RPI. To see the updated statistics, you need to refresh the page. To add a new registration, fill the form and click submit, the data will be added to the csv file and will be shown on the website.
On the website you can see the entries of different registered people including their names, Roll number, average_count, average_RSSI, status (present/absent).

