# import the necessary packages
from imutils import paths
import numpy as np
import argparse
import imutils
import pickle
import cv2
import os
 
# construct the argument parser and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--dataset", required=True,
# 	help="path to input directory of faces + images")
# ap.add_argument("-e", "--embeddings", required=True,
# 	help="path to output serialized db of facial embeddings")
# ap.add_argument("-d", "--detector", required=True,
# 	help="path to OpenCV's deep learning face detector")
# ap.add_argument("-m", "--embedding-model", required=True,
# 	help="path to OpenCV's deep learning face embedding model")
# ap.add_argument("-c", "--confidence", type=float, default=0.5,
# 	help="minimum probability to filter weak detections")
args = {
    'dataset': 'dataset', 
    'embeddings': 'output/embeddings.pickle', 
    'detector': 'face_detection_model', 
    'embedding_model': 'openface_nn4.small2.v1.t7', 
    'confidence': 0.5
}

protoPath = os.path.sep.join([args["detector"], "deploy.prototxt"])
modelPath = os.path.sep.join([args["detector"],
	"res10_300x300_ssd_iter_140000.caffemodel"])

detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)
embedder = cv2.dnn.readNetFromTorch(args['embedding_model'])	
imagePaths = list(paths.list_images(args["dataset"]))
 
knownEmbeddings = []
knownNames = []
 
# initialize the total number of faces processed
total = 0

for (i, imagePath) in enumerate(imagePaths):
    print("[INFO] processing image {}/{}".format(i + 1,len(imagePaths)))
    name = imagePath.split(os.path.sep)[-2]

    image = cv2.imread(imagePath)
    image = imutils.resize(image, width=600)
    (h, w) = image.shape[:2]
    # print(h, w)
    imageBlob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300),(104.0, 177.0, 123.0), swapRB=False, crop=False)
    # print(imageBlob)
    detector.setInput(imageBlob)
    detections = detector.forward()
    # print(detections)
    if len(detections) > 0:
        i = np.argmax(detections[0, 0, :, 2])
        confidence = detections[0, 0, i, 2]
        print(confidence)
        if confidence > args["confidence"]:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            face = image[startY:endY, startX:endX]
            (fH, fW) = face.shape[:2]
            print(fH, fW)

            if fW < 20 or fH < 20:
                continue

            faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255,
            (96, 96), (0, 0, 0), swapRB=True, crop=False)
            embedder.setInput(faceBlob)
            vec = embedder.forward()
            print('is', i)

            knownNames.append(name)
            knownEmbeddings.append(vec.flatten())
            total += 1
# print(imagePaths)
# print(embedder)

data = {"embeddings": knownEmbeddings, "names": knownNames}
f = open(args["embeddings"], "wb")
f.write(pickle.dumps(data))
f.close()