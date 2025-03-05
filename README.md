
# 🎭 Face Recognition-Based Attendance System

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?style=for-the-badge&logo=opencv)
![SQLite](https://img.shields.io/badge/Database-SQLite-blue?style=for-the-badge&logo=sqlite)
![Face Recognition](https://img.shields.io/badge/Face%20Recognition-Enabled-orange?style=for-the-badge)

## 📌 Overview
The **Face Recognition-Based Attendance System** automates attendance marking using real-time facial recognition. It uses **OpenCV, face_recognition library, and SQLite database** to detect and log student attendance securely.

## 🚀 Features
- ✅ **Face Recognition-Based Attendance**: Detects faces and marks attendance automatically.
- ✅ **SQLite Database Integration**: Stores attendance records securely.
- ✅ **Real-Time Webcam Detection**: Uses OpenCV to capture video frames.
- ✅ **Encodes and Stores Faces**: Trains on images and saves encodings for fast recognition.
- ✅ **Efficient & Scalable**: Works smoothly with multiple faces.

## 🏗️ Tech Stack
- **Programming Language**: Python 🐍
- **Libraries Used**:
  - OpenCV 🎥 (for face detection & image processing)
  - face_recognition 😃 (for facial feature encoding & recognition)
  - NumPy 🔢 (for matrix operations)
  - SQLite 🗄️ (for storing attendance data)
  - Pickle 📦 (for saving encodings)

## 📂 Project Structure
```
📁 Face-Recognition-Attendance-System
│── 📄 README.md             # Project documentation
│── 📄 face_recognition.py   # Main script for face recognition & attendance
│── 📁 Training_images       # Folder containing images of registered users
│── 📄 face_encodings.pkl    # Saved face encodings for faster recognition
│── 📄 attendance.db         # SQLite database for attendance records
```

## 🔥 Installation & Usage

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/your-username/Face-Recognition-Attendance-System.git
cd Face-Recognition-Attendance-System
```

### 2️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 3️⃣ Run the Face Recognition Attendance System
```sh
python face_recognition.py
```

## 🗄️ Database Schema (SQLite)
The database **attendance.db** contains the following tables:

### **STUDENTS Table** (Stores registered students)
| ID | Name  |
|----|-------|
| 101 | Alice |
| 102 | Bob   |

### **ATTENDANCE Table** (Stores attendance records)
| ID  | Name  | Date       | Time     | Status  |
|-----|-------|-----------|----------|---------|
| 101 | Alice | 2025-03-05 | 09:00:00 | Present |
| 102 | Bob   | 2025-03-05 | 09:02:00 | Present |

## 📸 How It Works
1️⃣ The system **loads pre-trained face encodings** from images in the `Training_images` folder.
2️⃣ The **webcam captures live video**, detects faces, and **compares them** with stored encodings.
3️⃣ If a **match is found**, the system **logs the attendance** into the SQLite database.
4️⃣ A bounding box with the student’s name is displayed in real-time.

## 📺 Demo
![Demo GIF](https://github.com/your-username/Face-Recognition-Attendance-System/blob/main/demo.gif)

## 🔐 Future Enhancements
- [ ] **GPS-Based Verification** 📍 (Ensure students are within the classroom before marking attendance)
- [ ] **Session Locking** 🔒 (Prevents students from logging out before class ends)
- [ ] **Teacher-Controlled Attendance Window** ⏳ (Restricts attendance marking to a specific timeframe)
- [ ] **Device Fingerprinting** 📱 (Ensures students use registered devices for attendance)
- [ ] **Web-Based Dashboard** 📊 (View & export attendance reports online)

## 🤝 Contributing
Contributions are welcome! To contribute:
1. **Fork** this repository 🍴
2. **Create a new branch** (`git checkout -b feature-branch`) 🌿
3. **Commit your changes** (`git commit -m 'Add new feature'`) 💾
4. **Push to the branch** (`git push origin feature-branch`) 🚀
5. **Open a Pull Request** 📩



---
Made with ❤️ by [Chirag Halan](https://github.com/chiraghalan/)
```

