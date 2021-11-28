import cv2

capture = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier("C:\\Users\\jwchu\\Documents\\schoolFiles\\Project based "
                                     "learning\\playground\\test\\haarcascades"
                                     "\\haarcascade_frontalface_default.xml")

count = 1
while True:
    _, img = capture.read()
    grayScaledImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        grayScaledImage,
        scaleFactor=1.3,
        minNeighbors=5,
    )
    for (x, y, w, h) in faces:
        cv2.imwrite("C:\\Users\\jwchu\\Documents\\schoolFiles\\Project based "
                    "learning\\playground\\test\\dataset\\jiwon\\" + str(count) + '.jpg',
                    grayScaledImage[y: y + h, x: x + w])
        count += 1
    if count == 101:
        print("shoot done")
        break
