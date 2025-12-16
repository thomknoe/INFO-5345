# MIXI: Sentiment Analysis & Beverage Mixology

<mark> **Collaborators: Thomas Knoepffler, Carrie Wang, Julia Chen** </mark>

---

**\*\*\*1. Background\*\*\***

<mark>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</mark>

<p align="center">
<img src="https://github.com/thomknoe/INFO-5345/blob/Fall2025/Final%20Project/Images/MIXI_1.jpg" alt="MIXI 1" width="49.5%"/>
<img src="https://github.com/thomknoe/INFO-5345/blob/Fall2025/Final%20Project/Images/MIXI_2.jpg" alt="MIXI 2" width="49.5%"/>
<img src="https://github.com/thomknoe/INFO-5345/blob/Fall2025/Final%20Project/Images/MIXI_3.jpg" alt="MIXI 3" width="49.5%"/>
<img src="https://github.com/thomknoe/INFO-5345/blob/Fall2025/Final%20Project/Images/MIXI_4.jpg" alt="MIXI 4" width="49.5%"/>
</p>

<mark> _**Image Source:** Original MIXI Project, Design for Physical Interaction, Fall 2024._ </mark>

**\*\*\*2. User Interaction\*\*\***

<mark>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</mark>

![Storyboard](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Final%20Project/Diagrams/Storyboard.png)
![System Diagram](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Final%20Project/Diagrams/System_Diagram.png)

**\*\*\*3. Electronics Assembly\*\*\***

<mark>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</mark>

### <mark>Components</mark>

- <mark> Raspberry Pi 5 Model B/8GB </mark>
- <mark> (6) 5V Peristaltic Pump Motors </mark>
- <mark> 8-Channel 5V Relay </mark>
- <mark> Arduino Micro Pro </mark>
- <mark> Adafruit Mini PiTFT 1.14" 135x240 </mark>
- <mark> Adafruit I2C Stemma QT Rotary Encoder </mark>
- <mark> USB Webcam/Microphone </mark>
- <mark> Mini Bluetooth Speacker </mark>

![Electronics Assembly](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Final%20Project/Images/Electronics_Assembly.jpg)
![Componenent Diagram](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Final%20Project/Diagrams/Component_Diagram.png)

**\*\*\*4. Fluid Mechanisms\*\*\***

<mark>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</mark>

```
import time
import serial

SERIAL_PORT = "/dev/ttyACM0"
BAUD = 9600

PUMP_INDEX = 1          # the pump you calibrated
TARGET_OZ = 5.0         # calibration target

ser = serial.Serial(SERIAL_PORT, BAUD, timeout=1)
time.sleep(2)

print("Starting calibration...")
print(f"Pump {PUMP_INDEX} ON — press ENTER when cup reaches {TARGET_OZ} fl oz")

start_time = time.time()

# Start pump
ser.write(f"ON {PUMP_INDEX}\n".encode())

input()  # you press enter manually when cup hits 5 oz

# Stop pump
ser.write(f"OFF {PUMP_INDEX}\n".encode())

elapsed = time.time() - start_time

print(f"Elapsed time: {elapsed:.2f} seconds")
```

| Parameter              | Value                          |
| ---------------------- | ------------------------------ |
| Target volume          | 5 fl oz                        |
| Target volume (metric) | 148 mL                         |
| Measured fill time     | 6.77 seconds                   |
| Flow rate              | 21.877 mL / second             |
| Time per mL            | 45.7 ms / mL                   |
| Pump consistency       | All pumps assumed equivalent   |
| Tubing state           | Pre-filled (continuous column) |

![Calibration](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Final%20Project/GIFs/Calibration.gif)

**\*\*\*5. Beverage Logic\*\*\***

<mark>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</mark>

![Menu 1](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Final%20Project/Graphics/Menu_1.png)
![Menu 2](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Final%20Project/Graphics/Menu_2.png)

**\*\*\*6. Coding Stack\*\*\***

<mark>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</mark>

![UML Diagram](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Final%20Project/Diagrams/UML_Diagram.png)

**\*\*\*7. Form Factor\*\*\***

<mark>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</mark>

<p align="center">
<img src="https://github.com/thomknoe/INFO-5345/blob/Fall2025/Final%20Project/Images/Inspiration_1.jpg" alt="Inspiration 1" width="49.5%"/>
<img src="https://github.com/thomknoe/INFO-5345/blob/Fall2025/Final%20Project/Images/Inspiration_2.jpg" alt="Inspiration 2" width="49.5%"/>
</p>

<mark> _**Image Source:** Lorem Ipsum._ </mark>

**\*\*\*8. Technical Drawings\*\*\***

<mark>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</mark>

![Technical Sections](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Final%20Project/Diagrams/Technical_Sections.png)
![Technical Isometric](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Final%20Project/Diagrams/Technical_Isometric.png)

**\*\*\*9. Full Assembly\*\*\***

<mark>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</mark>

![Assembly 1](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Final%20Project/Images/Assembly_1.jpg)
![Assembly 2](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Final%20Project/Images/Assembly_2.jpg)
![Assembly 3](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Final%20Project/Images/Assembly_3.jpg)
![Assembly 4](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Final%20Project/Images/Assembly_4.jpg)
![Assembly 5](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Final%20Project/Images/Assembly_5.jpg)
![Assembly 6](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Final%20Project/Images/Assembly_6.jpg)
![Assembly 7](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Final%20Project/Images/Assembly_7.jpg)
![Assembly 8](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Final%20Project/Images/Assembly_8.jpg)
![Assembly 9](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Final%20Project/Images/Assembly_9.jpg)
![Assembly 10](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Final%20Project/Images/Assembly_10.jpg)

**\*\*\*10. Demo\*\*\***

<mark>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</mark>

![Demo 1](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Final%20Project/GIFs/Demo_1.gif)
![Demo 2](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Final%20Project/GIFs/Demo_2.gif)

![Showcase 1](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Final%20Project/Images/Showcase_1.jpg)
![Showcase 2](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Final%20Project/Images/Showcase_2.jpg)
![Showcase 3](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Final%20Project/Images/Showcase_3.jpg)

**\*\*\*11. Reflections\*\*\***

<mark>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</mark>

**\*\*\*12. Conclusions\*\*\***

<mark>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</mark>

<mark> Collaborators: Thomas Knoepffler (Digital Fabrication & Assembly), Carrie Wang (3D Modeling & User Experience), Julia Chen (Hardware & Software Engineer) </mark>

<p align="center">
<img src="https://github.com/thomknoe/INFO-5345/blob/Fall2025/Final%20Project/Images/Bonus_1.jpg" alt="Bonus 1" width="33%"/>
<img src="https://github.com/thomknoe/INFO-5345/blob/Fall2025/Final%20Project/Images/Bonus_2.jpg" alt="Bonus 2" width="33%"/>
<img src="https://github.com/thomknoe/INFO-5345/blob/Fall2025/Final%20Project/Images/Bonus_3.jpg" alt="Bonus 3" width="33%"/>
</p>
