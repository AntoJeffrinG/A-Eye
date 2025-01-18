import cv2
from ultralytics import YOLO

# Load the pre-trained YOLO model
model = YOLO('yolov8n.pt')

def infer_relationship(obj1, obj2):
    """
    Infer spatial relationship between two objects based on bounding box coordinates.
    """
    label1, bbox1 = obj1
    label2, bbox2 = obj2
    
    x1a, y1a, x2a, y2a = bbox1  # Object 1
    x1b, y1b, x2b, y2b = bbox2  # Object 2

    # Debugging: Print out bounding box coordinates
    print(f"{label1}: {bbox1}")
    print(f"{label2}: {bbox2}")

    # Relationship: obj1 is "on" obj2
    if y2a < y1b and x1a < x2b and x2a > x1b:  # y2a (bottom of obj1) is above y1b (top of obj2)
        return f"{label1} is on {label2}"
    
    # Relationship: obj1 is "next to" obj2 (left or right)
    if x2a < x1b:  # obj1 is to the left of obj2
        return f"{label1} is to the left of {label2}"
    elif x1a > x2b:  # obj1 is to the right of obj2
        return f"{label1} is to the right of {label2}"

    # Default: No clear relationship
    return None

# Start the webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Perform object detection
    results = model.predict(frame, conf=0.5)  # Confidence threshold = 0.5
    detected_objects = []

    for box in results[0].boxes:
        cls = int(box.cls[0])  # Class index
        label = results[0].names[cls]  # Object label
        bbox = box.xyxy[0].cpu().numpy()  # Bounding box coordinates
        detected_objects.append((label, bbox))

    # Infer spatial relationships
    relationships = []
    for i, obj1 in enumerate(detected_objects):
        for j, obj2 in enumerate(detected_objects):
            if i != j:  # Compare different objects
                relationship = infer_relationship(obj1, obj2)
                if relationship:
                    relationships.append(relationship)

    # Draw bounding boxes and labels
    for obj in detected_objects:
        label, bbox = obj
        x1, y1, x2, y2 = map(int, bbox)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # Display relationships prominently in black
    y_offset = 20
    if relationships:
        for relationship in relationships:
            cv2.putText(frame, relationship, (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)  # Black color (0, 0, 0)
            y_offset += 20
    else:
        cv2.putText(frame, "No significant relationships found.", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)  # Black color (0, 0, 0)

    # Show the frame
    cv2.imshow("YOLO with Contextual Awareness", frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
