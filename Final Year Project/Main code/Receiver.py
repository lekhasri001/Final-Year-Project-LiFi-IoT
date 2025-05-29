Receiver side :

#include <LiquidCrystal_I2C.h>
#define LDR_PIN 26 
#define SAMPLING_TIME 5

float values[10]; // Array to store parsed values
int index1 = 0;

LiquidCrystal_I2C lcd(0x27, 16, 2);

const char RSA_Key = 'K'; // Change this for better security

// Function to encrypt/decrypt using XOR
void AESEncryptDecrypt(char *data, int length, char key) {
    for (int i = 0; i < length; i++) {
        data[i] ^= key; // XOR each character with the key
    }
}

bool led_state = false;
bool previous_state = true;
bool current_state = true;
char buff[100];
String dataBuffer = ""; // Buffer to store the incoming data
int lcdLine = 0; // Track which line of the LCD to print on

void setup()
{
  Serial.begin(9600);
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print(" LIFI ");
  lcd.setCursor(0, 1);
  lcd.print(" Receiver ");
  delay(2000);
  lcd.clear();
}

void loop()
{
   
 current_state = get_ldr();

  if (!current_state && previous_state) {
    char receivedChar = get_byte();

    // Only consider printable characters
    if (isPrintable(receivedChar)) {
      Serial.print(receivedChar);
      dataBuffer += receivedChar; // Append to buffer
    }

    if (receivedChar == 'h') { // End of data stream
      Serial.println();

      // Convert String to char array
      char charArray[dataBuffer.length() + 1];
      dataBuffer.toCharArray(charArray, sizeof(charArray));
      int length = strlen(charArray); // Safer than sizeof(charArray)-1

      // Decrypt
      AESEncryptDecrypt(charArray, length, RSA_Key);

      // Output results
      Serial.print("Decrypted: ");
      Serial.println(charArray);
      parseCharArray(charArray);

      // Display on LCD
      lcd.clear();
      lcd.setCursor(0, 0);
      
      Serial.println(values[0]);
      Serial.println(values[1]);
      Serial.println(values[2]);
      Serial.println(values[3]);
      Serial.println(values[4]);
      Serial.println(values[5]);
      Serial.println(values[6]);
      Serial.println(values[7]);
      lcd.print("X,Y,Z:");
      lcd.print(String(values[0]));
       lcd.print(",");
      lcd.print(String(values[1]));
      lcd.setCursor(0, 1);
       lcd.print(",");
      lcd.print(String(values[2]));
      delay(500);

      lcd.clear();
      lcd.setCursor(0, 0);

      lcd.print("SPO2,HeartRate:");
      lcd.setCursor(0, 1);
      lcd.print(String(values[3]));
       lcd.print(",");
      lcd.print(String(values[4]));
      
  
      delay(500);
      lcd.clear();
      lcd.setCursor(0, 0);

      lcd.print("Temp.,Pressure.");
       lcd.setCursor(0, 1);
      lcd.print(String(values[5]));
       lcd.print(",");
      lcd.print(String(values[6]));
      delay(500);

      lcd.clear();
      lcd.setCursor(0, 0);
        lcd.print("Altitude");
       lcd.setCursor(0, 1);
       lcd.print(String(values[7]));

      
      


      // Clear buffer for next message
      dataBuffer = "";
    }
  }

  previous_state = current_state;
  
}

bool get_ldr()
{
  bool val = analogRead(LDR_PIN) > 300 ? true : false; //500
  return val; 
}

char get_byte()
{
  char data_byte = 0;
  delay(SAMPLING_TIME * 1.5);
  for (int i = 0; i < 8; i++)
  {
    data_byte |= (char)get_ldr() << i;
    delay(SAMPLING_TIME);
  }
  return data_byte;
}

void parseCharArray(char* input) {
    int index1 = 0; 
  char* token = strtok(input, ","); // Split by comma

  while (token != NULL && index1 < 10) {
    values[index1++] = atof(token); // Convert token to int
    token = strtok(NULL, ","); // Move to next token
  }
}

void splitAndDisplayData(String data)
{
  int firstCommaIndex = data.indexOf(',');
  String bp = data.substring(0, firstCommaIndex);

  int secondCommaIndex = data.indexOf(',', firstCommaIndex + 1);
  String spo2 = data.substring(firstCommaIndex + 1, secondCommaIndex);

  int thirdCommaIndex = data.indexOf(',', secondCommaIndex + 1);
  String ax = data.substring(secondCommaIndex + 1, thirdCommaIndex);
  
  int fourthCommaIndex = data.indexOf(',', thirdCommaIndex + 1);
  String ay = data.substring(thirdCommaIndex + 1,fourthCommaIndex); // The rest of the string after the last comma
 
   int fifthCommaIndex = data.indexOf(',', fourthCommaIndex + 1);
  String az = data.substring(fourthCommaIndex + 1,fifthCommaIndex);
  
  int sixthCommaIndex = data.indexOf(',', fifthCommaIndex + 1);
  String gx = data.substring(fifthCommaIndex + 1,sixthCommaIndex);
  
  int seventhCommaIndex = data.indexOf(',', sixthCommaIndex + 1);
  String gy = data.substring(sixthCommaIndex + 1,seventhCommaIndex);

  int eightCommaIndex = data.indexOf(',', seventhCommaIndex + 1);
  String gz = data.substring(seventhCommaIndex + 1,eightCommaIndex);

  int ninthCommaIndex = data.indexOf(',', eightCommaIndex + 1);
  String TEM = data.substring(eightCommaIndex + 1, ninthCommaIndex);
  
  int tenthCommaIndex = data.indexOf(',', ninthCommaIndex + 1);
  String PRE = data.substring(ninthCommaIndex + 1, tenthCommaIndex);

  int levelthCommaIndex = data.indexOf(',', tenthCommaIndex + 1);
  String ALT = data.substring(tenthCommaIndex + 1, levelthCommaIndex);

// Printing the values to verify
Serial.println("BP: " + bp);
//Serial.println("SpO2: " + spo2);
//Serial.println("AX: " + ax);
//Serial.println("AY: " + ay);
//Serial.println("AZ: " + az);
//Serial.println("GX: " + gx);
//Serial.println("GY: " + gy);
//Serial.println("GZ: " + gz);

  // Displaying on LCD
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("BPM: ");