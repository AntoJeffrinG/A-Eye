import cv2
import torch
import torchvision.transforms as T
from PIL import Image
import pyttsx3

# Load a pre-trained model (MobileNet or ResNet)
model = torch.hub.load('pytorch/vision:v0.10.0', 'mobilenet_v2', pretrained=True)
model.eval()

# Load ImageNet labels
# Ensure "imagenet_classes.txt" is in the same directory and contains one class name per line
with open("imagenet_classes.txt") as f:
    imagenet_labels = [line.strip() for line in f]

# Initialize TTS engine
tts_engine = pyttsx3.init()

def narrate(text):
    """Narrate the detected product name."""
    tts_engine.say(text)
    tts_engine.runAndWait()

# Define transformations for image preprocessing
transform = T.Compose([
    T.ToPILImage(),
    T.Resize((224, 224)),
    T.ToTensor(),
    T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Real-time recognition
cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Preprocess the frame
    input_tensor = transform(frame).unsqueeze(0)

    # Perform inference
    with torch.no_grad():
        outputs = model(input_tensor)
        _, predicted = outputs.max(1)
        label = imagenet_labels[predicted.item()]  # Get the class name

    # Narrate the detected object
    narrate(f"I see a {label}")
    print(f"Detected: {label}")

    # Display the frame with label
    cv2.putText(frame, f"{label}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.imshow('Product Recognition', frame)

    # Quit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
