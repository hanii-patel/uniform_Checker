# app.py (or camera_feed.py)
import cv2
import os
from datetime import datetime

# Create folder if not exists
os.makedirs("data/test_entries", exist_ok=True)

# Start webcam (use 0 or change to your cam ID)
cap = cv2.VideoCapture(0)

print("Press 's' to save frame, 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Display the frame
    cv2.imshow("Entry Camera Feed", frame)

    key = cv2.waitKey(1)
    
    if key == ord('s'):
        # Save frame
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/test_entries/frame_{timestamp}.jpg"
        cv2.imwrite(filename, frame)
        print(f"Frame saved as: {filename}")

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
