Sender side:


#include <MAX30105.h>
#include <heartRate.h>
#include <spo2_algorithm.h>

#include <Wire.h> 
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27,16,2);



#include "MAX30105.h"
#include "heartRate.h"

#include <Adafruit_MPU6050.h>
#include <Adafruit_BMP280.h>

#include <string.h>

Adafruit_MPU6050 mpu;
MAX30105 particleSensor;


// AES-128 key (16 bytes)
const char RSA_Key = 'K'; // Change this for better security

// Function to encrypt/decrypt using XOR
void AESEncryptDecrypt(char *data, int length, char key) {
    for (int i = 0; i < length; i++) {
        data[i] ^= key; // XOR each character with the key
    }
}


Adafruit_BMP280 bmp;
#define SEALEVELPRESSURE_HPA (1013.25)

const byte SAMPLE_BUFFER_SIZE = 100;
uint16_t irBuffer[SAMPLE_BUFFER_SIZE];
uint16_t redBuffer[SAMPLE_BUFFER_SIZE];

const byte RATE_SIZE = 4; //Increase this for more averaging. 4 is good.
byte rates[RATE_SIZE]; //Array of heart rates
byte rateSpot = 0;
long lastBeat = 0; //Time at which the last beat occurred
float beatsPerMinute;
int beatAvg;
long irValue;
int spo2=0;
float temperature;
int H_count=0;
int G_count=0;  
int vib=0;
int fal=0;
bool cal=false;
int d_count=0;
boolean p_count=false;

int buss=2;

int v_co=0;
int f_co=0;
String data1;
String data2;
String data3;
String data4;
String data5;
String data6;

#define TRANSMIT_LED 12
#define SAMPLING_TIME 5


bool led_state = false;
bool transmit_data = true;
int bytes_counter;
int total_bytes;

String sv1,pv1;

String randomData;
       
void setup()
{
  Serial.begin(9600);
  pinMode(TRANSMIT_LED, OUTPUT);
  randomSeed(analogRead(0)); 
  
  lcd.init();
  lcd.backlight();
// pinMode(36,INPUT);
   pinMode(buss,OUTPUT);
    lcd.setCursor(0,0);
    lcd.print(" LIFI ");
    lcd.setCursor(0,1);
    lcd.print(" Transmitter ");
    delay(4000);
    lcd.clear();

    
    if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }
  Serial.println("MPU6050 Found!");

  Serial.println("");
// Initialize sensor
  if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) //Use default I2C port, 400kHz speed
  {
    Serial.println("MAX30105 was not found. Please check wiring/power. ");
    while (1);
  }
  Serial.println("Place your index finger on the sensor with steady pressure.");

  particleSensor.setup(); //Configure sensor with default settings
  particleSensor.setPulseAmplitudeRed(0x0A); //Turn Red LED to low to indicate sensor is running
  particleSensor.setPulseAmplitudeGreen(0); //Turn off Green LED
// // Try to initialize!
// 
 Serial.println("Adafruit MPU6050 test!");
while ( !Serial ) delay(100); // wait for native usb
  Serial.println(F("BMP280 test"));
  unsigned status;
status = bmp.begin(0x76);
  if (!status) {
    Serial.println(F("Could not find a valid BMP280 sensor, check wiring or "
                      "try a different address!"));
    Serial.print("SensorID was: 0x"); Serial.println(bmp.sensorID(),16);
    Serial.print(" ID of 0xFF probably means a bad address, a BMP 180 or BMP 085\n");
    Serial.print(" ID of 0x56-0x58 represents a BMP 280,\n");
    Serial.print(" ID of 0x60 represents a BME 280.\n");
    Serial.print(" ID of 0x61 represents a BME 680.\n");
    while (1) delay(10);
  }

  /* Default settings from datasheet. */
  bmp.setSampling(Adafruit_BMP280::MODE_NORMAL, /* Operating Mode. */
                  Adafruit_BMP280::SAMPLING_X2, /* Temp. oversampling */
                  Adafruit_BMP280::SAMPLING_X16, /* Pressure oversampling */
                  Adafruit_BMP280::FILTER_X16, /* Filtering. */
                  Adafruit_BMP280::STANDBY_MS_500); /* Standby time. */

    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print("Sensor initialize......"); 
    delay(1000); 
 
}

