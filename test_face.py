import face_recognition

image = face_recognition.load_image_file("known_faces/Dharini.jpg")

print("Shape:", image.shape)
print("Dtype:", image.dtype)

faces = face_recognition.face_locations(image)

print("Faces found:", len(faces))