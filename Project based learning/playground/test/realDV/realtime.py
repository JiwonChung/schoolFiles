import threading
import time
from datetime import datetime
import cv2 as cv2
from PIL import ImageTk, Image
import tkinter as tk
import os
import numpy as np


class GlobalVariables:
    def __init__(self):
        self.count = 0
        self.previousName = ["", "", ""]

        self.doesFaceInDB_count = 0
        self.face_cascade = cv2.CascadeClassifier("C:\\Users\\jwchu\\Documents\\schoolFiles\\Project based "
                                                  "learning\\playground\\test\\haarcascades"
                                                  "\\haarcascade_frontalface_default.xml")
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()

        self.capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.cvFont = cv2.FONT_HERSHEY_SIMPLEX
        # 최소 얼굴 사이즈
        self.minimumFaceSize = int(0.1 * self.capture.get(4))
        # 시작시
        BASE_DIR = os.path.dirname("C:\\Users\\jwchu\\Documents\\schoolFiles\\Project based "
                                   "learning\\playground\\test\\realDV")
        image_dir = os.path.join(BASE_DIR, "dataset")
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
                    # print(label, "레이블, 아이디", id_)

                    # gray scaled 이미지 빙빙
                    grayScaled_image = Image.open(path).convert("L")

                    size = (320, 320)

                    # 안티에리어시드 이미지 빙빙
                    final_image = grayScaled_image.resize(size, Image.ANTIALIAS)

                    # 배열 형태로 빙빙
                    image_array = np.array(final_image, "uint8")

                    # 얼굴 케스케이드 빙빙
                    faces = self.get_faces(image_array)

                    for (x, y, w, h) in faces:
                        regionOfInterest = image_array[y: y + h, x: x + w]
                        x_train.append(regionOfInterest)
                        y_label.append(id_)

        self.recognizer.train(x_train, np.array(y_label))
        self.recognizer.save("recognizers/face-trainer.yml")

        self.recognizer.read("C:\\Users\\jwchu\\Documents\\schoolFiles\\Project based "
                             "learning\\playground\\test\\recognizers\\face-trainer.yml")

        self.index_name_hash = {y: x for x, y in label_ids.items()}
        print("index name", self.index_name_hash)

        self.foundPersonIndex = []

    def get_faces(self, img_gray):
        faces = self.face_cascade.detectMultiScale(
            img_gray,
            scaleFactor=1.3,
            minNeighbors=5,
            minSize=(self.minimumFaceSize, self.minimumFaceSize)
        )
        return faces


class GUI:
    def __init__(self, globalVariables):

        self.window = tk.Tk(className="정지원만세 - Windows Color")

        # 라즈베리 디스플레이 사이즈
        self.window.geometry("480x320+10+10")
        self.window.configure(bg="black")
        self.window.resizable(False, False)

        self.font_title = ("Microsoft YaHei UI", 20, "bold")
        self.font_button = ("Microsoft YaHei UI", 15, "bold")

        # 햄버거 슬라이드 프레임
        self.frame_slide1_left = tk.Frame(master=self.window, width=160, height=320, bg="purple")

        self.frame_slide1_left.grid(row=0, column=0)

        # 사진 나오는 프레임
        self.frame_slide1_right = tk.Frame(master=self.window, width=320, height=320, bg="blue")
        self.frame_slide1_right.grid(row=0, column=1)

        # 제목 버튼
        self.label_slide1_left_title = tk.Label(
            master=self.frame_slide1_left,
            text="셰비서",
            bg="purple",
            fg="white")
        self.label_slide1_left_title.configure(font=self.font_title)
        self.label_slide1_left_title.place(x=10, y=10)

        # 프로파일 버튼
        self.button_slide1_left_profile = tk.Button(
            master=self.frame_slide1_left,
            text="프로파일",
            width=12,
            height=1,
            bg="purple",
            fg="white",
            font=self.font_button,
            command=lambda: self.uploadLeftSide(str(globalVariables.count))
        )
        self.button_slide1_left_profile.place(x=0, y=100)

        # img 레이블
        self.label_slide1_right_img = tk.Label(self.frame_slide1_right)
        self.label_slide1_right_img.grid()

        # found people
        self.label_slide1_left_foundPerson1 = tk.Label(
            master=self.frame_slide1_left,
            bg="purple",
            fg="yellow",
            font=self.font_button
        )
        self.label_slide1_left_foundPerson2 = tk.Label(
            master=self.frame_slide1_left,
            bg="purple",
            fg="yellow",
            font=self.font_button
        )
        self.label_slide1_left_foundPerson3 = tk.Label(
            master=self.frame_slide1_left,
            bg="purple",
            fg="yellow",
            font=self.font_button
        )

        # 언너운
        self.button_slide1_left_unknown = tk.Button(
            master=self.frame_slide1_left,
            text="Unknown",
            width=12,
            height=1,
            bg="purple",
            fg="white",
            font=self.font_button,
            command=saveFace
        )

    def uploadLeftSide(self, name):
        globalVariables.count += 1
        count = globalVariables.count % 3
        if count % 3 == 1:
            self.label_slide1_left_foundPerson1.config(text=name)
            self.label_slide1_left_foundPerson1.place(x=0, y=150)
            globalVariables.previousName[0] = name
            threading.Timer(3, lambda: self.afterTimer(1))
        elif count % 3 == 2:
            self.label_slide1_left_foundPerson2.config(text=name)
            self.label_slide1_left_foundPerson2.place(x=0, y=180)
            globalVariables.previousName[1] = name
            threading.Timer(3, lambda: self.afterTimer(2))
        else:
            self.label_slide1_left_foundPerson3.config(text=name)
            self.label_slide1_left_foundPerson3.place(x=0, y=210)
            globalVariables.previousName[2] = name
            threading.Timer(3, lambda: self.afterTimer(3))

    def afterTimer(self, index):
        if index is 1:
            self.label_slide1_left_foundPerson1.place_forget()
            globalVariables.previousName[0] = ""
        elif index is 2:
            self.label_slide1_left_foundPerson2.place_forget()
            globalVariables.previousName[1] = ""
        else:
            self.label_slide1_left_foundPerson3.place_forget()
            globalVariables.previousName[2] = ""

    def showUnknown(self):
        if globalVariables.doesFaceInDB_count >= 10:
            self.button_slide1_left_unknown.place(x=0, y=240)
        elif globalVariables.doesFaceInDB_count < -20:
            self.button_slide1_left_unknown.place_forget()


