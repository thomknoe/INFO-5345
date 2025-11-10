# Distributed Interaction

<mark> **Collaborators: Thomas Knoepffler, Carrie Wang, Xiaocheng Li, Julia Chen** </mark>

---

<details>
	<summary><strong>Prep</strong></summary>

## Prep

1. Pull the new changes
2. Read: [The Presence Table](https://dl.acm.org/doi/10.1145/1935701.1935800) ([video](https://vimeo.com/15932020))

</details>

<details>
	<summary><strong>Overview</strong></summary>

## Overview

Build interactive systems where **multiple devices communicate over a network** using MQTT messaging. Work in teams of 3+ with Raspberry Pis.

**Parts:**

- A: Learn MQTT messaging
- B: Try collaborative pixel grid demo
- C: Build your own distributed system

</details>

---

<details>
	<summary><strong>Part A: MQTT Messaging</strong></summary>

## Part A: MQTT Messaging

MQTT = lightweight messaging for IoT. Publish/subscribe model with central broker.

**Concepts:**

- **Broker**: `farlab.infosci.cornell.edu:1883`
- **Topic**: Like `IDD/bedroom/temperature` (use `#` wildcard)
- **Publish/Subscribe**: Send and receive messages

**Install MQTT tools on your Pi:**

```bash
sudo apt-get update
sudo apt-get install -y mosquitto-clients
```

**Test it:**

**Subscribe to messages (listener):**

```bash
mosquitto_sub -h farlab.infosci.cornell.edu -p 1883 -t 'IDD/#' -u idd -P 'device@theFarm'
```

**Publish a message (sender):**

```bash
mosquitto_pub -h farlab.infosci.cornell.edu -p 1883 -t 'IDD/test/yourname' -m 'Hello!' -u idd -P 'device@theFarm'
```

> **💡 Tips:**
>
> - Replace `yourname` with your actual name in the topic
> - Use single quotes around the password: `'device@theFarm'`

**🔧 Debug Tool:** View all MQTT messages in real-time at `http://farlab.infosci.cornell.edu:5001`

![MQTT Explorer showing messages](imgs/MQTT-explorer.png)

</details>

**\*\*\*Brainstorm 5 ideas for messaging between devices\*\*\***

| #     | Concept                                | Description / Interaction                                                                                                                                                                  |
| ----- | -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **1** | <mark>Telepresent Emotion Cubes</mark> | <mark>Small acrylic cubes that glow in colors matching remote users’ facial or vocal emotion. FER-based emotion detection → MQTT broadcast → LED diffusion through frosted acrylic.</mark> |
| **2** | Mood Beacon Lamps                      | Cylindrical desk lights that collectively visualize shared team mood. Users tap the lamp to select emotion; color syncs with others via MQTT topics for ambient awareness.                 |
| **3** | Pulse Orbs                             | Handheld diffused lights that emit rhythmic glow mirroring a user’s heartbeat. Heart rate sensor normalizes pulse → brightness modulation to create calm biofeedback loops.                |
| **4** | Weather Spirits                        | Portable diffused lights reflecting remote environmental data (like sunlight or weather). Cloud API maps temperature and condition data to animated color gradients.                       |
| **5** | Memory Stones                          | Acrylic diffusers that store and replay past collective color states. Shared color history replays as a soft gradient loop representing group continuity over time.                        |

<mark> _**AI Usage:** Utilized assistance from ChatGPT for ideation and generation._ </mark>

---

<details>
	<summary><strong>Part B: Collaborative Pixel Grid</strong></summary>

## Part B: Collaborative Pixel Grid

Each Pi = one pixel, controlled by RGB sensor, displayed in real-time grid.

**Architecture:** `Pi (sensor) → MQTT → Server → Web Browser`

**Setup:**

1. **Sensor**

#### Light/Proximity/Gesture sensor (APDS-9960)

We use this sensor [Adafruit APDS-9960](https://www.adafruit.com/product/3595) for this exmaple to detect light (also RGB)

<img src="https://cdn-shop.adafruit.com/970x728/3595-06.jpg" width=200>

Connect it to your pi with Qwiic connector

<img src="imgs/IMG_0270.jpg" height="200" />
We need to use the screen to display the color detection, so we need to stop the running piscreen.service to make your screen available again

```bash
# stop the screen service
sudo systemctl stop piscreen.service
```

if you want to restart the screen service

```bash
# start the screen service
sudo systemctl start piscreen.service
```

2. **Server** (one person on laptop):

```bash
cd "Lab 6"
source .venv/bin/activate
pip install -r requirements-server.txt
python app.py
```

2. **View in browser:**

   - Grid: `http://farlab.infosci.cornell.edu:5000`
   - Controller: `http://farlab.infosci.cornell.edu:5000/controller`

3. **Pi publisher** (everyone on their Pi):

```bash
# First time setup - create virtual environment
cd "Lab 6"
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-pi.txt

# Run the publisher
python pixel_grid_publisher.py
```

Hold colored objects near sensor to change your pixel!

![Pixel grid with two devices](imgs/two-devices-grid.png)

</details>

**\*\*\*Include: Screenshot of grid + photo of your Pi setup\*\*\***

![Colors Command](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%206/Images/Part_1/Colors_Command.jpg)
![Pi](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%206/Images/Part_1/Pi.jpg)

<p align="center">
	<img src="https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%206/Images/Part_1/Colors_Screen.jpg" alt="Colors Screen" width="100%"/>
	<img src="https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%206/Images/Part_1/Colors_3.jpg" alt="Colors 3" width="33%"/>
	<img src="https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%206/Images/Part_1/Colors_2.jpg" alt="Colors 2" width="33%"/>
	<img src="https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%206/Images/Part_1/Colors_1.jpg" alt="Colors 1" width="33%"/>
</p>

---

<details>
	<summary><strong>Part C: Make Your Own</strong></summary>

## Part C: Make Your Own

**Requirements:**

- 3+ people, 3+ Pis
- Each Pi contributes sensor input via MQTT
- Meaningful or fun interaction

**Ideas:**

**Sensor Fortune Teller**

- Each Pi sends 0-255 from different sensor
- Server generates fortunes from combined values

**Frankenstories**

- Sensor events → story elements (not text!)
- Red = danger, gesture up = climbed, distance <10cm = suddenly

**Distributed Instrument**

- Each Pi = one musical parameter
- Only works together

**Others:** Games, presence display, mood ring

</details>

**\*\*\*1. Project Description\*\*\***

- What does it do? Why interesting? User experience?

**\*\*\*2. Architecture Diagram\*\*\***

- Hardware, connections, data flow
- Label input/computation/output

**\*\*\*3. Build Documentation\*\*\***

![Parts](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%206/Images/Part_2/Parts.jpg)

![Electronics](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%206/Images/Part_2/Electronics.jpg)

![Mockups 1](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%206/Images/Part_2/Mockups_5.jpg)
![Mockups 2](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%206/Images/Part_2/Mockups_4.jpg)
![Mockups 3](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%206/Images/Part_2/Mockups_3.jpg)
![Mockups 4](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%206/Images/Part_2/Mockups_2.jpg)
![Mockups 5](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%206/Images/Part_2/Mockups_1.jpg)

**\*\*\*4. User Testing\*\*\***

![Live Feed 1](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%206/Images/Part_2/Live_Feed_1.gif)
![Live Feed 2](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%206/Images/Part_2/Live_Feed_2.gif)

<p align="center">
	<img src="https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%206/Images/Part_2/Testing_Group.jpg" alt="Testing Group" width="100%">
	<img src="https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%206/Images/Part_2/Testing_1.jpg" alt="Testing 1" width="49.5%"/>
	<img src="https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%206/Images/Part_2/Testing_2.jpg" alt="Testing 2" width="49.5%"/>
	<img src="https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%206/Images/Part_2/Testing_3.jpg" alt="Testing 3" width="49.5%"/>
	<img src="https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%206/Images/Part_2/Testing_4.jpg" alt="Testing 4" width="49.5%"/>
</p>

**\*\*\*5. Reflection\*\*\***

- What worked well?
- Challenges with distributed interaction?
- How did sensor events work?
- What would you improve?

---

<details>
	<summary><strong>Code Files</strong></summary>

## Code Files

**Server files:**

- `app.py` - Pixel grid server (Flask + WebSocket + MQTT)
- `mqtt_viewer.py` - MQTT message viewer for debugging
- `mqtt_bridge.py` - MQTT → WebSocket bridge
- `requirements-server.txt` - Server dependencies

**Pi files:**

- `pixel_grid_publisher.py` - Example (RGB sensor → MQTT)
- `requirements-pi.txt` - Pi dependencies

**Web interface:**

- `templates/grid.html` - Pixel grid display
- `templates/controller.html` - Color picker
- `templates/mqtt_viewer.html` - Message viewer

</details>

---

<details>
	<summary><strong>Debugging Tools</strong></summary>

## Debugging Tools

**MQTT Message Viewer:** `http://farlab.infosci.cornell.edu:5001`

- See all MQTT messages in real-time
- View topics and payloads
- Helpful for debugging your own projects

**Command line:**

```bash
# See all IDD messages
mosquitto_sub -h farlab.infosci.cornell.edu -p 1883 -t "IDD/#" -u idd -P "device@theFarm"
```

</details>

---

<details>
	<summary><strong>Troubleshooting</strong></summary>

## Troubleshooting

**MQTT:** Broker `farlab.infosci.cornell.edu:1883`, user `idd`, pass `device@theFarm`

**Sensor:** Check `i2cdetect -y 1`, APDS-9960 at `0x39`

**Grid:** Verify server running, check MQTT in console, test with web controller

**Pi venv:** Make sure to activate: `source .venv/bin/activate`

</details>

---

<details>
	<summary><strong>Submission Checklist</strong></summary>

## Submission Checklist

Before submitting:

- [ ] Delete prep/instructions above
- [ ] Add YOUR project documentation
- [ ] Include photos/videos/diagrams
- [ ] Document user testing with non-team members
- [ ] Add reflection on learnings
- [ ] List team names at top

**Your README = story of what YOU built!**

</details>

---

<mark> Collaborators: Thomas Knoepffler (Assembly & Fabrication), Carrie Wang (Hardware & Systems), Xiaocheng Li (Tester & Facilitator), Julia Chen (Developer & Debugger) </mark>

![Bonus](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%206/Images/Bonus.jpg)

<details>
	<summary><strong>Resources</strong></summary>

Resources: [MQTT Guide](https://www.hivemq.com/mqtt-essentials/) | [Paho Python](https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php) | [Flask-SocketIO](https://flask-socketio.readthedocs.io/)

</details>
