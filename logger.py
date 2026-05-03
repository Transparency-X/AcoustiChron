import sounddevice as sd
import numpy as np
import threading
import time
import sys
from datetime import datetime, timezone

# InfluxDB specific imports
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import ASYNCHRONOUS

# ==========================================
# ⚙️ AUDIO CONFIGURATION
# ==========================================
SAMPLE_RATE = 48000
BLOCK_SIZE = 48000   # 48000 samples = 1 exact second of audio
CHANNELS = 1

# CALIBRATION OFFSET: Change this so your dBFS output matches real-world dB SPL.
# For a UMIK-1, check the .txt calibration file provided by miniDSP.
CALIBRATION_OFFSET = 100.0  

# ==========================================
# 🗄️ INFLUXDB CONFIGURATION
# ==========================================
# For Local Database use: "http://localhost:8086"
# For Cloud use your specific region URL (e.g., "https://us-east-1-1.aws.cloud2.influxdata.com")
INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "PASTE_YOUR_LONG_API_TOKEN_HERE"
INFLUX_ORG = "Acoustics_Lab"
INFLUX_BUCKET = "acoustichron_data"

# ==========================================
# 🌐 GLOBAL VARIABLES
# ==========================================
# Global variable to track the active event tag inputted by the user
CURRENT_TAG = "None"

# Initialize InfluxDB Client
client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)

# ASYNCHRONOUS mode handles queueing and batching automatically behind the scenes
write_api = client.write_api(write_options=ASYNCHRONOUS)


def audio_callback(indata, frames, time_info, status):
    """
    Called by sounddevice for every block of audio (1x per second).
    Captures the audio, calculates SPL, and pushes an InfluxDB Point to the queue.
    """
    if status:
        print(f"\n[Stream Warning] {status}", file=sys.stderr)
    
    # Calculate RMS (Root Mean Square) of the audio block
    rms = np.sqrt(np.mean(indata**2))
    
    if rms > 0:
        # Convert RMS to decibels relative to Full Scale (dBFS)
        dbfs = 20 * np.log10(rms)
        # Convert dBFS to Sound Pressure Level (dB SPL)
        spl = dbfs + CALIBRATION_OFFSET
    else:
        spl = 0

    # Create an InfluxDB Data Point
    point = (
        Point("acoustic_measurement")
        .tag("environment", "main_room")         # Static tag (e.g., specific room or mic)
        .tag("event_tag", CURRENT_TAG)           # Dynamic tag (e.g., "White Noise", "TV Playing")
        .field("spl_db", float(spl))             # The actual measured decibel level
        .time(datetime.now(timezone.utc), WritePrecision.NS) # Exact timestamp in UTC
    )

    # Write to InfluxDB
    # (Because we use ASYNCHRONOUS, this instantly passes to a background thread without blocking audio)
    write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)


def user_input_thread():
    """Background thread that listens for user keyboard input to manually tag the logs."""
    global CURRENT_TAG
    
    print("\n" + "="*55)
    print("📝 EVENT TAGGING IS ACTIVE")
    print("Type an event (e.g., 'White Noise', 'TV') and press Enter.")
    print("Type 'clear', 'none', or leave blank to remove the tag.")
    print("="*55 + "\n")
    
    while True:
        try:
            new_tag = input()
            # Handle clear commands
            if new_tag.strip().lower() in ['clear', 'none', 'stop', '']:
                CURRENT_TAG = "None"
                print(f"--> [Tag Cleared] Back to logging ambient noise.")
            else:
                CURRENT_TAG = new_tag.strip()
                print(f"--> [Tag Active] All following seconds logged as: '{CURRENT_TAG}'")
        except EOFError:
            break


def main():
    print(f"🎙️ Starting AcoustiChron Real-Time Logging to InfluxDB...")
    print(f"Target URL: {INFLUX_URL} | Bucket: {INFLUX_BUCKET}")
    print(f"Resolution: 1 second | Base Sample Rate: {SAMPLE_RATE} Hz")
    print(f"Press Ctrl+C at any time to stop logging gracefully.")

    # Start the User Input thread for live tagging
    input_thread = threading.Thread(target=user_input_thread, daemon=True)
    input_thread.start()

    try:
        # Start the Audio Stream
        with sd.InputStream(samplerate=SAMPLE_RATE, 
                            blocksize=BLOCK_SIZE, 
                            channels=CHANNELS, 
                            callback=audio_callback):
            
            # Keep the main thread alive so background threads can run
            while True:
                time.sleep(0.1) 
                
    except KeyboardInterrupt:
        print("\n\n🛑 Stop command received. Shutting down safely...")
    finally:
        # Crucial: Ensure all pending asynchronous writes are flushed to the DB before closing!
        write_api.close()
        client.close()
        print("✅ Flushed queue and gracefully disconnected from InfluxDB.")


if __name__ == "__main__":
    main()
