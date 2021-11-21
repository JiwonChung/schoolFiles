import numpy as np
import cv2
import timeit
import dlib
from PIL import ImageTk, Image
import numpy

# haarcascades 디렉토리의 haarcascade_frontalface_default.xml 파일을 Classifier로 사용
faceCascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
# camera
cap = cv2.VideoCapture(0)

# set width
cap.set(3, 640)
# set Height
cap.set(4, 480)


while True:
    ret, img = cap.read()
    now = timeit.default_timer()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(20, 20)
    )
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y: y + h, x: x + w]
        roi_color = img[y: y + h, x: x + w]

    # video 라는 이름으로 출력
    cv2.imshow("정지원만세", img)

    print("FPS:", round(1 / (timeit.default_timer() - now), 2))

    # press 'ESC' to quit # ESC를 누르면 종료
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break


cap.release()
cv2.destroyAllWindows()