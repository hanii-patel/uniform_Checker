import cv2
import numpy as np
import os
import sqlite3
from datetime import datetime
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from deepface import DeepFace

# Load uniform classifier
uniform_model = load_model('uniform_classifier.keras')

# Set up Haar cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Database and capture setup
stored_violations = []

def save_violation(name, emp_id, status, img_path):
    conn = sqlite3.connect('violation.db')
    cursor = conn.cursor()

    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    cursor.execute("""
        INSERT INTO violations (name, emp_id, status, date, time, image_path)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, emp_id, status, date, time, img_path))

    conn.commit()
    conn.close()

    os.system('say "saved"' if os.name == 'posix' else 'echo \a')
    stored_violations.append(f"[SAVED] {name} ({emp_id}) | {status} at {date} {time}")

# Step 1: Load employee embeddings using DeepFace
employee_embeddings = []
employee_names = []
employee_ids = []

for file in os.listdir('employee_db'):
    if file.endswith('.jpg') or file.endswith('.png'):
        path = os.path.join('employee_db', file)
        try:
            embedding = DeepFace.represent(img_path=path, model_name="Facenet")[0]["embedding"]
            name_id = os.path.splitext(file)[0].split("_")
            name = name_id[0]
            emp_id = name_id[1] if len(name_id) > 1 else "00"
            employee_embeddings.append(embedding)
            employee_names.append(name)
            employee_ids.append(emp_id)
        except:
            print(f"❌ Failed to process: {file}")

# Step 2: Webcam logic
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    faces = face_cascade.detectMultiScale(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 1.3, 5)

    for (x, y, w, h) in faces:
        face_img = frame[y:y+h, x:x+w]

        try:
            input_embedding = DeepFace.represent(face_img, model_name="Facenet", enforce_detection=False)[0]["embedding"]
            similarities = [np.dot(input_embedding, emb) / (np.linalg.norm(input_embedding) * np.linalg.norm(emb)) for emb in employee_embeddings]
            best_match_idx = int(np.argmax(similarities))
            confidence = similarities[best_match_idx]

            name = employee_names[best_match_idx] if confidence > 0.75 else "Unknown"
            emp_id = employee_ids[best_match_idx] if confidence > 0.75 else "--"
        except:
            name = "Unknown"
            emp_id = "--"

        # Uniform detection
        uniform_crop = cv2.resize(frame, (224, 224))
        uniform_input = img_to_array(uniform_crop) / 255.0
        uniform_input = np.expand_dims(uniform_input, axis=0)
        prediction = uniform_model.predict(uniform_input)[0][0]
        status = "Worn" if prediction > 0.5 else "Not Worn"

        label = f"{name} ({emp_id}) - {status}"
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0,255,0), 2)
        cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('c') and name != "Unknown":
            now = datetime.now()
            timestamp = now.strftime("%Y%m%d_%H%M%S")
            filename = f"captures/{name}_{emp_id}_{timestamp}.jpg"
            cv2.imwrite(filename, frame)
            save_violation(name, emp_id, status, filename)

        if key == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break

    cv2.imshow("Uniform & Face Checker (Hybrid)", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Print log
if stored_violations:
    print("\n✅ Violations Stored:")
    for entry in stored_violations:
        print(entry)
else:
    print("\n⚠️ No violations were stored.")
