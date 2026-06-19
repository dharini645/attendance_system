from PIL import Image
import numpy as np

img = Image.open("known_faces/Dharini.jpg")

print("Mode:", img.mode)
print("Size:", img.size)

arr = np.array(img)

print("Shape:", arr.shape)
print("Dtype:", arr.dtype)