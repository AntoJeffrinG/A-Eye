import cv2
from pyzbar.pyzbar import decode
import requests
import numpy as np

# Function to fetch product details from the Barcode Lookup API
def get_product_details(barcode_data):
    api_key = 'qpx4kxqlra1ws5p2a0o91kbwi03218'  # Replace with your API key
    url = f'https://api.barcodelookup.com/v2/products?barcode={barcode_data}&key={api_key}'
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['products']:
                product = data['products'][0]  # Fetch the first product
                product_name = product.get('product_name', 'Unknown')
                product_price = product.get('price', 'N/A')
                return product_name, product_price
            else:
                return "No product found", "N/A"
        else:
            return f"API Error: {response.status_code}", "N/A"
    except Exception as e:
        return f"Error: {e}", "N/A"

# Start webcam feed
cap = cv2.VideoCapture(0)

# Set resolution for better detection
cap.set(3, 1280)  # Width
cap.set(4, 720)   # Height

# Check webcam accessibility
if not cap.isOpened():
    print("Error: Could not access the webcam.")
    exit()

print("Webcam is accessible. Starting barcode scanning...")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame.")
        break

    try:
        # Decode barcodes using PyZbar
        barcodes = decode(frame)

        for barcode in barcodes:
            # Extract barcode data
            barcode_data = barcode.data.decode('utf-8')
            print(f"Detected barcode: {barcode_data}")

            # Fetch product details using the Barcode Lookup API
            product_name, product_price = get_product_details(barcode_data)
            print(f"Product Name: {product_name}")
            print(f"Price: {product_price}")

            # Draw bounding box around barcode (green box)
            points = barcode.polygon
            if len(points) == 4:  # If a polygon is detected
                pts = np.array([(point.x, point.y) for point in points], np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(frame, [pts], isClosed=True, color=(0, 255, 0), thickness=3)
            else:
                # Draw a rectangle as a fallback
                rect = barcode.rect
                cv2.rectangle(frame, 
                              (rect.left, rect.top), 
                              (rect.left + rect.width, rect.top + rect.height), 
                              (0, 255, 0), 
                              3)

            # Display product details on the frame
            text = f"{product_name} - {product_price}"
            cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    
    except Exception as e:
        print(f"Error during barcode processing: {e}")

    # Display the frame with bounding boxes
    cv2.imshow('Barcode Scanner', frame)

    # Break loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Exiting...")
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
