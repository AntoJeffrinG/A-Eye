import cv2
from pyzbar.pyzbar import decode  # Library to scan barcodes
import requests  # For making API requests
import re  # For detecting URLs

# Function to lookup product details using barcode number
def barcode_lookup(barcode):
    # Check if the detected barcode is a URL
    if re.match(r'^https?://', barcode):  # Match URL pattern
        print(f"Detected URL: {barcode}")
        return "URL Detected", barcode  # Return URL as product name and price as the URL itself
    else:
        # Proceed with the regular product lookup API for numeric barcodes
        api_url = f"https://api.barcodelookup.com/v2/products?barcode={barcode}&key=ifDzhmKslKav42OD93NEOH"
        try:
            response = requests.get(api_url)
            response.raise_for_status()  # Raises an exception for 4xx/5xx errors
            data = response.json()

            # Ensure 'products' key is present and not empty
            if 'products' in data and data['products']:
                product_name = data['products'][0]['product_name']
                price = data['products'][0].get('price', 'N/A')  # Price might not always be available
                return product_name, price
            else:
                print(f"Product not found for barcode: {barcode}.")
                return None, None
        except requests.exceptions.RequestException as e:
            print(f"API request failed for barcode {barcode}: {e}")
            return None, None

# Function to detect barcodes and display product details
def detect_barcode():
    cap = cv2.VideoCapture(0)  # Start capturing from the webcam
    last_product_name = ""
    last_price = ""

    try:
        while True:
            ret, frame = cap.read()  # Read a frame from the webcam
            if not ret:
                print("Failed to capture image")
                break

            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert frame to grayscale for barcode detection
            try:
                barcodes = decode(gray_frame)  # Detect barcodes using pyzbar
            except Exception as e:
                print(f"Error during barcode decoding: {e}")
                barcodes = []  # In case of error, continue with an empty list

            if barcodes:
                for barcode in barcodes:
                    barcode_data = barcode.data.decode('utf-8')  # Extract the barcode number
                    print(f"Detected barcode: {barcode_data}")  # Debugging output

                    # Get bounding box coordinates for barcode
                    x, y, w, h = barcode.rect
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Draw a green rectangle around barcode

                    # Lookup product details
                    product_name, price = barcode_lookup(barcode_data)

                    if product_name:
                        last_product_name = product_name
                        last_price = price
                        print(f"Product: {product_name}, Price: {price}")
                        cv2.putText(frame, f"Product: {product_name}, Price: {price}",
                                    (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    else:
                        print(f"Product not found for barcode: {barcode_data}.")

            # Display the last detected product if no new barcode is found
            if last_product_name:
                cv2.putText(frame, f"Product: {last_product_name}, Price: {last_price}",
                            (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)  # Display recognition result

            cv2.imshow('Barcode Detection', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit when 'q' key is pressed
                break

    finally:
        cap.release()  # Release the webcam
        cv2.destroyAllWindows()  # Close all OpenCV windows

if __name__ == "__main__":
    detect_barcode()
