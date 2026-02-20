import cv2
import serial
import threading
import time
import math
import csv
import os
from datetime import datetime
from queue import Queue
from picamera2 import Picamera2
from ultralytics import YOLO

# ---------------- LOAD MODEL ----------------
model = YOLO("best.pt")

# ---------------- CSV SETUP ----------------
CSV_FILE = "detections_log.csv"

if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Image", "Label", "Priority", "Timestamp", "Latitude", "Longitude"])

# ---------------- PRIORITY ----------------
CLASS_PRIORITY = {
    "pothole": "HIGH",
    "manhole": "MEDIUM",
    "crack": "LOW"
}

# ---------------- DUPLICATE CONTROL ----------------
stored_objects = []
DISTANCE_THRESHOLD = 80
TIME_THRESHOLD = 10

def is_new_detection(cx, cy, label):
    current_time = time.time()

    for px, py, plabel, ptime in stored_objects:
        distance = math.sqrt((cx - px) ** 2 + (cy - py) ** 2)

        if label == plabel and distance < DISTANCE_THRESHOLD:
            if current_time - ptime < TIME_THRESHOLD:
                return False

    stored_objects.append((cx, cy, label, current_time))

    if len(stored_objects) > 50:
        stored_objects.pop(0)

    return True

# ---------------- ASYNC LOG QUEUE ----------------
log_queue = Queue()

def log_worker():
    while True:
        data = log_queue.get()

        if data is None:
            break

        img, filename, label, priority, time_stamp, lat, lon = data

        cv2.imwrite(filename, img)

        # ✅ STORE IN CSV
        with open(CSV_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([filename, label, priority, time_stamp, lat, lon])

        print(f"\n✅ STORED")
        print(f"{label} | {priority} | {time_stamp} | {lat}, {lon}")

        log_queue.task_done()

threading.Thread(target=log_worker, daemon=True).start()

def store_data(img, time_stamp, label, priority, lat, lon):
    filename = f"capture_{time_stamp}.jpg"
    log_queue.put((img.copy(), filename, label, priority, time_stamp, lat, lon))

# ---------------- GPS ----------------
gps_lat = "No Satellite"
gps_lon = "No Satellite"

def read_gps():
    global gps_lat, gps_lon

    try:
        ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)

        while True:
            line = ser.readline().decode('utf-8', errors='ignore')

            if "$GPGGA" in line:
                data = line.split(',')

                if data[2] and data[4]:
                    lat = float(data[2][:2]) + float(data[2][2:]) / 60
                    lon = float(data[4][:3]) + float(data[4][3:]) / 60

                    gps_lat = f"{lat:.6f}"
                    gps_lon = f"{lon:.6f}"
                else:
                    gps_lat = "No Satellite"
                    gps_lon = "No Satellite"

    except:
        gps_lat = "GPS Error"
        gps_lon = "GPS Error"

threading.Thread(target=read_gps, daemon=True).start()

# ---------------- CAMERA ----------------
picam2 = Picamera2()
config = picam2.create_preview_configuration(
    main={"format": "BGR888", "size": (640, 480)}
)
picam2.configure(config)
picam2.start()

print("🚀 Road Damage Detection Started | Press 'q' to quit")

# ---------------- FPS COUNTER ----------------
prev_time = time.time()

# ---------------- MAIN LOOP ----------------
while True:

    frame = picam2.capture_array()
    results = model.predict(frame, conf=0.4, verbose=False)

    detections = []

    for r in results:
        for box in r.boxes:

            cls = int(box.cls[0])
            label = model.names[cls]

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            detections.append((label, cx, cy))

    # ---------------- PRIORITY CHECK ----------------
    for target in ["pothole", "manhole", "crack"]:

        for label, cx, cy in detections:

            if label == target and is_new_detection(cx, cy, label):

                priority = CLASS_PRIORITY[label]
                time_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                store_data(frame, time_stamp, label, priority, gps_lat, gps_lon)
                break
        else:
            continue
        break

    # ---------------- DISPLAY GPS ----------------
    cv2.putText(frame, f"Lat: {gps_lat}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    cv2.putText(frame, f"Lon: {gps_lon}", (20, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    # ---------------- FPS DISPLAY ----------------
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time

    cv2.putText(frame, f"FPS: {int(fps)}", (20, 110),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    cv2.imshow("Road Damage Detection - Pi 5", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
picam2.stop()
log_queue.put(None)