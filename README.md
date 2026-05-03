# 🎙️ AcoustiChron

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-Active_Development-orange)
![Release](https://img.shields.io/badge/release-v1.1.0-purple)

**AcoustiChron** is an open-source Python suite designed for continuous, high-resolution environmental acoustic logging and time-series analysis. 

Built with calibrated measurement microphones (like the miniDSP UMIK-1) in mind, AcoustiChron captures real-time Sound Pressure Level (SPL) data at 1-second intervals. It streams this data asynchronously to **InfluxDB**, allowing you to monitor acoustics, track countermeasure effectiveness (like white noise or AGC), and visualize 30+ day trends in Grafana without dropping a single frame of audio.

## 📖 Overview

Standard SPL meters give you a snapshot of a moment in time, but environmental sound analysis requires an understanding of *trends*. AcoustiChron utilizes a thread-safe, non-blocking architecture to ensure continuous audio streaming. 

With the new built-in interactive console, users can manually tag acoustic events (e.g., "TV Playing", "HVAC On") in real-time. These tags are indexed natively in InfluxDB, allowing you to easily filter and visualize exactly how specific events impact the ambient noise floor (L90) and peak intrusive noise (L10) of your environment.

## ✨ Core Features

* **High-Resolution Real-Time Logging:** Captures and calculates RMS-to-dBFS sound pressure levels at 1-second resolution.
* **InfluxDB Native Integration:** Built from the ground up for Time-Series Databases. Capable of handling continuous 24/7 logging (2.6+ million rows/month) effortlessly.
* **Live Event Tagging:** An interactive background thread allows you to type notes into the console while logging is active, instantly appending tags to your database points.
* **Hardware Agnostic (UMIK-1 Optimized):** Works out-of-the-box with any USB measurement microphone. Features easily configurable calibration offsets.
* **Privacy First:** Only mathematical acoustic levels are stored. Raw audio is instantly discarded from RAM, ensuring compliance with privacy laws in offices or public spaces.

---

## 🛠️ Setup & Installation

### Prerequisites
* Python 3.8 or higher.
* A USB Measurement Microphone (e.g., miniDSP UMIK-1).
* Docker (for running a local instance of InfluxDB).

### 1. Install Python Dependencies
Clone this repository and install the required libraries:
```bash
git clone https://github.com/yourusername/acoustichron.git
cd acoustichron
pip install sounddevice numpy influxdb-client
```

### 2. Set Up InfluxDB (Local Edge Database)
The best way to run InfluxDB locally without hitting cloud rate limits is via Docker. Run this command to spin up an InfluxDB container:
```bash
docker run -p 8086:8086 -v influxdb2:/var/lib/influxdb2 influxdb:latest
```
1. Open your browser and navigate to `http://localhost:8086`.
2. Follow the setup wizard and create an Organization (e.g., `Acoustics_Lab`) and a Bucket (e.g., `acoustichron_data`).
3. Navigate to **Load Data > API Tokens** and generate an **All Access Token**. Copy this token.

*(Note: You can also use InfluxDB Cloud. See the wiki for cloud setup).*

### 3. Configure the Script
Open `logger.py` in your favorite text editor and update the configuration section:
```python
# UPDATE THESE VARIABLES IN logger.py
CALIBRATION_OFFSET = 100.0  # Find this in your mic's calibration file
INFLUX_TOKEN = "PASTE_YOUR_COPIED_TOKEN_HERE"
INFLUX_ORG = "Acoustics_Lab"
INFLUX_BUCKET = "acoustichron_data"
```

---

## 🚀 Usage

Start the logger by running:
```bash
python logger.py
```

**Live Event Tagging:**
While the script is running, you can type directly into the console to tag the acoustic environment.
* Type `White Noise Active` and press Enter. All subsequent logged seconds will carry this tag in InfluxDB.
* Type `clear` and press Enter to return to baseline logging.
* Press `Ctrl+C` to gracefully flush the database queue and exit.

**Visualizing the Data:**
Connect your InfluxDB instance to **Grafana**. Query the `spl_db` field and group by `event_tag` to instantly generate beautiful, color-coded line graphs of your acoustic environment!

---

## 🛣️ Roadmap

### Phase 1: Enhanced DSP & Storage (Current)
- [x] **Database Migration:** Replaced CSV logging with InfluxDB integration for robust, multi-month logging sessions.
- [x] **Live Tagging:** Added multi-threaded console input for manual acoustic event tracking.
- [ ] **Software Weighting Filters:** Implement digital A-Weighting (dBA) and C-Weighting (dBC) in Python using `scipy.signal`.

### Phase 2: Visualization & Alerting
- [ ] **Grafana Dashboard Templates:** Provide pre-configured JSON dashboards to instantly visualize L10, L90, and Leq trends.
- [ ] **Threshold Alerting System:** Webhook integrations (Slack/Discord) that trigger if rolling averages exceed noise ordinance limits.

### Phase 3: Advanced Acoustics & Machine Learning
- [ ] **Real-Time 1/3 Octave Band Analysis:** Log frequency-specific SPL alongside broadband levels to determine *what* is making the noise.
- [ ] **Edge AI Sound Classification:** Integration with TensorFlow Lite / YAMNet to locally classify and tag noise events automatically without saving raw audio.
