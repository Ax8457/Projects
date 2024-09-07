import cv2
import mediapipe as mp
import math


class HandDetector:
    def __init__(self, image_mode=False, max_num_hands=1,complexity=1, min_detection_confidence=0.5,min_tracking_confidence=0.5,vPositions=[]):
        self.aMode = image_mode
        self.aNumHand = max_num_hands
        self.aComplexity = complexity
        self.aMinDetectionConfidence = min_detection_confidence
        self.aMinTrackingConfidence = min_tracking_confidence
        self.aPositions = vPositions
        self.aFingersId = [4, 8, 12, 16, 20]

        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(self.aMode, self.aNumHand,self.aComplexity, self.aMinDetectionConfidence, self.aMinTrackingConfidence)

    def drawRectangleAndLabel(self,image, width, height, epsilon, state1, state2, label):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        self.results = self.hands.process(image_rgb)

        if self.results.multi_hand_landmarks:
            for self.hand_landmarks in self.results.multi_hand_landmarks:
                x_max = 0
                y_max = 0
                x_min = width
                y_min = height
                for landmark in self.hand_landmarks.landmark:
                    x, y = int(landmark.x * width), int(landmark.y * height)
                    if x > x_max:
                        x_max = x
                    if x < x_min:
                        x_min = x
                    if y > y_max:
                        y_max = y
                    if y < y_min:
                        y_min = y

            if state1:
                cv2.rectangle(image, (x_min - epsilon, y_min - epsilon), (x_max + epsilon, y_max + epsilon),(0, 0, 255), 2)

            if state2:
                    cv2.putText(image, '{:s}'.format(label), (x_min - epsilon, y_min - epsilon - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.2, (0, 0, 255), 2)

        return image

    def drawHandOnWhiteBoard(self, image):
        if self.results.multi_hand_landmarks:
            for self.hand_landmarks in self.results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(image, self.hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

        return image

    def whichHand(self,image):
        if self.results.multi_hand_landmarks:
            for self.hand_landmarks in self.results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(image, self.hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                for hand in self.results.multi_handedness:
                    handType = hand.classification[0].label
                    if handType == "Right":
                        return 1
                    else:
                        return 0

    def countUpFingers(self,whichHand):
        self.fingers = []

        if whichHand == 0:
            if self.fingerPositionList[self.aFingersId[0]][1] > self.fingerPositionList[self.aFingersId[0] - 1][1]:
                self.fingers.append(1)
            else:
                self.fingers.append(0)
        else:
            if self.fingerPositionList[self.aFingersId[0]][1] > self.fingerPositionList[self.aFingersId[0] - 1][1]:
                self.fingers.append(0)
            else:
                self.fingers.append(1)

        for id in range(1, 5):
            if self.fingerPositionList[self.aFingersId[id]][2] < self.fingerPositionList[self.aFingersId[id] - 2][2]:
                self.fingers.append(1)
            else:
                self.fingers.append(0)

        return self.fingers

    def mouseTracer(self,image,wScreen,state3):
        self.fingerPositionList = []
        if self.results.multi_hand_landmarks:
            for id, lm in enumerate(self.hand_landmarks.landmark):
                height, width, channel = image.shape
                x3, y3 = int(wScreen - lm.x * width), int(lm.y * height)
                x, y = int(lm.x * width), int(lm.y * height)
                self.fingerPositionList.append([id, x, y])
                if id == 8:
                    if len(self.aPositions) >= 20:
                        self.aPositions.pop(0)
                    self.aPositions.append([x3, y3])
                    for i in range(len(self.aPositions)-1):
                        x1,y1 = self.aPositions[i]
                        x2,y2 = self.aPositions[i+1]
                        if self.fingers[0] == 0 and self.fingers[1] == 1 and self.fingers[2] == 0 and self.fingers[3] == 0 and self.fingers[4] == 0:
                            if state3:
                                cv2.line(image, (wScreen - x1, y1), (wScreen - x2, y2), (0, 0, 255), 2)

        return self.fingerPositionList

    def distanceBetweenTwoFingers(self, finger1, finger2):
        x1, y1 = self.fingerPositionList[finger1][1:]
        x2, y2 = self.fingerPositionList[finger2][1:]
        length = math.hypot(x2 - x1, y2 - y1)

        return length