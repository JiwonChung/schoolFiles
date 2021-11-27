import tkinter as tk
from time import sleep
import threading


class GUI:
    def __init__(self):
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

        # 제목
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
            command=lambda: self.wait5sec("jiwon")
        )
        self.button_slide1_left_profile.place(x=0, y=100)

        # 스텍
        self.stack = [False, False, False]

        # img 레이블
        self.label_slide1_left_img = tk.Label(self.frame_slide1_right)
        self.label_slide1_left_img.grid()

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
        if not self.stack[0]:
            self.label_slide1_left_foundPerson1.config(text=name+"1")
            self.label_slide1_left_foundPerson1.place(x=0, y=150)
            threading.Timer(5, lambda: self.dropLabel(self.label_slide1_left_foundPerson1, 0)).start()
            self.stack[0] = True
        elif not self.stack[1]:
            self.label_slide1_left_foundPerson2.config(text=name+'2')
            self.label_slide1_left_foundPerson2.place(x=0, y=180)
            threading.Timer(5, lambda: self.dropLabel(self.label_slide1_left_foundPerson2, 1)).start()
            self.stack[1] = True
        elif not self.stack[2]:
            self.label_slide1_left_foundPerson3.config(text=name+'3')
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



if __name__ == '__main__':
    gui = GUI()
    gui.window.mainloop()
