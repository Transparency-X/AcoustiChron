### Project Name: **AcoustiChron**
*(A portmanteau of "Acoustics" and "Chronos", representing the continuous, long-term measurement of sound over time.)*

---

# 🎙️ AcoustiChron

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-Active_Development-orange)

**AcoustiChron** is an open-source Python suite designed for continuous, high-resolution environmental acoustic logging and time-series analysis. 

Built with calibrated measurement microphones (like the miniDSP UMIK-1) in mind, AcoustiChron captures real-time Sound Pressure Level (SPL) data at 1-second intervals and aggregates it into human-readable acoustic metrics. Whether you are monitoring neighborhood noise pollution, optimizing office acoustics, or studying sleep environments over a 30-day period, AcoustiChron provides the high-fidelity data you need.

## 📖 Overview

Standard SPL meters give you a snapshot of a moment in time, but environmental sound analysis requires an understanding of *trends*. AcoustiChron utilizes a thread-safe architecture to ensure continuous audio streaming while seamlessly logging data to disk without dropping frames. 

Included is a powerful data-processing pipeline that utilizes `pandas` to take millions of high-resolution data points and automatically calculate industry-standard metrics—such as **Background Noise (L90)**, **Intrusive Noise (L10)**, and **Maximum Peaks (Lmax)**—across 15-minute, hourly, daily, weekly, and monthly timeframes.

## ✨ Core Features

* **High-Resolution Real-Time Logging:** Captures and calculates RMS-to-dBFS sound pressure levels at 1-second resolution using non-blocking background threads.
* **Hardware Agnostic (UMIK-1 Optimized):** Works out-of-the-box with any USB measurement microphone. Features easily configurable calibration offsets to match your mic's individual sensitivity file.
* **Automated Trend Aggregation:** Instantly condense millions of rows of data into actionable timeframes (15m, 1hr, 8hr, 24hr, 7d, 30d).
* **Industry-Standard Acoustic Metrics:**
  * **Leq:** The equivalent continuous sound level (average acoustic energy).
  * **L10:** The sound level exceeded 10% of the time (Intrusive noise peak measure).
  * **L90:** The sound level exceeded 90% of the time (True background/ambient noise).
  * **Lmax / Lmin:** Absolute maximum and minimum sound levels recorded in the timeframe.
* **Privacy First:** Only mathematical acoustic levels are stored. Raw audio is immediately discarded from RAM, ensuring compliance with privacy laws in offices or public spaces.

---

## 🚀 Roadmap of Future Features

AcoustiChron is currently in **v1.0.0**. Our vision is to evolve it from a highly capable script into a fully containerized edge-computing appliance. 

### Phase 1: Enhanced DSP & Storage (v1.1 - v1.5)
- [ ] **Software Weighting Filters:** Implement digital A-Weighting (dBA) and C-Weighting (dBC) directly in Python using `scipy.signal` to emulate human hearing and low-frequency HVAC rumble accurately.
- [ ] **Database Migration:** Replace CSV logging with an SQLite database integration for faster querying and better stability over multi-month logging sessions.
- [ ] **Headless Auto-Start:** Create `systemd` service templates to allow AcoustiChron to run flawlessly as a headless appliance on a Raspberry Pi.

### Phase 2: Visualization & Alerting (v2.0)
- [ ] **Time-Series Database Integration:** Native support for writing directly to **InfluxDB** or **Prometheus**.
- [ ] **Grafana Dashboard Templates:** Pre-configured JSON dashboards allowing users to visualize 1-second resolution metrics, pan, and zoom through months of data via a web browser.
- [ ] **Threshold Alerting System:** Webhook integrations (Slack/Discord/Email) that trigger if a specific metric (e.g., Leq over a 15-minute window) exceeds local noise ordinance limits (e.g., >85 dB).

### Phase 3: Advanced Acoustics & Machine Learning (v3.0)
- [ ] **Real-Time 1/3 Octave Band Analysis:** Log frequency-specific SPL alongside broadband levels to help users determine *what* is making the noise (e.g., 60Hz electrical hum vs. 1000Hz human voices).
- [ ] **Edge AI Sound Classification:** Integration with TensorFlow Lite to locally classify and tag noise events (e.g., "Sirens", "Traffic", "Dog Barking", "HVAC") in the logs without saving the raw audio, enabling intelligent noise pollution tracking.

---

## 🛠️ Quick Start

**1. Install Dependencies**
```bash
pip install -r requirements.txt
# Requirements: sounddevice, numpy, pandas, scipy
```

**2. Calibrate Your Mic**
Open `logger.py` and update the `CALIBRATION_OFFSET` to match your specific microphone's dBFS-to-SPL offset.

**3. Start Logging**
```bash
python logger.py
```

**4. Analyze Data Trends**
```bash
python analyzer.py --input acoustic_log.csv
```

## 🤝 Contributing
Pull requests are welcome! If you are an acoustics engineer, data scientist, or Python developer, we would love your help in implementing A/C weighting filters or Grafana dashboards. Please open an issue first to discuss what you would like to change.

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.
