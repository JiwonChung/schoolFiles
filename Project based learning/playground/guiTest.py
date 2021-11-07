import tkinter as tk
import cv2
import dlib
import os
from PIL import ImageTk, Image
import numpy as numpy

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('models/shape_predictor_68_face_landmarks.dat')
facerec = dlib.face_recognition_model_v1('models/dlib_face_recognition_resnet_model_v1.dat')
cap = cv2.VideoCapture(0)
#
# while True:
#     # 동영상 파일에서 프레임 단위로 읽기
#     ret, img = cap.read()
#     if not ret:
#         break
#
#     faces = detector(img)
#     if len(faces) != 0:
#         for face in faces:
#             # dlib 객체 생성
#             dlib_shape = predictor(img, face)
#             # dlib 객체를 np로 변환
#             shape_2d = numpy.array([[p.x, p.y] for p in dlib_shape.parts()])
#             print(len(shape_2d))
#             # visualize
#             img = cv2.rectangle(img, pt1=(face.left(), face.top()), pt2=(face.right(), face.bottom()),
#                                 color=(255, 255, 255), thickness=2, lineType=cv2.LINE_AA)
#     # 출력
#     cv2.imshow('img', img)
#     # 1msec  만큼 기다리기
#     cv2.waitKey(1)

window = tk.Tk(className="정지원만세 - Windows Color")

# 라즈베리 디스플레이 사이즈
window.geometry("480x320+10+10")
window.configure(bg="black")
window.resizable(False, False)
# # 레이블
# label = tk.Label(
#     text="Sherpa",
#     foreground="green",
#     background="black",
#     width=13,
#     height=6
# )
# label.pack()
#
# button = tk.Button(
#     text = "Click me",
#     width = 25,
#     height = 5,
#     fg = "red",
#     bg = "blue"
# )
# button.pack()
#
# Font_tuple = ("Comic Sans MS", 20, "bold")
# label.configure(font=Font_tuple)

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


def show_frames():
    # Get the latest frame and convert into Image
    isReturnValue, img = cap.read()
    if not isReturnValue:
        return
    faces = detector(img)
    # 얼굴 1개만 아니면 계속 함
    if len(faces) != 0:
        for face in faces:
            # dlib 객체 생성
            dlib_shape = predictor(img, face)
            # dlib 객체를 numpy 객체로 변환
            shape_2d = numpy.array([[p.x, p.y] for p in dlib_shape.parts()])
            # color(b, g, r)
            img = cv2.rectangle(img, pt1=(face.left(), face.top()), pt2=(face.right(), face.bottom()),
                                color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
    img = cv2.resize(img, dsize=(0, 0), fx=0.5, fy=0.5)
    # print(img.shape)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    imagetk = ImageTk.PhotoImage(image=img)
    label_slide2_img.imgtk = imagetk
    label_slide2_img.configure(image=imagetk)
    label_slide2_img.after(1, show_frames)


show_frames()
window.mainloop()