def saveFace():
    # roi gray 로 연사 조지고 (tmp 로 저장) 10장 찍기
    # 아이디 받고
    # dataset 에 저장하기
    print("start shoot")
    count = 1
    while True:
        _, img = globalVariables.capture.read()
        grayScaledImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = globalVariables.get_faces(grayScaledImage)
        for (x, y, w, h) in faces:
            cv2.imwrite("C:\\Users\\jwchu\\Documents\\schoolFiles\\Project based "
                        "learning\\playground\\test\\dataset\\tmp\\" + str(count) + '.jpg',
                        grayScaledImage[y: y + h, x: x + w])

            count += 1
        if count == 11:
            print("shoot done")
            break


class Square:
    def __init__(self, gui, globalVariables):
        self.gui = gui
        self.globalVariables = globalVariables

    def returnImg(self):
        isReturn, img_bgr = globalVariables.capture.read()
        img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

        if not isReturn:
            return None
        faces = globalVariables.get_faces(img_gray)

        for (x, y, w, h) in faces:
            index = self.predict(img_gray, x, y, w, h)
            if index == -1:
                name = "unknown"
            elif index < -1:
                pass
            else:
                name = globalVariables.index_name_hash.get(index)
                if name is None:
                    pass
                flag = False
                for n in globalVariables.previousName:
                    if n == name:
                        flag = True
                        break
                if not flag:
                    gui.uploadLeftSide(name)
                # else:
                #     globalVariables.previousName = name
            img_bgr = self.drawEveryThing(img_bgr, x, y, w, h, name)
        return img_bgr

    def predict(self, img_gray, x, y, w, h):
        regionOfInterest_gray = img_gray[y: y + h, x: x + w]
        index, confidence = globalVariables.recognizer.predict(regionOfInterest_gray)
        print("index: ", index)
        print("condidence: ", confidence)
        if 45 < confidence < 70:
            if globalVariables.doesFaceInDB_count >= 10:
                globalVariables.doesFaceInDB_count = 10
            globalVariables.doesFaceInDB_count -= 1
        else:
            index = -1
            if globalVariables.doesFaceInDB_count < 0:
                globalVariables.doesFaceInDB_count = 0
            globalVariables.doesFaceInDB_count += 1
        return index

    def drawEveryThing(self, img, x, y, w, h, name):
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        img = cv2.putText(img, str(name), (x + 5, y - 5), globalVariables.cvFont, 1, (255, 255, 255), 2)
        return img

    def computeVision(self):
        # ------------------
        img_bgr = self.returnImg()
        # ------0.05~0.1sec-----
        img_bgr = cv2.resize(img_bgr, dsize=(0, 0), fx=0.5, fy=0.5)
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        img_rgb = Image.fromarray(img_rgb)
        img_tkinter = ImageTk.PhotoImage(image=img_rgb)
        gui.label_slide1_right_img.imgtk = img_tkinter
        gui.label_slide1_right_img.configure(image=img_tkinter)

        # 언너운 감지하기
        gui.showUnknown()

        gui.label_slide1_right_img.after(10, self.computeVision)


if __name__ == '__main__':
    globalVariables = GlobalVariables()
    gui = GUI(globalVariables)

    square = Square(gui, globalVariables)
    square.computeVision()
    gui.window.mainloop()
