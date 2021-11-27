# import tkinter as tk
#
# window = tk.Tk()
#
# window.rowconfigure(0, minsize=50)
# window.columnconfigure([0, 1, 2, 3], minsize=50)
#
# label1 = tk.Label(text="1", bg="black", fg="white")
# label2 = tk.Label(text="2", bg="black", fg="white")
# label3 = tk.Label(text="3", bg="black", fg="white")
# label4 = tk.Label(text="4", bg="black", fg="white")
#
# label1.grid(row=0, column=0)
# label2.grid(row=0, column=1, sticky="ew")
# label3.grid(row=0, column=2, sticky="nws")
# label4.grid(row=0, column=3, sticky="nsew")
#
# window.mainloop()

# from tkinter import *
# from tkinter import messagebox
#
# root = Tk()
#
#
# # 버튼 클릭 이벤트 핸들러
# def okClick():
#     name = txt.get()
#     messagebox.showinfo("이름", name)
#
#
# lbl = Label(root, text="이름")
# lbl.grid(row=0, column=0)
# txt = Entry(root)
# txt.grid(row=0, column=1)
#
# # 버튼 클릭 이벤트와 핸들러 정의
# btn = Button(root, text="OK", command=okClick)
#
# btn.grid(row=1, column=1)
#
# root.mainloop()

# from tkinter import *
#
# root = Tk()
#
#
# def click(event):
#     print("클릭위치", event.x, event.y)
#
#
# frame = Frame(root, width=300, height=300)
#
# # 왼쪽 마우스 버튼 바인딩
# frame.bind("<Button-1>", click)
#
# frame.pack()
# root.mainloop()

import tkinter as tk

win = tk.Tk()


def changeText():
    a.config(text="changed text!")


a = tk.Label(win, text="hello world")
a.pack()
tk.Button(win, text="Change Label Text", command=lambda: changeText()).pack()

win.mainloop()

# from tkinter import *
#
# def motion(event):
#   print("Mouse position: (%s %s)" % (event.x, event.y))
#   return
#
# master = Tk()
# whatever_you_do = "Whatever you do will be insignificant, but it is very important that you doit.\n(Mahatma Gandhi)"
# msg = Message(master, text = whatever_you_do)
# msg.config(bg='lightgreen', font=('times', 24, 'italic'))
# msg.bind('<Motion>',motion)
# msg.pack()
# mainloop()