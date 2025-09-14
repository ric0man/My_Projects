## 😷 Face Mask Detection — `README.md`

```markdown
# 😷 Face Mask Detection

Real-time face mask detection using OpenCV and a pre-trained CNN. Designed for quick demos, modular clarity.
## 🚀 Features
- 🎥 Real-time webcam feed processing
- 🧠 CNN-based mask detection
- 🧱 Modular code with clean separation of concerns
- 📦 Easy setup and deployment

## 🛠️ Tech Stack
- Python
- OpenCV
- TensorFlow / Keras

## 📦 Setup

```bash
git clone https://github.com/ric0man/Face_Mask_Detection.git
cd Face_Mask_Detection
pip install -r requirements.txt


----------------------------------------------------------------------
Run Locally:python detect_mask.py

Project Structure:
├── detect_mask.py
├── model/
│   └── mask_detector.model
├── utils/
│   ├── face_detector.py
│   └── mask_classifier.py
├── .env
├── .gitignore
├── .gitattributes
└── README.md


📌 Notes
- Designed for quick demos.
- Easily extendable to mobile or edge deployment
- Model can be retrained with custom dataset
- .env, .gitignore, and .gitattributes included for clean setup
- README structured for clarity and reproducibility

