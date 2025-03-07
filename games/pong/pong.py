# import cvzone
# import cv2
# from cvzone.HandTrackingModule import HandDetector
# import numpy as np
#
# cap = cv2.VideoCapture(0)
# cap.set(3, 1280)
# cap.set(4, 720)
#
# # Importing all images
# imgBackground = cv2.imread("Resources/Background.png")
# imgGameOver = cv2.imread("Resources/gameOver.png")
# imgBall = cv2.imread("Resources/Ball.png", cv2.IMREAD_UNCHANGED)
# imgBat1 = cv2.imread("Resources/bat1.png", cv2.IMREAD_UNCHANGED)
# imgBat2 = cv2.imread("Resources/bat2.png", cv2.IMREAD_UNCHANGED)
#
# # Check if images are loaded correctly
# if imgBackground is None or imgGameOver is None or imgBall is None or imgBat1 is None or imgBat2 is None:
#     print("Error: One or more images not found in 'Resources' folder.")
#     exit()
#
# # Resize background to match camera resolution
# imgBackground = cv2.resize(imgBackground, (1280, 720))
#
# # Hand Detector
# detector = HandDetector(detectionCon=0.8, maxHands=2)
#
# # Variables
# ballPos = [100, 100]
# speedX = 20
# speedY = 20
# gameOver = False
# score = [0, 0]
#
# while True:
#     success, img = cap.read()
#     if not success:
#         print("Error: Camera not detected!")
#         break
#     img = cv2.flip(img, 1)
#     imgRaw = img.copy()
#
#     # Find the hand and its landmarks
#     hands, img = detector.findHands(img, flipType=False)
#
#     # Overlaying the background image
#     img = cv2.addWeighted(img, 0.2, imgBackground, 0.8, 0)
#
#     # Check for hands
#     if hands:
#         for hand in hands:
#             x, y, w, h = hand['bbox']
#             h1, w1, _ = imgBat1.shape
#             y1 = y - h1 // 2
#             y1 = np.clip(y1, 20, 415)
#
#             if hand['type'] == "Left":
#                 img = cvzone.overlayPNG(img, imgBat1, (59, y1))
#                 if 59 < ballPos[0] < 59 + w1 and y1 < ballPos[1] < y1 + h1:
#                     speedX = abs(speedX)
#                     ballPos[0] += 30
#                     score[0] += 1
#
#             if hand['type'] == "Right":
#                 img = cvzone.overlayPNG(img, imgBat2, (1195, y1))
#                 if 1195 - 50 < ballPos[0] < 1195 and y1 < ballPos[1] < y1 + h1:
#                     speedX = -abs(speedX)
#                     ballPos[0] -= 30
#                     score[1] += 1
#
#     # Game Over Condition
#     if ballPos[0] < 40 or ballPos[0] > 1200:
#         gameOver = True
#
#     if gameOver:
#         img = imgGameOver.copy()
#         cv2.putText(img, str(score[1] + score[0]).zfill(2), (585, 360), cv2.FONT_HERSHEY_COMPLEX, 2.5, (200, 0, 200), 5)
#     else:
#         # Move the Ball
#         if ballPos[1] >= 500 or ballPos[1] <= 10:
#             speedY = -speedY
#
#         ballPos[0] += speedX
#         ballPos[1] += speedY
#
#         # Draw the ball
#         img = cvzone.overlayPNG(img, imgBall, ballPos)
#
#         cv2.putText(img, str(score[0]), (300, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)
#         cv2.putText(img, str(score[1]), (900, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)
#
#     img[580:700, 20:233] = cv2.resize(imgRaw, (213, 120))
#
#     cv2.imshow("Pong Game", img)
#     key = cv2.waitKey(1)
#     if key == ord('r'):
#         ballPos = [100, 100]
#         speedX = 20
#         speedY = 20
#         gameOver = False
#         score = [0, 0]
#         imgGameOver = cv2.imread("Resources/gameOver.png")
#     elif key == 27:  # Press ESC to exit
#         break
#
# cap.release()
# cv2.destroyAllWindows()

import cvzone
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import os

# Set the correct path like the Car game
RESOURCES_DIR = "games/pong/Resources"

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Importing all images
imgBackground = cv2.imread(os.path.join(RESOURCES_DIR, "Background.png"))
imgGameOver = cv2.imread(os.path.join(RESOURCES_DIR, "gameOver.png"))
imgBall = cv2.imread(os.path.join(RESOURCES_DIR, "Ball.png"), cv2.IMREAD_UNCHANGED)
imgBat1 = cv2.imread(os.path.join(RESOURCES_DIR, "bat1.png"), cv2.IMREAD_UNCHANGED)
imgBat2 = cv2.imread(os.path.join(RESOURCES_DIR, "bat2.png"), cv2.IMREAD_UNCHANGED)

# Check if images are loaded correctly
if any(img is None for img in [imgBackground, imgGameOver, imgBall, imgBat1, imgBat2]):
    print("Error: One or more images not found in 'Resources' folder.")
    exit()

# Resize background to match camera resolution
imgBackground = cv2.resize(imgBackground, (1280, 720))

# Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=2)

# Variables
ballPos = [100, 100]
speedX = 20
speedY = 20
gameOver = False
score = [0, 0]

while True:
    success, img = cap.read()
    if not success:
        print("Error: Camera not detected!")
        break
    img = cv2.flip(img, 1)
    imgRaw = img.copy()

    # Find the hand and its landmarks
    hands, img = detector.findHands(img, flipType=False)

    # Overlaying the background image
    img = cv2.addWeighted(img, 0.2, imgBackground, 0.8, 0)

    # Check for hands
    if hands:
        for hand in hands:
            x, y, w, h = hand['bbox']
            h1, w1, _ = imgBat1.shape
            y1 = y - h1 // 2
            y1 = np.clip(y1, 20, 415)

            if hand['type'] == "Left":
                img = cvzone.overlayPNG(img, imgBat1, (59, y1))
                if 59 < ballPos[0] < 59 + w1 and y1 < ballPos[1] < y1 + h1:
                    speedX = abs(speedX)
                    ballPos[0] += 30
                    score[0] += 1

            if hand['type'] == "Right":
                img = cvzone.overlayPNG(img, imgBat2, (1195, y1))
                if 1195 - 50 < ballPos[0] < 1195 and y1 < ballPos[1] < y1 + h1:
                    speedX = -abs(speedX)
                    ballPos[0] -= 30
                    score[1] += 1

    # Game Over Condition
    if ballPos[0] < 40 or ballPos[0] > 1200:
        gameOver = True

    if gameOver:
        img = imgGameOver.copy()
        cv2.putText(img, str(score[1] + score[0]).zfill(2), (585, 360), cv2.FONT_HERSHEY_COMPLEX, 2.5, (200, 0, 200), 5)
    else:
        # Move the Ball
        if ballPos[1] >= 500 or ballPos[1] <= 10:
            speedY = -speedY

        ballPos[0] += speedX
        ballPos[1] += speedY

        # Draw the ball
        img = cvzone.overlayPNG(img, imgBall, ballPos)

        cv2.putText(img, str(score[0]), (300, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)
        cv2.putText(img, str(score[1]), (900, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)

    img[580:700, 20:233] = cv2.resize(imgRaw, (213, 120))

    cv2.imshow("Pong Game", img)
    key = cv2.waitKey(1)
    if key == ord('r'):
        ballPos = [100, 100]
        speedX = 20
        speedY = 20
        gameOver = False
        score = [0, 0]
        imgGameOver = cv2.imread(os.path.join(RESOURCES_DIR, "gameOver.png"))
    elif key == 27:  # Press ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
