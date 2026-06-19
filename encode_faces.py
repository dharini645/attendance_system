"""
encode_faces.py

Run this ONCE before starting the attendance system.
It reads all photos from the known_faces/ folder,
generates a 128-number face encoding for each person,
and saves them to a file called encodings.pkl.

HOW TO USE:
  1. Add one clear photo per student to the known_faces/ folder.
  2. Name each file as the student's name, e.g.:  Dharini.jpg
  3. Run:  python encode_faces.py
  4. You'll see "Encodings saved!" when done.

IMPORTANT:
  - Use one front-facing photo per person (good lighting, face clearly visible).
  - Supported formats: .jpg, .jpeg, .png
"""

import os
import pickle
import face_recognition


KNOWN_FACES_DIR = "known_faces"
ENCODINGS_FILE  = "encodings.pkl"


def encode_all_faces():
    known_encodings = []   # list of 128-number arrays
    known_names     = []   # list of student names matching each encoding

    
    # Loop through every image in the known_faces/ folder
    for filename in os.listdir(KNOWN_FACES_DIR):
        if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
            continue   # skip non-image files

        # Extract name from filename  →  "Dharini.jpg" becomes "Dharini"
        name      = os.path.splitext(filename)[0]
        filepath  = os.path.join(KNOWN_FACES_DIR, filename)

        print(f"Processing: {filename} → name: {name}")



        # Load the image and compute the face encoding
        import cv2
        import numpy as np
        img_bgr = cv2.imread(filepath)
        if img_bgr is None:
            print(f"  ⚠️  Could not read {filename}. Skipping.")
            continue
        image = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        # Force contiguous array in uint8
        image = np.ascontiguousarray(image, dtype=np.uint8)
        # Detect face locations first, then encode
        print("Shape:", image.shape)
        print("Dtype:", image.dtype)
        print("Min:", image.min())
        print("Max:", image.max())
        face_locations = face_recognition.face_locations(image, model="hog")
        if not face_locations:
            print(f"  ⚠️  No face detected in {filename}. Skipping.")
            continue
        encodings = face_recognition.face_encodings(image, known_face_locations=face_locations)

        if len(encodings) == 0:
            # No face was found in this photo — skip it
            print(f"  ⚠️  No face detected in {filename}. Skipping.")
            continue

        if len(encodings) > 1:
            # More than one face found — only use the first one
            print(f"  ⚠️  Multiple faces in {filename}. Using the first one.")

        known_encodings.append(encodings[0])
        known_names.append(name)
        print(f"  ✅  Encoded successfully.")

    # Save everything to a pickle file for fast loading later
    with open(ENCODINGS_FILE, "wb") as f:
        pickle.dump({"encodings": known_encodings, "names": known_names}, f)

    print(f"\n✅ Done! {len(known_names)} face(s) encoded and saved to {ENCODINGS_FILE}")
    print(f"   Names registered: {', '.join(known_names)}")


if __name__ == "__main__":
    encode_all_faces()