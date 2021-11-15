import threading
import time
import tkinter as tk
from datetime import datetime

import cv2
import dlib
from PIL import ImageTk, Image
import numpy as numpy

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('models/shape_predictor_68_face_landmarks.dat')
facerec = dlib.face_recognition_model_v1('models/dlib_face_recognition_resnet_model_v1.dat')
cap = cv2.VideoCapture(0)

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
# ------------------    GUI end   --------------------


# 내 얼굴 npy 파일
savedDescriptors = {
    'Jiwon': numpy.load('img/desc.npy', allow_pickle=True)
}


# 프레임 뽑기
def show_frames():
    now = datetime.now()
    # Get the latest frame and convert into Image
    isReturnValue, img = cap.read()
    if not isReturnValue:
        return
    rects, shapes, shapes_np = find_faces(img)

    # 얼굴 0개만 아니면 계속 함
    if len(rects) != 0:
        for i, name in enumerate(useEuclideanDistance(encode_faces(img, shapes))):
            img = cv2.rectangle(img, pt1=(rects[i][0][0], rects[i][0][1]), pt2=(rects[i][1][0], rects[i][1][1]),
                                color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
            img = cv2.putText(img, name, (rects[i][0][0], rects[i][0][1]), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
                              2, (0, 255, 255), 3, cv2.LINE_8)  # 폰트, 숫자, 색, 라인 유형 선택하기

    # 이 부분을 따로 분리했으면 좋겠음
    img = cv2.resize(img, dsize=(0, 0), fx=0.5, fy=0.5)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    imagetk = ImageTk.PhotoImage(image=img)
    label_slide2_img.imgtk = imagetk
    label_slide2_img.configure(image=imagetk)
    # print(datetime.now() - now)
    label_slide2_img.after(100, show_frames)


# find_faces fuction's param should be rgb img file
# for loop up
def find_faces(img):
    global shape, k
    dets = detector(img, 1)
    # 얼굴을 하나도 찾지 못했을 경우 return 빈 배열
    if len(dets) == 0:
        return numpy.empty(0), numpy.empty(0), numpy.empty(0)

    # 결과물 저장할 변수들
    rects, shapes = [], []
    shapes_np = numpy.zeros((len(dets), 68, 2), dtype=int)

    for k, d in enumerate(dets):
        rect = ((d.left(), d.top()), (d.right(), d.bottom()))
        rects.append(rect)

        # 랜드마크 구하기
        shape = predictor(img, d)
        shapes.append(shape)

    print(len(shapes))
    # numpy array 로 바꾸기
    for i in range(0, 68):
        shapes_np[k][i] = (shape.part(i).x, shape.part(i).y)

    return rects, shapes, shapes_np


# 68개의 점 -> 128개의 벡터
def encode_faces(img, shapes):
    face_descriptors = []
    for s in shapes:
        face_descriptor = facerec.compute_face_descriptor(img, s)
        face_descriptors.append(numpy.array(face_descriptor))

    return numpy.array(face_descriptors)


# 유클리드 디스턴스를 계산
def useEuclideanDistance(receivedDescriptors):
    # print(len(receivedDescriptors))
    names = []

    # input 불러 오기
    for receivedDescriptor in receivedDescriptors:
        # 저장된거 불러오기
        for name, savedDescriptor in savedDescriptors.items():
            # 저장된 거랑 비교하기
            distance = numpy.linalg.norm([receivedDescriptor] - savedDescriptor, axis=1)
            if distance < 0.6:
                names.append(name)
            else:
                names.append('unknown')
    print(names)
    return names


show_frames()
window.mainloop()