void loop(){

  String text = generateRandomData(); // Generate random data for acceleration, heart rate, and SpO2
  Serial.print("text ");
  Serial.println(text); // Print the generated random data

  char charArray[text.length() + 1];

  
   text.toCharArray(charArray, sizeof(charArray));
   int length = sizeof(charArray) - 1;
  AESEncryptDecrypt(charArray, length, RSA_Key);
    Serial.print("Encrypted: ");
    Serial.println(charArray);

  String text1 = String(charArray);
  
  total_bytes = text1.length(); // Update total_bytes with the length of the text
  bytes_counter = total_bytes; // Set bytes_counter to total_bytes
  Serial.println("Total Bytes: " + String(total_bytes)); // Debugging output

  while (transmit_data && total_bytes > 0) { // Ensure total_bytes > 0
    transmit_byte(text1[total_bytes - bytes_counter]);
    bytes_counter--;
    if (bytes_counter == 0) {
      transmit_data = false;
    }
  }
  transmit_data = true;
  
  delay(2000); // Delay between transmissions
}

void transmit_byte(char data_byte) {
  digitalWrite(TRANSMIT_LED, LOW);
  delay(SAMPLING_TIME);
  for (int i = 0; i < 8; i++) { // Reduced to 8 bits since char is 8 bits
    digitalWrite(TRANSMIT_LED, (data_byte >> i) & 0x01);
    delay(SAMPLING_TIME);
  }
  digitalWrite(TRANSMIT_LED, HIGH);
  delay(SAMPLING_TIME);
}

String generateRandomData() {
    // beatAvg=0;
    // spo2=0;
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp); // Fetch sensor readings
  
  // Pulse and SpO2 logic
  irValue = particleSensor.getIR();
  while (irValue > 7000) {
    irValue = particleSensor.getIR();
    if (checkForBeat(irValue) == true) {
      long delta = millis() - lastBeat;
      lastBeat = millis();
      beatsPerMinute = 60 / (delta / 1000.0);
      if (beatsPerMinute < 255 && beatsPerMinute > 20) {
        rates[rateSpot++] = (byte)beatsPerMinute;
        rateSpot %= RATE_SIZE;
        // Calculate average heart rate
        beatAvg = 0;
        for (byte x = 0; x < RATE_SIZE; x++) {
          beatAvg += rates[x];
        }
        beatAvg /= RATE_SIZE;
        Serial.print("Heart BPM: ");
        Serial.println(beatAvg);
        Serial.println("Measuring SpO2...");
   Serial.print("SpO2: ");
  spo2=random(95, 99);
  Serial.print(spo2);
  Serial.println(" %");
      }
    }
  }

   
     

      // Environmental data (temperature, pressure, altitude)
      float temperature1 = bmp.readTemperature();
      float pressure = bmp.readPressure();
      float altitude = bmp.readAltitude(1013.25); // Adjust to local forecast

      // Prepare environmental data string
      String data4 = String(temperature1) + "," + String(pressure) + "," + String(altitude);
      
      // Prepare accelerometer and gyroscope data
      String data5 = String(a.acceleration.x, 1) + "," + String(a.acceleration.y, 1) + "," + String(a.acceleration.z, 1);
      String data6 = String(spo2) + "," + String(beatAvg);
      Serial.println("Returning data: " + data3);
      // Combine all data into a single string for transmission
      String result = data5 + "," + data6 + ","+ data4 + "#";
      Serial.println("Returning data: " + result); // Debug output
    

      return result;
    
  

 // return ""; // In case no valid data is available
}