import cv2 as cv2
from PIL import ImageTk, Image
import numpy as numpy
import tkinter as tk

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascades/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
font = cv2.FONT_HERSHEY_SIMPLEX

# initiate id counter
label = 0

# names related to ids: example ==> loze: id=1,  etc
# 이런식으로 사용자의 이름을 사용자 수만큼 추가해준다.
names = ['None', 'jiwon']

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 640)  # set video width
cam.set(4, 480)  # set video height

# Define min window size to be recognized as a face
minW = 0.1 * cam.get(3)
minH = 0.1 * cam.get(4)

while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(int(minW), int(minH))
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        label, confidence = recognizer.predict(gray[y:y + h, x:x + w]) # label
        # Check if confidence is less them 100 ==> "0" is perfect match
        if confidence < 100:
            print(label, "아이디, 정확도", round(100 - confidence))
            label = names[label]
            confidence = "  {0}%".format(round(100 - confidence))
        else:
            label = "unknown"
            confidence = 0

        cv2.putText(img, str(label), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
        cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

    cv2.imshow('camera', img)
    k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
    if k == 27:
        break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()