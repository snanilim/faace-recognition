import face_recognition
from PIL import Image, ImageDraw
import os
import math


def find_face(image_fileqqq):
    
    face_recognition.load_image_file(image_fileqqq)
    return [True]
    # face_locations = face_recognition.face_locations(image)
    # face_len = len(face_locations)
    # print('face_locations', face_len)
    # if face_len == 1:
    #     return [True]
    # elif face_len == 0:
    #     return [False, "No face found on this image, please upload one face image"]
    # elif face_len > 1:
    #     return [False, "Multiple faces found on this image, please upload one face image"]