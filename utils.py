import cv2
import mediapipe as mp
import numpy as np
import psutil
from AppOpener import open, close
import speech_recognition as sr


class Finger_counter():

    def __init__(self, finger_coor: list = [(8, 6), (12, 10), (16, 14), (20, 18)],  thum_coor: tuple = (4, 3)) -> None:

        # setting the image processing instances
        self.hand = mp.solutions.hands
        self.hands = self.hand.Hands()
        self.hand_draw = mp.solutions.drawing_utils

        # setting the finger coordinates
        self.finger_coor = finger_coor
        self.thum_coor = thum_coor


    def count_fingers(self, image:np.ndarray, text_center_coor:tuple=(150, 150), font:int=cv2.FONT_HERSHEY_PLAIN,  font_scale:int=12, color:tuple=(0, 255, 255), thickness:int = 12)->tuple:
        # Finding out the Hands in the Frame tgrouh Image Tracking
        imaged = cv2.imread("image.jpg")
        cv2.imshow("Documentation", imaged)
        results = self.hands.process(image)

        # finding out the finger count throug the hand landmarks
        finger_count = 0
        if results.multi_hand_landmarks:

            # finding out the land mark coordiantes
            landmarks = self._extract_landmarks(image, results)

            # Drawing the hand marks
            self._draw_landmarks(image, results, landmarks)

            # counting the fingers according to the parsed image areas
            finger_count = self._check_finger_positions(landmarks, finger_count)

        # drawing the reults into tge image
        cv2.putText(image, str(finger_count), text_center_coor, font, font_scale, color, thickness)

        if (finger_count==1):
            if (not "telegram.exe" in (i.name() for i in psutil.process_iter())):
                open("telegram")
        elif (finger_count==2):
            open("chrome")
        elif (finger_count==3):
            if not "code.exe" in (i.name() for i in psutil.process_iter()):
                open("visual studio code")
        elif (finger_count==4):
            if not "brave.exe" in (i.name() for i in psutil.process_iter()):
                open("brave")
        elif (finger_count==5):
            if not "wordpad.exe" in (i.name() for i in psutil.process_iter()):
                open("wordpad")
        return image, finger_count

    def _draw_landmarks(self, image:np.ndarray, results:type, landmarks:list, radius:int = 5, color:tuple = (0, 255, 0))->np.ndarray:

        # drawing Hand Connections
        for hand_in_frame in results.multi_hand_landmarks:
            self.hand_draw.draw_landmarks(image, hand_in_frame, self.hand.HAND_CONNECTIONS)

        # drawing the hand land mark points as circles
        for point in landmarks:
            cv2.circle(image, point, radius, color, cv2.FILLED)

        return image
    def _check_finger_positions(self, landmarks:list, finger_count:int)->int:
        # increase the number according to parsed image areas for fingers
        for coordinate in self.finger_coor:
            if landmarks[coordinate[0]][1] < landmarks[coordinate[1]][1]:
                finger_count += 1

        # increase the number according to parsed image areas for fingers
        if landmarks[self.thum_coor[0]][0] > landmarks[self.thum_coor[1]][0]:
            finger_count += 1

        return finger_count

    def _extract_landmarks(self, image:np.ndarray, results:type, referanced_hand_index:int = 0)->list:
        # finding out the land mark coordiantes
        landmarks = list()
        for landmark in results.multi_hand_landmarks[referanced_hand_index].landmark:

            # calculating the corresponding coordinates. (cate x--> width -> col_size, cate y--> height --> row _size)
            height, width, = image.shape[:2]
            cx, cy = int(landmark.x*width), int(landmark.y*height)
            landmarks.append((cx, cy))

        return landmarks