# include "./esppl_functions.h" 

void cb(esppl_frame_info *info) {
  String destination = ""; // variable to store the destination address
  String source = ""; // varaible to store the source address
  char addr_hex[1]; // 1 byte of data 
  
  // Converting receiver and source addresses to hex strings (6 byte MAC ID)
  for (int i = 0; i < 6; i++){
    sprintf(addr_hex, "%02x", info->receiveraddr[i]); // function for converting a int to hexadecimal
    destination.concat(addr_hex);
    sprintf(addr_hex, "%02x", info->sourceaddr[i]);
    source.concat(addr_hex);
  }

  // Sending data to RPI using serial communication
  Serial.print("\n");
  // Frame type
  Serial.print("FT: ");  
  Serial.print((int) info->frametype);
  // Frame subtype
  Serial.print(" FST: ");  
  Serial.print((int) info->framesubtype);
  // Source MAC ID
  Serial.print(" SRC: ");
  for (int i = 0; i < 6; i++) Serial.printf("%02x", info->sourceaddr[i]);
  // Destination MAC ID (0xffffffffffff for open broadcast)
  Serial.print(" DEST: ");
  for (int i = 0; i < 6; i++) Serial.printf("%02x", info->receiveraddr[i]);
  // Signal strength
  Serial.print(" RSSI: ");
  Serial.print(info->rssi);

  // SSID of WiFi router
  if (info->ssid_length > 0) {
    Serial.print(" SSID: ");
    for (int i = 0; i < info->ssid_length; i++) Serial.print((char) info->ssid[i]);    
  }

  // Resetting the variables to be used again in next frame
  destination = ""; 
  source = "";
}

void setup() {
  delay(500);
  Serial.begin(115200);
  esppl_init(cb); // callback function which runs everytime after a frame is processed
}

void loop() {
  esppl_sniffing_start(); // start sniffing for frames
  while (true) {
    // iterating through all the different channels present in WiFi
    for (int i = 1; i < 15; i++ ) {
      esppl_set_channel(i);
      while (esppl_process_frames()) { // waiting to process the frame
        delay(1000); // delay added to reduce load on rpi for receiving and processing the data realtime
      }
    }
  }  
}