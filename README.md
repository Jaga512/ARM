
## AI-Based Road Damage Detection & Geo-Tagging System (Edge AI)

 ### An embedded real-time road inspection system that detects potholes, cracks, and manholes using YOLO on Raspberry Pi, geo-tags them with GPS, assigns priority levels, and logs the data for smart infrastructure analytics.
---
## Features
- Real-time road damage detection  
- Geo-tagging with GPS (latitude & longitude)  
- Priority-based classification  
- Duplicate detection filtering  
- Edge AI (works without internet)  
- Triple-thread high-FPS pipeline  
- Automatic evidence storage  
- Offline logging + future cloud sync ready

---
## System Architecture

The system runs completely on an edge device (Raspberry Pi):

- Camera captures live video  
- Frames processed locally  
- YOLO detects road damage  
- GPS fetches location  
- Unique detections are stored  
- Road Health Score can be computed  

This eliminates cloud dependency and reduces latency.

---

## Tech Stack

### Hardware
- Raspberry Pi (Edge AI processor)  
- Pi Camera Module  
- GPS Module (Serial communication)  
- SD Card (data storage)  
- Portable Power Supply

---

### Software
- Python  
- OpenCV  
- Ultralytics YOLO  
- Picamera2  
- PySerial  
- Multi-threading

---

## Multi-Threaded Edge AI Pipeline

To achieve real-time performance:

🟢 **Camera Thread**
- Captures frames continuously  

🔵 **YOLO Inference Thread**
- Runs object detection  

🟡 **Logger Thread**
- Stores image + metadata asynchronously  

**This ensures:**
- ✔ Zero lag live feed  
- ✔ Maximum FPS  
- ✔ Non-blocking disk operations

---
## Dataset

Dataset includes:

- Potholes  
- Cracks  
- Manholes  

---

## Output
![WhatsApp Image 2026-02-20 at 4 47 40 PM](https://github.com/user-attachments/assets/a6e1e31a-73ec-401a-8b7d-19f80983ec14)
<img width="1600" height="1200" alt="image" src="https://github.com/user-attachments/assets/81d23768-4c92-4b81-84fe-a7018b98d98f" />
![WhatsApp Image 2026-02-20 at 4 47 51 PM](https://github.com/user-attachments/assets/237b6e71-d9ab-4318-9530-47369e61f175)

---
## Performance

- ✔ Real-time CPU inference on Raspberry Pi  
- ✔ Stable continuous detection  
- ✔ Accurate multi-class detection  
- ✔ Low-cost deployment
  ---

## Use Cases

- Automated road inspection vehicles  
- Damage hotspot mapping  
- Predictive maintenance  
- Infrastructure analytics  
- Government monitoring systems  

---
##  Future Scope

- Cloud dashboard  
- Edge TPU / GPU acceleration
- Integration with maps 
- Depth-based pothole severity  
- Real-time damage heatmaps  
- Vehicle-mounted large-scale deployment

---
## Authors

- Jagasuriya S (ECE) - jagasuriyas.ece2023@citchennai.net
- Deepak Raj K (ECE) - deepakrajk.ece2023@citchennai.net
- Inbaselvan Ayyanar (CSE) - inbaselvanayyanar.cse2023@citchennai.net
---


