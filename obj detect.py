import cv2
import torch
import pyttsx3  # Text-to-Speech library

# Load the YOLOv5 model (pre-trained on COCO dataset)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# Initialize TTS engine
tts_engine = pyttsx3.init()

# Function to narrate detected objects
def narrate(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# Open the webcam
cap = cv2.VideoCapture(0)  # 0 for the default camera

# Set to keep track of narrated objects
narrated_objects = set()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Perform object detection
    results = model(frame)

    # Parse results
    current_frame_objects = set()
    for *box, conf, cls in results.xyxy[0]:  # Iterate through detections
        label = results.names[int(cls)]  # Get object name
        confidence = conf.item()

        # Check if the object is newly detected
        if label not in narrated_objects:
            narrate(f"I detected a {label}")
            narrated_objects.add(label)  # Mark as narrated
        
        # Keep track of objects in the current frame
        current_frame_objects.add(label)

        # Draw bounding box and label
        x1, y1, x2, y2 = map(int, box)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(frame, f"{label} {confidence:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # Remove objects that are no longer in the frame
    narrated_objects.intersection_update(current_frame_objects)

    # Display the video feed
    cv2.imshow('Object Detection', frame)

    # Quit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
