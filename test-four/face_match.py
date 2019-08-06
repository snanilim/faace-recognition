import face_recognition
from PIL import Image, ImageDraw
import os
import math





def face_distance_to_conf(face_distance, face_match_threshold=0.6):
    if face_distance > face_match_threshold:
        range = (1.0 - face_match_threshold)
        linear_val = (1.0 - face_distance) / (range * 2.0)
        return linear_val
    else:
        range = face_match_threshold
        linear_val = 1.0 - (face_distance / (range * 2.0))
        return linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))

def match_algorithm(folderName):
    old_image_path = './img/old/' + folderName + '/'

    for root, dirs, files in  os.walk(old_image_path):
        for i, file in enumerate(files):
            if file.endswith("png") or file.endswith("jpg"):
                print(i)
                print(len(files))


                old_image = face_recognition.load_image_file(old_image_path + file)
                old_image_encodings = face_recognition.face_encodings(old_image)[0]


                new_image = face_recognition.load_image_file('./img/new/compaer.jpg')
                new_face_locations = face_recognition.face_locations(new_image)
                new_face_encodings = face_recognition.face_encodings(new_image, new_face_locations)


                # Loop through faces in test image
                for(top, right, bottom, left), face_encoding in zip(new_face_locations, new_face_encodings):
                    matches = face_recognition.compare_faces([old_image_encodings], face_encoding, tolerance=0.5)
                    distance = face_recognition.face_distance([old_image_encodings], face_encoding)
                    
                    distance_number = face_distance_to_conf(distance)
                    distance_percent = distance_number[0] * 100

                    print('distance', distance_number[0] * 100)
                    # if match
                    if True in matches:
                        return [True, distance_percent]

                    elif i == len(files) - 1:
                        return [False, distance_percent]




        



