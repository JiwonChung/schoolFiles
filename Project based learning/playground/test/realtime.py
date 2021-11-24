from datetime import datetime

import cv2 as cv2
from PIL import ImageTk, Image
import numpy as numpy
import tkinter as tk

# GUI 시작------------------
window = tk.Tk(className="정지원만세 - Windows Color")

# 라즈베리 디스플레이 사이즈
window.geometry("480x320+10+10")
window.configure(bg="black")
window.resizable(False, False)

font_title = ("Microsoft YaHei UI", 20, "bold")
font_button = ("Microsoft YaHei UI", 15, "bold")

# 햄버거 슬라이드 프레임
frame_slide1 = tk.Frame(master=window, width=160, height=320, bg="purple")

frame_slide1.grid(row=0, column=0)

# 사진 나오는 프레임
frame_slide2 = tk.Frame(master=window, width=320, height=320, bg="blue")
frame_slide2.grid(row=0, column=1)

# 제목 버튼
label_slide1_title = tk.Label(
    master=frame_slide1,
    text="Sherpa",
    bg="purple",
    fg="white")
label_slide1_title.configure(font=font_title)
label_slide1_title.place(x=10, y=10)

# 프로파일 버튼
button_slide1_profile = tk.Button(
    master=frame_slide1,
    text="프로파일",
    width=12,
    height=1,
    bg="purple",
    fg="white",
    font=font_button
)
button_slide1_profile.place(x=0, y=150)

# img 레이블
label_slide2_img = tk.Label(frame_slide2)
label_slide2_img.grid()
# GUI 끝-------------------------------

cascadePath = "haarcascades/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
recognizer = cv2.face.LBPHFaceRecognizer_create()

recognizer.read('trainer/trainer.yml')

cvFont = cv2.FONT_HERSHEY_SIMPLEX

index_name_hash = {
    1: 'jiwon'
}

capture = cv2.VideoCapture(0)

# 최소 얼굴 사이즈
minimumFaceSize = int(0.1 * capture.get(4))


def returnImg():
    isReturn, img_bgr = capture.read()
    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    doesFaceInDB = False

    if not isReturn:
        return None
    faces = get_faces(img_gray)

    for (x, y, w, h) in faces:
        doesFaceInDB, name, percentage = predict(img_gray, x, y, w, h)
        img_bgr = drawEveryThing(img_bgr, x, y, w, h, name, percentage)
    return img_bgr


def predict(img_gray, x, y, w, h):
    index, confidence = recognizer.predict(img_gray[y:y + h, x:x + w])
    name = "unknown"
    percentage = 0
    isThere = False
    if confidence < 80:
        name = index_name_hash.get(index)
        percentage = round(100 - confidence, 2)
        isThere = True
        print(percentage, "퍼센트, 이름: ", name)

    return isThere, name, percentage


def drawEveryThing(img, x, y, w, h, name, percentage):
    img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    img = cv2.putText(img, str(name), (x + 5, y - 5), cvFont, 1, (255, 255, 255), 2)
    img = cv2.putText(img, str(percentage), (x + 5, y + h - 5), cvFont, 1, (255, 255, 0), 1)
    return img


def get_faces(img_gray):
    faces = faceCascade.detectMultiScale(
        img_gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(minimumFaceSize, minimumFaceSize)
    )
    return faces


def computeVision():
    # ------------------
    img_bgr = returnImg()
    # ------0.05~0.1sec-----
    img_bgr = cv2.resize(img_bgr, dsize=(0, 0), fx=0.5, fy=0.5)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    img_rgb = Image.fromarray(img_rgb)
    img_tkinter = ImageTk.PhotoImage(image=img_rgb)
    label_slide2_img.imgtk = img_tkinter
    label_slide2_img.configure(image=img_tkinter)
    label_slide2_img.after(10, computeVision)


if __name__ == '__main__':
    computeVision()
    window.mainloop()
