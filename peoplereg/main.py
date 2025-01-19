import cv2
from face_recognition import detect_and_encode_faces
from database import store_face_data, find_matching_face
from user_input import get_user_info
import numpy as np

def main():
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Detect and encode faces
        encodings = detect_and_encode_faces(frame)

        for encoding in encodings:
            match = find_matching_face(encoding)
            if match:
                print(f"Face recognized! Info: {match}")
            else:
                print("New face detected.")
                name, age = get_user_info()
                store_face_data(name, age, encoding)
                
        # Display the captured frame
        cv2.imshow('Frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
    