import cv2
import os
import numpy as np
from PIL import Image


face_cascade = cv2.CascadeClassifier('C:\\Users\\jwchu\Documents\\schoolFiles\\Project based '
                                     'learning\\playground\\test\\haarcascades\\haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR, "dataset")

print(BASE_DIR)

current_id = 0
label_ids = {}
y_label = []
x_train = []

for root, dirs, files in os.walk(image_dir):
    print(root, dirs, files)
    for file in files:
        if file.endswith('png') or file.endswith('jpg'):
            path = os.path.join(root, file)
            label = os.path.basename(root).replace(" ", "-").lower()
            if label not in label_ids:
                label_ids[label] = current_id
                current_id += 1

            # 아이디 빙빙
            id_ = label_ids[label]
            print(label, "레이블, 아이디", id_)

            # gray scaled 이미지 빙빙
            grayScaled_image = Image.open(path).convert("L")

            size = (320, 320)

            # 안티에리어시드 이미지 빙빙
            final_image = grayScaled_image.resize(size, Image.ANTIALIAS)

            # 배열 형태로 빙빙
            image_array = np.array(final_image, "uint8")

            # 얼굴 케스케이드 빙빙
            faces = face_cascade.detectMultiScale(image_array, scaleFactor=1.1, minNeighbors=5)

            for (x, y, w, h) in faces:
                regionOfInterest = image_array[y: y + h, x: x + w]
                x_train.append(regionOfInterest)
                y_label.append(id_)

print(label_ids)
recognizer.train(x_train, np.array(y_label))
recognizer.save("recognizers/face-trainer.yml")
