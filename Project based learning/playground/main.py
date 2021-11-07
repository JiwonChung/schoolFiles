import cv2
import dlib
import numpy as numpy

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(
    'models/shape_predictor_68_face_landmarks.dat')
facerec = dlib.face_recognition_model_v1('models/dlib_face_recognition_resnet_model_v1.dat')

cap = cv2.VideoCapture(0)

while True:
    # 동영상 파일에서 프레임 단위로 읽기
    ret, img = cap.read()
    if not ret:
        break

    faces = detector(img)
    if len(faces) != 0:
        for face in faces:
            # dlib 객체 생성
            dlib_shape = predictor(img, face)
            # dlib 객체를 np로 변환
            shape_2d = numpy.array([[p.x, p.y] for p in dlib_shape.parts()])
            print(len(shape_2d))
            # visualize
            img = cv2.rectangle(img, pt1=(face.left(), face.top()), pt2=(face.right(), face.bottom()),
                                color=(255, 255, 255), thickness=2, lineType=cv2.LINE_AA)

    # 출력
    cv2.imshow('img', img)
    # 1msec  만큼 기다리기
    cv2.waitKey(1)
