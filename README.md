# 🎓 Smart Face Recognition Attendance System

A real-time attendance system built with Python and OpenCV that identifies students from a webcam feed and automatically logs their attendance to a database — no manual roll call needed.

> **Extended from published research:** This project implements the system described in *"Smart IoT-Based People Counter with Face Recognition"* — IRJMETS, Volume 07, Issue 05, May 2025.

---

## ✨ Features

- 🎥 **Real-time face detection** via webcam using OpenCV
- 🧠 **Face recognition** using 128-point facial encodings (face_recognition library)
- 🗄️ **SQLite database** — auto-logs name, date, and time per student
- 📄 **CSV export** using Pandas — generates daily attendance sheets
- 📊 **Streamlit dashboard** — view records, filter by date/student, download CSV
- 🚫 **Duplicate prevention** — each student is marked only once per day

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.10+ | Core language |
| OpenCV | Webcam access & frame processing |
| face_recognition | Face detection & 128-point encoding |
| SQLite3 | Attendance database (built into Python) |
| Pandas | Data processing & CSV export |
| Streamlit | Web dashboard |

---

## 📁 Project Structure

```
attendance-system/
├── known_faces/          ← Add one photo per student here
├── encode_faces.py       ← Step 1: Register student faces
├── attendance.py         ← Step 2: Run live attendance session
├── database.py           ← SQLite read/write logic
├── export.py             ← CSV export using Pandas
├── app.py                ← Streamlit dashboard
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/attendance-system.git
cd attendance-system
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

> ⚠️ **Windows users:** `face_recognition` requires `cmake` and `dlib`. Install cmake first:
> ```bash
> pip install cmake
> pip install dlib
> pip install face-recognition
> ```

### 3. Add student photos
Place one clear, front-facing photo per student in the `known_faces/` folder.
Name each file as the student's name:
```
known_faces/
├── Priya.jpg
└── Arjun.jpg
```

### 4. Encode the faces
```bash
python encode_faces.py
```
This generates `encodings.pkl` — the face database.

### 5. Start an attendance session
```bash
python attendance.py
```
The webcam opens. Recognized students are marked present automatically.

| Key | Action |
|---|---|
| `Q` | Quit the session |
| `S` | Save CSV immediately |

### 6. View the dashboard
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`

---

## 📸 Demo

```
🎥 Webcam opened. Attendance session started.
✅ Marked present: Dharini   (distance: 0.38)
✅ Marked present: Priya     (distance: 0.41)
📄 Attendance saved to: attendance_2025-06-10.csv

📋 Today's attendance (2 present):
   Dharini               09:32:15
   Priya                 09:33:02
```

---

## 🔧 Configuration

In `attendance.py`, you can tweak:

```python
TOLERANCE   = 0.50   # lower = stricter face matching (try 0.4–0.6)
FRAME_SKIP  = 2      # process every Nth frame (higher = faster but less responsive)
```

---

## 📄 License

MIT License — free to use and modify.

---

## 👩‍💻 Author

**Dharini R N** — Computer Science & Engineering, Kangeyam Institute of Technology  
[GitHub](https://github.com/dharini645) · [LinkedIn](https://www.linkedin.com/in/dharini-r-60647a264/)
