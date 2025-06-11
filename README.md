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
| 📁 Folder / 📄 File                   | Description                                                                  |
| ------------------------------------- | ---------------------------------------------------------------------------- |
| `employee_db/`                        | Folder containing employee reference images (e.g. `Hani_01.jpg`)             |
| `captures/`                           | Folder to save captured images of violations                                 |
| `datasets/`                           | Dataset folder used to train the uniform classifier                          |
| ├── `uniform/`                        | Images of people wearing uniform                                             |
| └── `no_uniform/`                     | Images of people **not** wearing uniform                                     |
| `violation.db`                        | SQLite database to store violation logs                                      |
| `haarcascade_frontalface_default.xml` | Haar Cascade XML file for face detection                                     |
| `uniform_classifier.keras`            | Trained Keras CNN model for uniform detection                                |
| `hybrid_uniform_checker.py`           | **Main Python script** combining CNN (uniform) + DeepFace (face recognition) |
| `re_train_model.py`                   | Script to retrain the CNN model using `datasets/`                            |
| `convert_model.py`                    | Script to convert or save the Keras model                                    |
| `requirements.txt`                    | List of Python dependencies for the project                                  |
| `README.md`                           | Project documentation (overview, setup, usage, etc.)                         |


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




