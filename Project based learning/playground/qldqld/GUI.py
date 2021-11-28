import os
import threading
import tkinter as tk
from datetime import datetime
import cv2
import numpy as np
from PIL import ImageTk, Image
import face_recognition
import glob

video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)


class Initializer:
    def __init__(self):
        self.knownCount = 0

        # 얼굴 인코딩 값을 배열로 저장
        self.label_ids = []
        self.encodings = []
        self.paths = []
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        image_dir = os.path.join(BASE_DIR, "img")
        counter = 0
        for root, dirs, files in os.walk(image_dir):
            for file in files:
                if file.endswith('png') or file.endswith('jpg'):
                    path = os.path.join(root, file)
                    self.paths.append(path)
                    label = file.split('.')[0]
                    self.label_ids.append(label)
                    img = face_recognition.load_image_file(path)
                    # print(img)
                    a = face_recognition.face_encodings(img)
                    # 얼굴을 찾지 못 했을 때
                    if len(a) != 0:
                        encoding = face_recognition.face_encodings(img)[0]
                        self.encodings.append(encoding)
                    counter += 1
        # ---------------------------------


class RecognizeFace:
    def __init__(self, initializer, view):
        self.init = initializer

        # Initialize some variables
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.process_this_frame = 0
        self.face_names = []

    def returnImg(self):
        # 사진 읽어오기
        _, received_image = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_image = cv2.resize(received_image, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = cv2.cvtColor(small_image, cv2.COLOR_BGR2RGB)

        # Only process every other frame of video to save time
        if self.process_this_frame % 3 == 0:
            # Find all the faces and face encodings in the current frame of video
            self.face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

            self.face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(self.init.encodings, face_encoding)
                name = "Unknown"

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(self.init.encodings, face_encoding)
                print("face_distance: ", face_distances)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index] and face_distances[best_match_index] < 0.65:
                    print("best_match_index: ", best_match_index)
                    name = self.init.label_ids[best_match_index]
                    init.knownCount -= 1
                    if init.knownCount >= 3:
                        init.knownCount = 3
                else:
                    if init.knownCount < 0:
                        init.knownCount = 0
                    init.knownCount += 1

                self.face_names.append(name)
            print(self.face_names)

        self.process_this_frame += 1

        # return img
        for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            received_image = cv2.rectangle(received_image, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            received_image = cv2.rectangle(received_image, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            received_image = cv2.putText(received_image, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        return received_image

    def computeVision(self):
        if view.viewVariable == 0:
            img = self.returnImg()
            img = cv2.resize(img, dsize=(0, 0), fx=0.5, fy=0.5)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_rgb = Image.fromarray(img_rgb)
            img_tkinter = ImageTk.PhotoImage(image=img_rgb)
            view.label_slide1_right_img.imgtk = img_tkinter
            view.label_slide1_right_img.configure(image=img_tkinter)
            view.showUnknown()
        view.label_slide1_right_img.after(1, self.computeVision)


class View:
    def __init__(self, init):
        self.profileIndex = 0

        self.profiles = []
        for i in range(len(init.label_ids)):
            self.profiles.append(Profile(init.label_ids[i], init.paths[i], i))

        # 0은 기본화면, 1은 등록화면, 3은 프로파일
        self.viewVariable = 0

        self.count = 0

        self.previousName = ["", "", ""]
        self.doesFaceInDB_count = 0
        self.window = tk.Tk(className="정지원만세 - Raspberry Pi Color")

        # 라즈베리 디스플레이 사이즈
        self.window.geometry("480x320+10+10")
        self.window.configure(bg="black")
        self.window.resizable(False, False)

        self.font_title = ("Microsoft YaHei UI", 20, "bold")
        self.font_button = ("Microsoft YaHei UI", 15, "bold")
        self.font_little = ("Microsoft YaHei UI", 10, "bold")

        # 햄버거 슬라이드 프레임
        self.frame_slide1_left = tk.Frame(master=self.window, width=160, height=320, bg="purple")
        self.frame_slide1_left.grid(row=0, column=0)

        # 사진 나오는 프레임
        self.frame_slide1_right = tk.Frame(master=self.window, width=320, height=320, bg="blue")
        self.frame_slide1_right.grid(row=0, column=1)

        # 햄버거 슬라이드 프레임
        self.frame_slide2_left = tk.Frame(master=self.window, width=160, height=320, bg="purple")
        # self.frame_slide2_left.grid(row=0, column=0)

        # 사진 나오는 프레임
        self.frame_slide2_right = tk.Frame(master=self.window, width=320, height=320, bg="blue")
        # self.frame_slide2_right.grid(row=0, column=1)

        # 햄버거 슬라이드 프레임
        self.frame_slide3_left = tk.Frame(master=self.window, width=160, height=320, bg="purple")
        # self.frame_slide3_left.grid(row=0, column=0)

        # 사진 나오는 프레임
        self.frame_slide3_right = tk.Frame(master=self.window, width=320, height=320, bg="blue")
        # self.frame_slide3_right.grid(row=0, column=1)

# --------------------------------------기본화면 시작--------------------------------------------------------------
        # 제목 - 기본화면
        self.label_slide1_left_title = tk.Label(
            master=self.frame_slide1_left,
            text="셰비서",
            bg="purple",
            fg="white",
            font=self.font_title
        )
        self.label_slide1_left_title.place(x=10, y=10)

        # 프로파일 버튼 - 기본화면
        self.button_slide1_left_profile = tk.Button(
            master=self.frame_slide1_left,
            text="프로파일",
            width=12,
            height=1,
            bg="purple",
            fg="white",
            font=self.font_button,
            command=self.button_slide1_left_profile_callback
        )
        self.button_slide1_left_profile.place(x=0, y=70)

        # 언너운 버튼 - 기본화면
        self.button_slide1_left_unknown = tk.Button(
            master=self.frame_slide1_left,
            text="Unknown",
            width=12,
            height=1,
            bg="purple",
            fg="white",
            font=self.font_button,
            command=self.button_slide1_left_unknown_callback
        )
        # self.button_slide1_left_unknown.place(x=0, y=100)

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
        # img 레이블
        self.label_slide1_right_img = tk.Label(self.frame_slide1_right)
        self.label_slide1_right_img.grid()

# --------------------------------------등록화면 시작--------------------------------------------------------------

        # 제목 - 등록화면
        self.label_slide2_left_title = tk.Label(
            master=self.frame_slide2_left,
            text="등록",
            bg="purple",
            fg="white",
            font=self.font_title
        )
        # self.label_slide2_left_title.place(x=10, y=10)

        # 이름 받는  Entry
        self.entry_slide2_left_nameInput = tk.Entry(
            master=self.frame_slide2_left,
            width=12,
            font=self.font_button
        )
        self.entry_slide2_left_nameInput.bind("<FocusIn>", lambda args: self.entry_slide2_left_nameInput.delete(0, tk.END))
        # self.entry_slide2_left_nameInput.place(x=0, y=70)

        # 키보드를 대체할 문자 3개
        self.button_slide2_left_A = tk.Button(
            master=self.frame_slide2_left,
            width=3,
            height=1,
            font=self.font_button,
            text="A",
            bg="purple",
            fg="white",
            command=lambda: self.entry_slide2_left_nameInput.insert(tk.END, 'A')
        )
        # self.button_slide2_left_A.place(x=0, y=180)
        self.button_slide2_left_B = tk.Button(
            master=self.frame_slide2_left,
            width=3,
            height=1,
            font=self.font_button,
            text="B",
            bg="purple",
            fg="white",
            command=lambda: self.entry_slide2_left_nameInput.insert(tk.END, 'B')
        )
        # self.button_slide2_left_B.place(x=55, y=180)
        self.button_slide2_left_C = tk.Button(
            master=self.frame_slide2_left,
            width=3,
            height=1,
            font=self.font_button,
            text="C",
            bg="purple",
            fg="white",
            command=lambda: self.entry_slide2_left_nameInput.insert(tk.END, 'C')
        )
        # self.button_slide2_left_C.place(x=110, y=180)

        # 취소 버튼
        self.button_slide2_left_cancel = tk.Button(
            master=self.frame_slide2_left,
            width=3,
            height=1,
            font=self.font_button,
            text="취소",
            bg="purple",
            fg="white",
            command=self.button_slide2_left_cancel_callback
        )
        # self.button_slide2_left_cancel.place(x=0, y=250)
        # 확인 버튼
        self.button_slide2_left_confirm = tk.Button(
            master=self.frame_slide2_left,
            width=3,
            height=1,
            font=self.font_button,
            text="확인",
            bg="purple",
            fg="white",
            command=self.button_slide2_left_confirm_callback
        )
        # self.button_slide2_left_confirm.place(x=110, y=250)

        # img 레이블
        self.label_slide2_right_img = tk.Label(self.frame_slide2_right)
        # self.label_slide2_right_img.grid()

# --------------------------------------프로파일 화면 시작--------------------------------------------------------------
        # 제목 - 프로파일 화면
        self.label_slide3_left_title = tk.Label(
            master=self.frame_slide3_left,
            text="프로파일",
            bg="purple",
            fg="white",
            font=self.font_title
        )
        # self.label_slide3_left_title.place(x=10, y=10)

        # 이름
        self.label_slide3_left_name = tk.Label(
            master=self.frame_slide3_left,
            text="이름: " + self.profiles[self.profileIndex].get_name(),
            bg="purple",
            fg="white",
            font=self.font_button
        )
        # self.label_slide3_left_name.place(x=0, y=70)

        # 인덱스
        self.label_slide3_left_index = tk.Label(
            master=self.frame_slide3_left,
            text=str(self.profiles[self.profileIndex].get_id() + 1) + "/" + str(len(self.profiles)),
            bg="purple",
            fg="white",
            font=self.font_little
        )
        # self.label_slide3_left_index.place(x=60, y=100)

        # to left
        self.button_slide3_left_left = tk.Button(
            master=self.frame_slide3_left,
            text='<',
            width=3,
            height=1,
            bg="purple",
            fg="white",
            font=self.font_title,
            command=self.button_slide3_left_left_callback
        )
        # self.button_slide3_left_left.place(x=0, y=250)

        # to right
        self.button_slide3_left_right = tk.Button(
            master=self.frame_slide3_left,
            text='>',
            width=3,
            height=1,
            bg="purple",
            fg="white",
            font=self.font_title,
            command=self.button_slide3_left_right_callback
        )
        # self.button_slide3_left_right.place(x=100, y=250)

        # 수정
        self.button_slide3_left_edit = tk.Button(
            master=self.frame_slide3_left,
            text='수정',
            width=3,
            height=1,
            bg="purple",
            fg="white",
            font=self.font_little,
            command=self.button_slide3_left_edit_callback
        )
        # self.button_slide3_left_edit.place(x=40, y=200)

        # 삭제
        self.button_slide3_left_delete = tk.Button(
            master=self.frame_slide3_left,
            text='삭제',
            width=3,
            height=1,
            bg="purple",
            fg="white",
            font=self.font_little,
            command=self.button_slide3_left_delete_callback
        )
        # self.button_slide3_left_delete.place(x=90, y=200)

        # img 레이블
        self.label_slide3_right_img = tk.Label(self.frame_slide3_right)
        # self.label_slide3_right_img.grid()

    def showUnknown(self):
        if init.knownCount >= 3:
            self.button_slide1_left_unknown.place(x=0, y=240)
        elif init.knownCount < -5:
            self.button_slide1_left_unknown.place_forget()

    def uploadLeftSide(self, name):
        self.count += 1
        count = self.count % 3
        if count % 3 == 1:
            self.label_slide1_left_foundPerson1.config(text=name)
            self.label_slide1_left_foundPerson1.place(x=0, y=150)
            self.previousName[0] = name
            threading.Timer(3, lambda: self.afterTimer(1))
        elif count % 3 == 2:
            self.label_slide1_left_foundPerson2.config(text=name)
            self.label_slide1_left_foundPerson2.place(x=0, y=180)
            self.previousName[1] = name
            threading.Timer(3, lambda: self.afterTimer(2))
        else:
            self.label_slide1_left_foundPerson3.config(text=name)
            self.label_slide1_left_foundPerson3.place(x=0, y=210)
            self.previousName[2] = name
            threading.Timer(3, lambda: self.afterTimer(3))

    def afterTimer(self, index):
        if index == 1:
            self.label_slide1_left_foundPerson1.place_forget()
            self.previousName[0] = ""
        elif index == 2:
            self.label_slide1_left_foundPerson2.place_forget()
            self.previousName[1] = ""
        else:
            self.label_slide1_left_foundPerson3.place_forget()
            self.previousName[2] = ""

    def button_slide1_left_unknown_callback(self):
        # 사진 찍고
        # 이름 받기
        _, cam = video_capture.read()
        cv2.imwrite("img/tmp.jpg", cam)

        # 사진 넘겨주기
        img = cv2.resize(cam, dsize=(0, 0), fx=0.5, fy=0.5)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_rgb = Image.fromarray(img_rgb)
        img_tkinter = ImageTk.PhotoImage(image=img_rgb)
        self.label_slide2_right_img.imgtk = img_tkinter
        self.label_slide2_right_img.configure(image=img_tkinter)

        self.viewVariable = 1
        self.viewController()

    def button_slide1_left_profile_callback(self):
        self.profileIndex = 0
        _profile = self.profiles[self.profileIndex]

        # 사진 넘겨주기
        cam = cv2.imread(_profile.get_imagePath(), cv2.IMREAD_COLOR)
        img = cv2.resize(cam, dsize=(0, 0), fx=0.5, fy=0.5)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_rgb = Image.fromarray(img_rgb)
        img_tkinter = ImageTk.PhotoImage(image=img_rgb)
        self.label_slide3_right_img.imgtk = img_tkinter
        self.label_slide3_right_img.configure(image=img_tkinter)

        # 이름 수정하기
        self.label_slide3_left_name.config(text="이름: " + _profile.get_name())

        # 인덱스 수정하기
        self.label_slide3_left_index.config(text=str(_profile.get_id() + 1) + "/" + str(len(self.profiles)))

        self.viewVariable = 2
        self.viewController()

    def button_slide2_left_cancel_callback(self):
        # 사진 지우고 1번으로 이동
        filePath = "img/tmp.jpg"
        if os.path.isfile(filePath):
            os.remove(filePath)
        self.viewVariable = 0
        self.viewController()

    def button_slide2_left_confirm_callback(self):
        _profile = self.profiles[self.profileIndex]
        old_path = "img/" + _profile.get_name() + ".jpg"
        new_name = 'img/' + self.entry_slide2_left_nameInput.get() + '.jpg'
        if os.path.isfile(old_path):
            os.rename(old_path, new_name)
        self.profiles[self.profileIndex].set_name(self.entry_slide2_left_nameInput.get())
        self.profiles[self.profileIndex].set_imagePath('C:\\Users\\jwchu\\Documents\\schoolFiles\\Project based '
                                                       'learning\\playground\\qldqld\\img\\' + self.entry_slide2_left_nameInput.get() + '.jpg')
        self.viewVariable = 0
        # 곧바로 사용 할 거면 여기서 학습
        self.viewController()

    def button_slide3_left_left_callback(self):

        # self.label_slide3_left_name
        # self.label_slide3_left_index
        if self.profileIndex != 0:
            self.profileIndex -= 1
            _profile = self.profiles[self.profileIndex]

            # 이미지 수정하기
            image = cv2.imread(_profile.get_imagePath(), cv2.IMREAD_COLOR)
            img = cv2.resize(image, dsize=(0, 0), fx=0.5, fy=0.5)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_rgb = Image.fromarray(img_rgb)
            img_tkinter = ImageTk.PhotoImage(image=img_rgb)
            self.label_slide3_right_img.imgtk = img_tkinter
            self.label_slide3_right_img.configure(image=img_tkinter)

            # 이름 수정하기
            self.label_slide3_left_name.config(text="이름: " + _profile.get_name())

            # 인덱스 수정하기
            self.label_slide3_left_index.config(text=str(_profile.get_id() + 1) + "/" + str(len(self.profiles)))
            # 필요한지 아직 모르겠음
            # self.viewController()

    def button_slide3_left_right_callback(self):
        if self.profileIndex != len(self.profiles) - 1:
            self.profileIndex += 1
            _profile = self.profiles[self.profileIndex]

            # 이미지 수정하기
            image = cv2.imread(_profile.get_imagePath(), cv2.IMREAD_COLOR)
            img = cv2.resize(image, dsize=(0, 0), fx=0.5, fy=0.5)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_rgb = Image.fromarray(img_rgb)
            img_tkinter = ImageTk.PhotoImage(image=img_rgb)
            self.label_slide3_right_img.imgtk = img_tkinter
            self.label_slide3_right_img.configure(image=img_tkinter)

            # 이름 수정하기
            self.label_slide3_left_name.config(text="이름: " + _profile.get_name())

            # 인덱스 수정하기
            self.label_slide3_left_index.config(text=str(_profile.get_id() + 1) + "/" + str(len(self.profiles)))
        # self.viewController()

    def button_slide3_left_edit_callback(self):
        cam = cv2.imread(self.profiles[self.profileIndex].get_imagePath(), cv2.IMREAD_COLOR)

        # 사진 넘겨주기
        img = cv2.resize(cam, dsize=(0, 0), fx=0.5, fy=0.5)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_rgb = Image.fromarray(img_rgb)
        img_tkinter = ImageTk.PhotoImage(image=img_rgb)
        self.label_slide2_right_img.imgtk = img_tkinter
        self.label_slide2_right_img.configure(image=img_tkinter)

        # 이름 넘겨주기
        self.entry_slide2_left_nameInput.delete(0, tk.END)
        self.entry_slide2_left_nameInput.insert(0, self.profiles[self.profileIndex].get_name())

        self.viewVariable = 1
        self.viewController()

    def button_slide3_left_delete_callback(self):
        # 파일에서 삭제하고
        filePath = self.profiles[self.profileIndex].get_imagePath()
        if os.path.isfile(filePath):
            os.remove(filePath)
        # 프로파일에서 삭제하기
        del (self.profiles[self.profileIndex])
        for f in self.profiles:
            if f.get_id() > self.profileIndex:
                f.set_id(f.get_id() - 1)

        self.viewVariable = 0
        self.viewController()

    def viewController(self):
        if self.viewVariable == 0:
            # 2번 지우기
            self.label_slide2_left_title.place_forget()
            self.entry_slide2_left_nameInput.place_forget()
            self.button_slide2_left_A.place_forget()
            self.button_slide2_left_B.place_forget()
            self.button_slide2_left_C.place_forget()
            self.button_slide2_left_cancel.place_forget()
            self.button_slide2_left_confirm.place_forget()
            self.label_slide2_right_img.place_forget()
            self.frame_slide2_left.grid_forget()
            self.frame_slide2_right.grid_forget()

            # 3번 지우기
            self.label_slide3_left_title.place_forget()
            self.label_slide3_left_index.place_forget()
            self.label_slide3_left_name.place_forget()
            self.button_slide3_left_right.place_forget()
            self.button_slide3_left_left.place_forget()
            self.button_slide3_left_edit.place_forget()
            self.button_slide3_left_delete.place_forget()
            self.label_slide3_right_img.place_forget()
            self.frame_slide3_left.grid_forget()
            self.frame_slide3_right.grid_forget()

            # 1번 띄우기
            self.frame_slide1_left.grid(row=0, column=0)
            self.frame_slide1_right.grid(row=0, column=1)
            self.label_slide1_left_title.place(x=10, y=10)
            self.button_slide1_left_profile.place(x=0, y=70)
            self.label_slide1_right_img.grid()
            # 프로세싱 시작

        elif self.viewVariable == 1:
            # 1번 지우기
            self.label_slide1_left_title.place_forget()
            self.button_slide1_left_profile.place_forget()
            self.button_slide1_left_unknown.place_forget()
            self.label_slide1_left_foundPerson1.place_forget()
            self.label_slide1_left_foundPerson2.place_forget()
            self.label_slide1_left_foundPerson3.place_forget()
            self.label_slide1_right_img.place_forget()
            self.frame_slide1_left.grid_forget()
            self.frame_slide1_right.grid_forget()

            # 3번 지우기
            self.label_slide3_left_title.place_forget()
            self.label_slide3_left_index.place_forget()
            self.label_slide3_left_name.place_forget()
            self.button_slide3_left_right.place_forget()
            self.button_slide3_left_left.place_forget()
            self.button_slide3_left_edit.place_forget()
            self.button_slide3_left_delete.place_forget()
            self.label_slide3_right_img.place_forget()
            self.frame_slide3_left.grid_forget()
            self.frame_slide3_right.grid_forget()

            # 2번 띄우기
            self.frame_slide2_left.grid(row=0, column=0)
            self.frame_slide2_right.grid(row=0, column=1)
            self.label_slide2_left_title.place(x=10, y=10)
            self.entry_slide2_left_nameInput.place(x=0, y=70)
            self.button_slide2_left_A.place(x=0, y=180)
            self.button_slide2_left_B.place(x=55, y=180)
            self.button_slide2_left_C.place(x=110, y=180)
            self.button_slide2_left_cancel.place(x=0, y=250)
            self.button_slide2_left_confirm.place(x=110, y=250)
            self.label_slide2_right_img.grid()

        else:
            # 1번 지우기
            self.label_slide1_left_title.place_forget()
            self.button_slide1_left_profile.place_forget()
            self.button_slide1_left_unknown.place_forget()
            self.label_slide1_left_foundPerson1.place_forget()
            self.label_slide1_left_foundPerson2.place_forget()
            self.label_slide1_left_foundPerson3.place_forget()
            self.label_slide1_right_img.place_forget()
            self.frame_slide1_left.grid_forget()
            self.frame_slide1_right.grid_forget()

            # 2번 지우기
            self.label_slide2_left_title.place_forget()
            self.entry_slide2_left_nameInput.place_forget()
            self.button_slide2_left_A.place_forget()
            self.button_slide2_left_B.place_forget()
            self.button_slide2_left_C.place_forget()
            self.button_slide2_left_cancel.place_forget()
            self.button_slide2_left_confirm.place_forget()
            self.label_slide2_right_img.place_forget()
            self.frame_slide2_left.grid_forget()
            self.frame_slide2_right.grid_forget()

            # 3번 띄우기
            self.frame_slide3_left.grid(row=0, column=0)
            self.frame_slide3_right.grid(row=0, column=1)
            self.label_slide3_left_title.place(x=10, y=10)
            self.label_slide3_left_name.place(x=0, y=70)
            self.label_slide3_left_index.place(x=60, y=100)
            self.button_slide3_left_left.place(x=0, y=250)
            self.button_slide3_left_right.place(x=100, y=250)
            self.button_slide3_left_edit.place(x=40, y=200)
            self.button_slide3_left_delete.place(x=90, y=200)
            self.label_slide3_right_img.grid()


class Profile:
    def __init__(self, name="", imagePath="", id=0):
        self._name = name
        self._imagePath = imagePath
        self._id = id

    def set_name(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def set_imagePath(self, imagePath):
        self._imagePath = imagePath

    def get_imagePath(self):
        return self._imagePath

    def set_id(self, id):
        self._id = id

    def get_id(self):
        return self._id


if __name__ == '__main__':

    init = Initializer()
    view = View(init)

    rf = RecognizeFace(init, view)

    rf.computeVision()
    view.window.mainloop()
