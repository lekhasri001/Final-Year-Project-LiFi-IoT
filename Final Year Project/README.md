# Secured Emergency Healthcare Monitoring System Using Li-Fi

## 📌 Overview

This project presents a secure and real-time patient monitoring system using **Li-Fi** technology combined with **AES** and **RSA** encryption algorithms to ensure **confidentiality**, **integrity**, and **fast transmission** of sensitive healthcare data. It eliminates the risks of electromagnetic interference associated with Wi-Fi/Bluetooth, making it ideal for use in hospital environments.

---

## 💡 Features

- Real-time monitoring of vitals: **Heart rate, SpO₂, temperature, motion**
- Li-Fi-based wireless data transmission
- **AES** (Advanced Encryption Standard) for fast, symmetric encryption
- **RSA** (Rivest–Shamir–Adleman) for secure key exchange
- NIST Statistical Test Suite used to validate encryption randomness
- Portable and energy-efficient design using microcontrollers and sensors

---

## 🛠️ Technologies & Components

### 🔧 Hardware
- **Arduino Uno** – collects and transmits data
- **Raspberry Pi Pico W** – receives and decrypts data
- **MAX30100 Sensor** – heart rate & SpO₂
- **BMP Sensor** – temperature & pressure
- **MPU-6050** – motion and fall detection
- **LED** – Li-Fi transmitter
- **Solar Panel** – Li-Fi receiver
- **LCD** – displays health parameters

### 💻 Software
- **Arduino IDE**
- **Python** (for AES, RSA, NIST testing)
- **Cryptographic Libraries**: `pycryptodome`, `cryptography`
- **NIST Statistical Test Suite** for encryption randomness analysis

---

## 📁 Project Structure

Final Year Project /
├──  Main code/
│ ├── Receiver.py
│ └── sender.py
│
├── Nist code
│ └── nist 
│
├── diagrams
│   ├── Encryption output.jpg
|   ├── Decryption output.jpg
|   ├── Nist test output.jpg
|   ├── circuit.jpeg
│ 
├── Report.pdf 
└── README.md 


---

## ⚙️ How It Works

1. **Transmitter Side**
   - Arduino collects data from sensors.
   - Data is encrypted using **AES**.
   - AES key is encrypted using **RSA**.
   - Encrypted data + AES key are transmitted via **Li-Fi LED**.

2. **Receiver Side**
   - Raspberry Pi Pico W receives the modulated signal via **solar panel**.
   - AES key is decrypted using RSA private key.
   - Encrypted data is decrypted using the AES key.
   - Vital signs are displayed on the LCD screen.

---

## 🔐 Security Highlights

- **AES Encryption**: Fast, secure, and efficient for real-time data.
- **RSA Key Exchange**: Asymmetric encryption ensures secure transmission of the AES key.
- **NIST Testing**: Validates the randomness and security strength of encryption.
- **Dual-layer Security**: Prevents eavesdropping, MITM attacks, and data tampering.

---

## 📈 Sample Output

| Parameter        | Value       |
|------------------|-------------|
| Body Temp        | 36.5°C      |
| Heart Rate       | 80 bpm      |
| SpO₂             | 98%         |
| Motion (Accel)   | X: -1.2, Y: 0.2, Z: 9.0 m/s² |
| Orientation (Gyro)| X: -0.3, Y: 0.03, Z: 0.42 rps |

---

## 📊 NIST Test Results

All encryption outputs passed NIST randomness tests, confirming the **high entropy** and **security strength** of the encrypted sensor data.

---

## 👩‍💻 Authors

- **Jeya Vaarshini S**
- **Kavitha P**
- **Lekhasri M**
- **Madhushree K**

SRM Valliammai Engineering College  
Department of Electronics and Communication Engineering  
April 2025

---

## 📄 License

This project is intended for academic and educational purposes only.

---


