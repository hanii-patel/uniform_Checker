# uniform detection system

A real-time system that detects if an employee is wearing a uniform and identifies them using a **hybrid AI approach**:
- 🎭 **Face Recognition** using DeepFace
- 👕 **Uniform Detection** using a custom-trained CNN (Keras)

---

## 🔧 Features

- Live webcam feed
- Employee face recognition (DeepFace)
- Uniform detection (CNN classifier)
- SQLite logging of violations
- Auto-save violation images with timestamp
- Capture on key press (`c`)
- Label as **Unknown** if face not matched

---

## 📁 Project Structure
Hybrid-Uniform-Checker/
│
├── employee_db/                         # ➤ Employee reference images (e.g. Hani_01.jpg)
│   └── Hani_01.jpg
│   └── Drashti_02.jpg
│   └── ...
│
├── captures/                            # ➤ Automatically saved violation images
│   └── Hani_01_20250608_141233.jpg
│   └── ...
│
├── datasets/                            # ➤ Training data for uniform classifier
│   ├── uniform/                         # ➤ Images with uniform
│   │   └── u1.jpg
│   │   └── u2.jpg
│   │   └── ...
│   └── no_uniform/                      # ➤ Images without uniform
│       └── nu1.jpg
│       └── nu2.jpg
│       └── ...
│
├── violation.db                         # ➤ SQLite database for logging violations
│
├── haarcascade_frontalface_default.xml  # ➤ Haar cascade file for face detection
│
├── uniform_classifier.keras             # ➤ Trained CNN model for uniform detection
│
├── hybrid_uniform_checker.py            # ➤ Main script (Hybrid CNN + DeepFace)
│
├── re_train_model.py                    # ➤ Script to retrain CNN model on dataset
│
├── convert_model.py                     # ➤ Script to convert/save Keras model
│
├── requirements.txt                     # ➤ All required Python packages
│
└── README.md                            # ➤ Project documentation (copy from above)


---

💾 Violation log(SQLite)
Logs to violation.db → violations table:
| name    | emp\_id | status   | date       | time     | image\_path                     |
| ------- | ------- | -------- | ---------- | -------- | ------------------------------- |
| Hani    | 01      | Not Worn | 2025-06-08 | 14:22:33 | captures/Hani\_01\_20250608.jpg |
| Unknown | --      | Not Worn | 2025-06-08 | 14:25:10 | captures/Unknown\_20250608.jpg  |

---

🧑‍💼 Face Recognition (DeepFace)
Match detected face against employee_db/

Supported formats: Name_ID.jpg

Example: Hani_01.jpg

Threshold = 0.6 (faces below this confidence are labeled Unknown)

---

👕 Uniform Detection (CNN)
Takes full frame as input (resized to 224x224)

Predicts:

Worn if CNN output > 0.5

Not Worn otherwise

Model must be trained before use and saved as uniform_classifier.keras.

---

📌 Notes
Face recognition uses DeepFace backend (default: VGG-Face)

For best results:

Add 2–3 clear face images per employee

Maintain consistent lighting and camera angle

Works offline after models are ready

---

📸 Capture Rules
Save only when:

Face is recognized

c key is pressed
File format:
captures/Name_ID_YYYYMMDD_HHMMSS.jpg

---

🧠 Models Used
Face Recognition: DeepFace (VGG-Face, Facenet, ArcFace, etc.)

Uniform Detection: Custom CNN (Keras)

✨ Future Work
Add Streamlit dashboard

Add admin portal to register employees

Generate violation reports

Trigger alert for repeated violators



