import mediapipe as mp
import numpy as np
import time
import pyautogui
import cv2

x, y = 0, 0
cx, cy = 0, 0

startx, starty, endx, endy = 0, 0, 0, 0
k = 0

def onMouse(event, x, y, flags, param):
    global startx, starty, endx, endy, k

    if event == cv2.EVENT_LBUTTONDOWN and k == 0:
        startx, starty = x * 2, y * 2
        # startx, starty = 0, 0
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

# startx = 2
# starty = 2

# resolution = pyautogui.size()
# endx = resolution.width
# endy = resolution.height

hnds = mp.solutions.hands
hnds_mesh = hnds.Hands(static_image_mode=False, min_detection_confidence=0.8, min_tracking_confidence=0.8)
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
# rad = 30

while True:
    _, frm = cap.read()
    frm = cv2.flip(frm, 1)

    rgb = cv2.cvtColor(frm, cv2.COLOR_BGR2RGB)

    op = hnds_mesh.process(rgb)

    if op.multi_hand_landmarks:
        for i in op.multi_hand_landmarks:
            point4 = i.landmark[4]  # Thumb tip
            point5 = i.landmark[5]
            point7 = i.landmark[7]
            point8 = i.landmark[8]
            point9 = i.landmark[9]
            point11 = i.landmark[11]
            point12 = i.landmark[12]

            draw.draw_landmarks(frm, i, hnds.HAND_CONNECTIONS)

            vertical_diff = int(abs(point8.y * 480 - point5.y * 480))
            horizontal_diff = int(abs(point8.x * 640 - point4.x * 640))

            if vertical_diff > 35:
                # click
                if int(abs(point12.x * 640 - point4.x * 640)) < 10 and int(abs(point12.y * 480 - point4.y * 480)) < 10:
                    if done:
                        pyautogui.click()
                    #done = False
                    pset = False
                    ctime = 0
                    ptime = 0
                    rad = 30
                    continue

                # index above middle
                elif point12.y > point7.y:
                    print("12:", point12.y)
                    print("7:", point7.y)
                    # One-finger gesture
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

                # up gesture
                elif int(abs(point9.y * 480 - point12.y * 480)) > 35:
                    pyautogui.scroll(1)
                
                # else:
                #     cv2.circle(frm, (int(point8.x * 640), int(point8.y * 480)), rad, (0, 255, 255), 3)
                #     if rad > 4:
                #         rad -= 1


            # up gesture
            elif int(abs(point9.y * 480 - point12.y * 480)) < 35:
                # Down gesture
                pyautogui.scroll(-1)

            else:
                # Not one or up or down
                # if done:
                #     pyautogui.click()
                # done = False
                pset = False
                ctime = 0
                ptime = 0
                rad = 30

    cv2.imshow("window", frm)

    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        cap.release()
        break