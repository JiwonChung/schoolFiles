import threading
from datetime import datetime
import cv2 as cv2
from PIL import ImageTk, Image
import tkinter as tk


class GlobalVariables:
    def __init__(self):
        self.count = 0

        self.isUnknown = False
        self.cascadePath = "C:\\Users\\jwchu\\Documents\\schoolFiles\\Project based " \
                           "learning\\playground\\test\\haarcascades\\haarcascade_frontalface_default.xml "
        self.faceCascade = cv2.CascadeClassifier(self.cascadePath)
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        now = datetime.now()
        self.recognizer.read("C:\\Users\\jwchu\\Documents\\schoolFiles\\Project based "
                             "learning\\playground\\test\\trainer\\trainer.yml")
        print(datetime.now() - now)
        self.cvFont = cv2.FONT_HERSHEY_SIMPLEX
        self.index_name_hash = {
            1: 'jiwon'
        }
        self.capture = cv2.VideoCapture(0)
        # 최소 얼굴 사이즈
        self.minimumFaceSize = int(0.1 * self.capture.get(4))


class GUI:
    def __init__(self, globalVariables):
        self.window = tk.Tk(className="정지원만세 - Windows Color")

        # 라즈베리 디스플레이 사이즈
        self.window.geometry("480x320+10+10")
        self.window.configure(bg="black")
        self.window.resizable(False, False)

        self.font_title = ("Microsoft YaHei UI", 20, "bold")
        self.font_button = ("Microsoft YaHei UI", 15, "bold")

        self.stack = [False, False, False]

        # 햄버거 슬라이드 프레임
        self.frame_slide1_left = tk.Frame(master=self.window, width=160, height=320, bg="purple")

        self.frame_slide1_left.grid(row=0, column=0)

        # 사진 나오는 프레임
        self.frame_slide1_right = tk.Frame(master=self.window, width=320, height=320, bg="blue")
        self.frame_slide1_right.grid(row=0, column=1)

        # 제목 버튼
        self.label_slide1_left_title = tk.Label(
            master=self.frame_slide1_left,
            text="Sherpa",
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
            command=lambda: self.wait5sec(str(globalVariables.count))

        )
        self.button_slide1_left_profile.place(x=0, y=100)

        # img 레이블
        self.label_slide2_img = tk.Label(self.frame_slide1_right)
        self.label_slide2_img.grid()

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

    def wait5sec(self, name):
        globalVariables.count += 1
        if not self.stack[0]:
            self.label_slide1_left_foundPerson1.config(text=name)
            self.label_slide1_left_foundPerson1.place(x=0, y=150)
            threading.Timer(5, lambda: self.dropLabel(self.label_slide1_left_foundPerson1, 0)).start()
            self.stack[0] = True
        elif not self.stack[1]:
            self.label_slide1_left_foundPerson2.config(text=name)
            self.label_slide1_left_foundPerson2.place(x=0, y=180)
            threading.Timer(5, lambda: self.dropLabel(self.label_slide1_left_foundPerson2, 1)).start()
            self.stack[1] = True
        elif not self.stack[2]:
            self.label_slide1_left_foundPerson3.config(text=name)
            self.label_slide1_left_foundPerson3.place(x=0, y=210)
            threading.Timer(5, lambda: self.dropLabel(self.label_slide1_left_foundPerson3, 2)).start()
            self.stack[2] = True

    def dropLabel(self, label, index):
        label.config(text="")
        self.stack[0] = False
        # 첫번 째
        if index == 0 and self.stack[1] is True:
            name2 = self.label_slide1_left_foundPerson2['text']
            self.label_slide1_left_foundPerson1.config(text=name2)
            self.stack[0] = True
            self.stack[1] = False
            if self.stack[2] is True:
                name3 = self.label_slide1_left_foundPerson3['text']
                self.label_slide1_left_foundPerson2.config(text=name3)
                self.label_slide1_left_foundPerson3.config(text="")
                self.stack[1] = True
                self.stack[2] = False
            else:
                self.label_slide1_left_foundPerson2.config(text="")
        if index == 1 and self.stack[2] is False:
            self.label_slide1_left_foundPerson1.config(text="")
            self.stack[1] = False
        if index == 2:
            self.label_slide1_left_foundPerson2.config(text="")
            self.stack[2] = False


class Square:
    def __init__(self, gui, globalVariables):
        self.gui = gui
        self.globalVariables = globalVariables

    def returnImg(self):
        isReturn, img_bgr = globalVariables.capture.read()
        img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

        if not isReturn:
            return None
        faces = self.get_faces(img_gray)

        for (x, y, w, h) in faces:
            doesFaceInDB, name, percentage = self.predict(img_gray, x, y, w, h)
            img_bgr = self.drawEveryThing(img_bgr, x, y, w, h, name, percentage)

            globalVariables.isUnknown = doesFaceInDB
        return img_bgr

    def predict(self, img_gray, x, y, w, h):
        index, confidence = globalVariables.recognizer.predict(img_gray[y:y + h, x:x + w])
        name = "unknown"
        percentage = 0
        isThere = False
        if confidence < 80:
            name = globalVariables.index_name_hash.get(index)
            percentage = round(100 - confidence, 2)
            isThere = True
            print(percentage, "퍼센트, 이름: ", name)

        return isThere, name, percentage

    def drawEveryThing(self, img, x, y, w, h, name, percentage):
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        img = cv2.putText(img, str(name), (x + 5, y - 5), globalVariables.cvFont, 1, (255, 255, 255), 2)
        img = cv2.putText(img, str(percentage), (x + 5, y + h - 5), globalVariables.cvFont, 1, (255, 255, 0), 1)
        return img

    def get_faces(self, img_gray):
        faces = globalVariables.faceCascade.detectMultiScale(
            img_gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(globalVariables.minimumFaceSize, globalVariables.minimumFaceSize)
        )
        return faces

    def computeVision(self):
        # ------------------
        img_bgr = self.returnImg()
        # ------0.05~0.1sec-----
        img_bgr = cv2.resize(img_bgr, dsize=(0, 0), fx=0.5, fy=0.5)
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        img_rgb = Image.fromarray(img_rgb)
        img_tkinter = ImageTk.PhotoImage(image=img_rgb)
        gui.label_slide2_img.imgtk = img_tkinter
        gui.label_slide2_img.configure(image=img_tkinter)
        gui.label_slide2_img.after(10, self.computeVision)


if __name__ == '__main__':
    globalVariables = GlobalVariables()
    gui = GUI(globalVariables)

    square = Square(gui, globalVariables)

    square.computeVision()
    gui.window.mainloop()
