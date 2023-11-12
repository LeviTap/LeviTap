
from flask import Flask, jsonify, request
import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import time

app = Flask(__name__)

x, y = 0, 0
cx, cy = 0, 0
startx, starty, endx, endy = 0, 0, 0, 0
k = 0

def onMouse(event, x, y, flags, param):
    global startx, starty, endx, endy, k

    if event == cv2.EVENT_LBUTTONDOWN and k == 0:
        startx, starty = x * 2, y * 2
        k += 1
        print(f"set l - x{startx}, y{starty}")

    elif event == cv2.EVENT_RBUTTONDOWN and k == 1:
        endx, endy = x * 2, y * 2
        k += 1
        print(f"set r - x{endx}, y{endy}")

cv2.namedWindow("setpoint")
cv2.setMouseCallback("setpoint", onMouse)

print('going to take screenshot! /n show only the player window clearly!')
time.sleep(2)
im = pyautogui.screenshot().convert('RGB')
im = np.array(im)
im = im[:, :, ::-1]

im = cv2.resize(im, (960, 540))

while True:
    cv2.imshow("setpoint", im)
    if cv2.waitKey(1) == 27 or k == 2:
        cv2.destroyAllWindows()
        break

@app.route('/run-python-code', methods=['POST'])
def run_python_code():
    global done, pset, x, y, cx, cy

    _, frm = cap.read()
    frm = cv2.flip(frm, 1)

    rgb = cv2.cvtColor(frm, cv2.COLOR_BGR2RGB)

    op = hnds_mesh.process(rgb)

    if op.multi_hand_landmarks:
        for i in op.multi_hand_landmarks:
            point8 = i.landmark[8]
            point5 = i.landmark[5]
            point4 = i.landmark[4]
            point12 = i.landmark[12]

            vertical_diff = int(abs(point8.y * 480 - point5.y * 480))
            horizontal_diff = int(abs(point8.x * 640 - point4.x * 640))

            if vertical_diff > 35:
                if int(abs(point12.x * 640 - point4.x * 640)) < 30 and int(abs(point12.y * 480 - point4.y * 480)) < 30:
                    if done:
                        pyautogui.click()
                    pset = False
                    ctime = 0
                    ptime = 0
                    rad = 30
                    continue

                if not pset:
                    pset = True
                    ptime = time.time()

                ctime = time.time()

                if (ctime - ptime) > 1:
                    if not done:
                        x = int(point8.x * 640)
                        y = int(point8.y * 480)
                        done = True

                    cx = int(point8.x * 640)
                    cy = int(point8.y * 640)

                    if cx < x:
                        cx = x
                    elif cx > (x + seekwidth):
                        cx = x + seekwidth

                    if cy < y:
                        cy = y
                    elif cy > (y + seekwidth):
                        cy = y + seekwidth

                    cv2.line(frm, (x, y), (x + seekwidth, y), (255, 0, 255), 6)
                    cv2.circle(frm, (cx, y), 9, (0, 255, 0), -1)

                    pyautogui.moveTo((cx - x) * mulx + startx, (cy - y) * muly + starty)

    cv2.imshow("window", frm)

    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        cap.release()
        return jsonify({'message': 'Server Stopped'})
    else:
        return jsonify({'message': 'Python code executed successfully'})

if __name__ == '__main__':
    hnds_mesh = mp.solutions.hands.Hands(static_image_mode=False, min_detection_confidence=0.8, min_tracking_confidence=0.8)
    draw = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0)
    done = False
    pset = False
    linewidth = (endx - startx)
    heightwidth = (endy - starty)
    seekwidth = 200
    muly = int(heightwidth/seekwidth)
    mulx = int(linewidth / seekwidth)
    ptime, ctime = 0, 0

    app.run(port=5000)
