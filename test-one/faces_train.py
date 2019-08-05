import os
import cv2
import numpy as np
from PIL import Image
import pickle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR, "images")

face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

current_id = 0
label_ids = {}

y_labels = []
x_train = []


for root, dirs, files in  os.walk(image_dir):
    for file in files:
        if file.endswith("png") or file.endswith("jpg"):
            path = os.path.join(root, file)
            label = os.path.basename(os.path.dirname(path)).replace(" ", "-").lower()
            # print(label, path)
            # y_labels.append(label) #some numbers
            # x_train.append(path) # turn into numpy array grayscale
            pil_image = Image.open(path).convert('L') #grayscale
            size = (550, 550)
            final_image = pil_image.resize(size, Image.ANTIALIAS)
            image_arr = np.array(final_image, "uint8")
            # print(image_arr)

            # if label in label_ids:
            #     pass
            # else:
            #     label_ids[label] = current_id
            #     current_id +=1
            
            # id_ = label_ids[label]


            if not label in label_ids:
                label_ids[label] = current_id
                current_id +=1
            id_ = label_ids[label]
            print(label_ids)

            faces = face_cascade.detectMultiScale(image_arr, scaleFactor=1.5, minNeighbors=5)
            for (x, y, w, h) in faces:
                roi = image_arr[y:y+h, x:x+w]
                x_train.append(roi)
                y_labels.append(id_)

# print(y_labels)
# print(x_train)

with open("labels.pickle", "wb") as f:
    pickle.dump(label_ids, f)

recognizer.train(x_train, np.array(y_labels))
recognizer.save("trainer.yml")

