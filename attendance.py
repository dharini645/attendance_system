"""
attendance.py

The MAIN script. Run this to start the attendance session.
It opens your webcam, recognizes faces in real time,
and marks attendance in the SQLite database.

HOW TO USE:
  python attendance.py

CONTROLS (while the camera window is open):
  Press  Q  →  quit the session
  Press  S  →  save today's attendance to CSV immediately

WHAT APPEARS ON SCREEN:
  - Green box  = face recognized (name shown below box)
  - Red box    = face detected but not recognized ("Unknown")
  - Console    = logs every time someone is newly marked present
"""

import cv2
import pickle
import face_recognition
import numpy as np
from database import init_db, mark_present, get_today_records
from export import export_to_csv


ENCODINGS_FILE  = "encodings.pkl"
TOLERANCE       = 0.50    # lower = stricter matching (0.4–0.6 is a good range)
FRAME_SKIP      = 2       # process every 2nd frame to keep things fast


def load_encodings():
    """Loads the saved face encodings from encodings.pkl."""
    try:
        with open(ENCODINGS_FILE, "rb") as f:
            data = pickle.load(f)
        print(f"✅ Loaded {len(data['names'])} known face(s): {', '.join(data['names'])}")
        return data["encodings"], data["names"]
    except FileNotFoundError:
        print("❌ encodings.pkl not found!")
        print("   Please run:  python encode_faces.py   first.")
        exit(1)


def draw_box(frame, top, right, bottom, left, name, is_known):
    """
    Draws a colored rectangle around the detected face
    and puts the person's name below it.
    Green = known person, Red = unknown person.
    """
    color = (0, 200, 0) if is_known else (0, 0, 220)   # BGR format: Green or Red

    # Draw the rectangle border
    cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

    # Draw a filled rectangle behind the name label (for readability)
    cv2.rectangle(frame, (left, bottom - 30), (right, bottom), color, cv2.FILLED)

    # Put the name text inside the label box
    cv2.putText(
        frame, name,
        (left + 6, bottom - 8),
        cv2.FONT_HERSHEY_DUPLEX,
        0.65,          # font scale
        (255, 255, 255),  # white text
        1
    )


def run_attendance():
    """Main function — opens the webcam and runs the attendance loop."""

    # 1. Setup database and load encodings
    init_db()
    known_encodings, known_names = load_encodings()

    # 2. Open webcam (0 = default/built-in camera)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Could not open webcam. Check that it's connected and not in use.")
        return

    print("\n🎥 Webcam opened. Attendance session started.")
    print("   Press Q to quit  |  Press S to save CSV\n")

    frame_count     = 0
    # Cache last processed results so we display them on skipped frames too
    last_face_locations  = []
    last_face_names      = []

    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️  Failed to read frame. Retrying...")
            continue

        frame_count += 1

        # --- Only process every Nth frame (for speed) ---
        if frame_count % FRAME_SKIP == 0:

            # Shrink the frame to 1/4 size for faster face detection
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # face_recognition expects RGB, OpenCV gives BGR — convert
            rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            # Detect face locations (returns top, right, bottom, left in 1/4 scale)
            face_locations = face_recognition.face_locations(rgb_small, model="hog")

            # Get 128-number encodings for each detected face
            face_encodings = face_recognition.face_encodings(rgb_small, face_locations)

            frame_names = []

            for face_encoding in face_encodings:
                # Compare this face against all known faces
                distances = face_recognition.face_distance(known_encodings, face_encoding)

                name = "Unknown"

                if len(distances) > 0:
                    best_match_idx = np.argmin(distances)   # index of closest match

                    if distances[best_match_idx] < TOLERANCE:
                        name = known_names[best_match_idx]

                        # Mark attendance (returns True only if newly added)
                        newly_marked = mark_present(name)
                        if newly_marked:
                            print(f"✅ Marked present: {name}  (distance: {distances[best_match_idx]:.2f})")

                frame_names.append(name)

            # Scale face locations back up to full frame size (×4)
            last_face_locations = [(t*4, r*4, b*4, l*4) for (t, r, b, l) in face_locations]
            last_face_names     = frame_names

        # --- Draw boxes on every frame (including skipped ones) ---
        for (top, right, bottom, left), name in zip(last_face_locations, last_face_names):
            draw_box(frame, top, right, bottom, left, name, name != "Unknown")

        # Show today's attendance count in the top-left corner
        present_today = len(get_today_records())
        cv2.putText(
            frame,
            f"Present today: {present_today}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        # Display the live video window
        cv2.imshow("Attendance System  |  Press Q to quit", frame)

        # Key controls
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            print("\n👋 Session ended.")
            break
        elif key == ord("s"):
            path = export_to_csv()
            print(f"💾 CSV saved: {path}")

    cap.release()
    cv2.destroyAllWindows()

    # Auto-save CSV when session ends
    csv_path = export_to_csv()
    print(f"\n📄 Attendance saved to: {csv_path}")

    # Print summary
    records = get_today_records()
    print(f"\n📋 Today's attendance ({len(records)} present):")
    for name, time in records:
        print(f"   {name:20s}  {time}")


if __name__ == "__main__":
    run_attendance()