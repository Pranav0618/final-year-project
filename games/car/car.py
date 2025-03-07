# import os
# import logging
# import cv2
# import cvzone
# import numpy as np
# import random
# import pygame  # Importing pygame for audio
# from cvzone.HandTrackingModule import HandDetector
#
# # Suppress TensorFlow and absl logs to keep the console clean
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
# logging.getLogger('tensorflow').setLevel(logging.FATAL)
# logging.getLogger('absl').setLevel(logging.FATAL)
#
# # Initialize pygame for audio playback
# pygame.mixer.init()
#
# # Load sound files
# engine_start_sound = pygame.mixer.Sound("Resources/engine_start.wav")
# car_running_sound = pygame.mixer.Sound("Resources/car_running.wav")
# crash_sound = pygame.mixer.Sound("Resources/crash_sound.wav")
#
# # Initialize the webcam
# cap = cv2.VideoCapture(0)
# cap.set(3, 1280)  # Width
# cap.set(4, 720)   # Height
#
# # Load images
# imgCar = cv2.imread("Resources/car.png", cv2.IMREAD_UNCHANGED)                  # Player's car
# imgPickupTruck = cv2.imread("Resources/pickup_truck.png", cv2.IMREAD_UNCHANGED)  # Obstacle image
# imgSemiTrailer = cv2.imread("Resources/semi_trailer.png", cv2.IMREAD_UNCHANGED)  # Obstacle image
# imgTaxi = cv2.imread("Resources/taxi.png", cv2.IMREAD_UNCHANGED)                # Obstacle image
# imgVan = cv2.imread("Resources/van.png", cv2.IMREAD_UNCHANGED)                  # Obstacle image
# crash_img = cv2.imread("Resources/crash.png", cv2.IMREAD_UNCHANGED)            # Crash image
#
# # Verify all images are loaded
# required_images = {
#     "car.png": imgCar,
#     "pickup_truck.png": imgPickupTruck,
#     "semi_trailer.png": imgSemiTrailer,
#     "taxi.png": imgTaxi,
#     "van.png": imgVan,
#     "crash.png": crash_img
# }
#
# for filename, img in required_images.items():
#     if img is None:
#         print(f"Error: {filename} not found in the Resources folder.")
#         exit()
#
# # Hand Detector
# detector = HandDetector(detectionCon=0.8, maxHands=2)
#
# # Game Variables
# player_x = 213  # Center position of the player's car, adjusted for new lane positions
# player_y = 550  # Y position of the car (near the bottom)
# obstacles = []   # List to hold obstacles
# lane_width = 142  # Width allocated for each lane (total 3 lanes on the road)
# speed = 10         # Speed of the obstacles
# gameOver = False
# score = 0
#
# # Define lanes (x-coordinates for center of each lane's driving space, between lane markers)
# lanes = [71, 213, 355]  # Center points for left, center, and right lanes
#
# # Define new road and markers dimensions
# road_top = 0        # Top y-coordinate of the road
# road_bottom = 800   # Bottom y-coordinate of the road
# road_left = 0      # Left x-coordinate of the road (moved to the left)
# road_right = 426   # Right x-coordinate of the road (occupies 1/3 of the screen)
# marker_width = 10
# marker_height = 50
#
# # Adjust hand detection areas (right two-thirds of the screen for control)
# hand_track_left = 426    # Hand control area starts after the road
# hand_track_right = 1280  # Full screen width for hand control (rest of the screen)
#
# # Hand detection boundaries for left, center, right regions
# hand_left_bound = hand_track_left + (hand_track_right - hand_track_left) // 3
# hand_right_bound = hand_left_bound + (hand_track_right - hand_track_left) // 3
#
# # Initialize lane marker movement
# lane_marker_move_y = 0
#
# # Play the engine start sound and wait for it to finish
# engine_start_sound.play()
# pygame.time.delay(2000)  # Delay to let the sound play for 2 seconds before starting the car sound
# car_running_sound.play(-1)  # Loop the car running sound indefinitely
#
# while True:
#     success, img = cap.read()
#     if not success:
#         print("Failed to grab frame")
#         break
#
#     img = cv2.flip(img, 1)  # Mirror the image
#     imgRaw = img.copy()
#
#     # Draw the road boundaries
#     cv2.rectangle(img, (road_left, road_top), (road_right, road_bottom), (100, 100, 100), -1)  # Gray road
#     cv2.rectangle(img, (road_left - 5, road_top), (road_left + marker_width - 5, road_bottom), (255, 232, 0), -1)  # Left yellow boundary
#     cv2.rectangle(img, (road_right - marker_width + 5, road_top), (road_right + 5, road_bottom), (255, 232, 0), -1)  # Right yellow boundary
#
#     # Draw the two lane markers (one between each pair of lanes)
#     lane_marker_move_y += speed * 2
#     if lane_marker_move_y >= marker_height * 2:
#         lane_marker_move_y = 0
#     for y in range(-marker_height * 2, road_bottom, marker_height * 2):
#         # First lane marker (between left and center lanes)
#         cv2.rectangle(img, (road_left + lane_width, y + lane_marker_move_y),
#                       (road_left + lane_width + marker_width, y + lane_marker_move_y + marker_height),
#                       (255, 255, 255), -1)
#         # Second lane marker (between center and right lanes)
#         cv2.rectangle(img, (road_left + 2 * lane_width, y + lane_marker_move_y),
#                       (road_left + 2 * lane_width + marker_width, y + lane_marker_move_y + marker_height),
#                       (255, 255, 255), -1)
#
#     # Find hands and their landmarks
#     hands, img = detector.findHands(img, flipType=False)  # with draw
#
#     # Check for hands and simulate steering based on new regions
#     if hands:
#         for hand in hands:
#             x, y, w, h = hand['bbox']
#             # Hand detection for left, center, right
#             if x < hand_left_bound:  # Left side detection
#                 player_x = lanes[0]  # Move to left lane
#             elif hand_left_bound <= x <= hand_right_bound:  # Center side detection
#                 player_x = lanes[1]  # Move to center lane
#             else:  # Right side detection
#                 player_x = lanes[2]  # Move to right lane
#
#     # Move the obstacles
#     if not gameOver:
#         # Randomly generate obstacles
#         if len(obstacles) < 2:
#             lane = random.choice(lanes)
#             obstacle_type = random.choice([imgPickupTruck, imgSemiTrailer, imgTaxi, imgVan])
#             obstacles.append([obstacle_type, lane, road_top - 100])  # [image, lane, y position]
#
#         # Update obstacles
#         for obstacle in obstacles[:]:
#             obstacle_image, obstacle_lane, obstacle_y = obstacle
#
#             # Move the obstacle down
#             obstacle_y += speed
#             obstacle[2] = obstacle_y
#
#             # Define the bounding boxes for collision
#             car_width = imgCar.shape[1]
#             car_height = imgCar.shape[0]
#             obstacle_width = obstacle_image.shape[1]
#             obstacle_height = obstacle_image.shape[0]
#
#             # Calculate the bounding boxes
#             car_box = [player_x - car_width // 2, player_y - car_height // 2, car_width, car_height]
#             obstacle_box = [obstacle_lane - obstacle_width // 2, obstacle_y - obstacle_height // 2, obstacle_width, obstacle_height]
#
#             # Check for collision using rectangle overlap
#             if (car_box[0] < obstacle_box[0] + obstacle_box[2] and
#                     car_box[0] + car_box[2] > obstacle_box[0] and
#                     car_box[1] < obstacle_box[1] + obstacle_box[3] and
#                     car_box[1] + car_box[3] > obstacle_box[1]):
#                 crash_sound.play()  # Play crash sound
#                 car_running_sound.stop()  # Stop car running sound
#                 gameOver = True
#
#             # If the obstacle goes off-screen, remove it and increment score
#             if obstacle_y > road_bottom:
#                 obstacles.remove(obstacle)
#                 score += 1
#                 # Increase speed every 5 points
#                 if score % 5 == 0:
#                     speed += 1
#
#             else:
#                 # Draw the obstacle, centered between the lane markers
#                 img = cvzone.overlayPNG(img, obstacle_image, (obstacle_lane - obstacle_image.shape[1] // 2, obstacle_y - obstacle_image.shape[0] // 2))
#
#     # Draw the player's car, centered between the lane markers
#     img = cvzone.overlayPNG(img, imgCar, (player_x - imgCar.shape[1] // 2, player_y - imgCar.shape[0] // 2))
#
#     # Game Over display
#     if gameOver:
#         img = cvzone.overlayPNG(img, crash_img, (player_x - crash_img.shape[1] // 2, player_y - crash_img.shape[0] // 2))
#         cv2.putText(img, "Game Over", (road_left + (road_right - road_left) // 2 - 100, road_top + 250),
#                     cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 255), 5)
#         cv2.putText(img, "Press R to Restart or Q to Quit", (road_left + (road_right - road_left) // 2 - 300, road_top + 400),
#                     cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
#
#         # Handle restart or quit options
#         key = cv2.waitKey(1) & 0xFF
#         if key == ord('r'):  # Restart
#             gameOver = False
#             obstacles.clear()
#             player_x = 213  # Reset player's position
#             speed = 5  # Reset speed
#             score = 0  # Reset score
#             lane_marker_move_y = 0  # Reset lane marker position
#             engine_start_sound.play()  # Play engine start sound again
#             pygame.time.delay(2000)  # Delay to let the sound play for 2 seconds before starting the car sound
#             car_running_sound.play(-1)  # Loop the car running sound again
#         elif key == ord('q'):  # Quit
#             break
#     else:
#         # Display score
#         cv2.putText(img, f'Score: {score}', (10, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
#
#     # Show the final frame
#     cv2.imshow("Car Game", img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# # Stop the car running sound when the game is over
# car_running_sound.stop()
#
# # Release the video capture and close windows
# cap.release()
# cv2.destroyAllWindows()

import os
import logging
import cv2
import cvzone
import numpy as np
import random
import pygame  # Importing pygame for audio
from cvzone.HandTrackingModule import HandDetector

# Suppress TensorFlow and absl logs to keep the console clean
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logging.getLogger('tensorflow').setLevel(logging.FATAL)
logging.getLogger('absl').setLevel(logging.FATAL)

# Initialize pygame for audio playback
pygame.mixer.init()

# Load sound files
engine_start_sound = pygame.mixer.Sound(os.path.join("games", "car", "Resources", "engine_start.wav"))
car_running_sound = pygame.mixer.Sound(os.path.join("games", "car", "Resources", "car_running.wav"))
crash_sound = pygame.mixer.Sound(os.path.join("games", "car", "Resources", "crash_sound.wav"))
# Initialize the webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Width
cap.set(4, 720)   # Height

# Load images
imgCar = cv2.imread(os.path.join("games", "car", "Resources", "car.png"), cv2.IMREAD_UNCHANGED)                  # Player's car
imgPickupTruck = cv2.imread(os.path.join("games", "car", "Resources", "pickup_truck.png"), cv2.IMREAD_UNCHANGED)  # Obstacle image
imgSemiTrailer = cv2.imread(os.path.join("games", "car", "Resources", "semi_trailer.png"), cv2.IMREAD_UNCHANGED)  # Obstacle image
imgTaxi = cv2.imread(os.path.join("games", "car", "Resources", "taxi.png"), cv2.IMREAD_UNCHANGED)                # Obstacle image
imgVan = cv2.imread(os.path.join("games", "car", "Resources", "van.png"), cv2.IMREAD_UNCHANGED)                  # Obstacle image
crash_img = cv2.imread(os.path.join("games", "car", "Resources", "crash.png"), cv2.IMREAD_UNCHANGED)            # Crash image

# Verify all images are loaded
required_images = {
    "car.png": imgCar,
    "pickup_truck.png": imgPickupTruck,
    "semi_trailer.png": imgSemiTrailer,
    "taxi.png": imgTaxi,
    "van.png": imgVan,
    "crash.png": crash_img
}

for filename, img in required_images.items():
    if img is None:
        print(f"Error: {filename} not found in the Resources folder.")
        exit()

# Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=2)

# Game Variables
player_x = 213  # Center position of the player's car, adjusted for new lane positions
player_y = 550  # Y position of the car (near the bottom)
obstacles = []   # List to hold obstacles
lane_width = 142  # Width allocated for each lane (total 3 lanes on the road)
speed = 5         # Speed of the obstacles
gameOver = False
score = 0

# Define lanes (x-coordinates for center of each lane's driving space, between lane markers)
lanes = [71, 213, 355]  # Center points for left, center, and right lanes

# Define new road and markers dimensions
road_top = 0        # Top y-coordinate of the road
road_bottom = 800   # Bottom y-coordinate of the road
road_left = 0      # Left x-coordinate of the road (moved to the left)
road_right = 426   # Right x-coordinate of the road (occupies 1/3 of the screen)
marker_width = 10
marker_height = 50

# Adjust hand detection areas (right two-thirds of the screen for control)
hand_track_left = 426    # Hand control area starts after the road
hand_track_right = 1280  # Full screen width for hand control (rest of the screen)

# Hand detection boundaries for left, center, right regions
hand_left_bound = hand_track_left + (hand_track_right - hand_track_left) // 3
hand_right_bound = hand_left_bound + (hand_track_right - hand_track_left) // 3

# Initialize lane marker movement
lane_marker_move_y = 0

def play_start_sounds():
    # Play the engine start sound and wait for it to finish
    engine_start_sound.play()
    pygame.time.delay(-1)  # Delay to let the sound play for 2 seconds before starting the car sound
    car_running_sound.play(-1)  # Loop the car running sound indefinitely

# Play the start sounds when the game begins
play_start_sounds()

while True:
    success, img = cap.read()
    if not success:
        print("Failed to grab frame")
        break

    img = cv2.flip(img, 1)  # Mirror the image
    imgRaw = img.copy()

    # Draw the road boundaries
    cv2.rectangle(img, (road_left, road_top), (road_right, road_bottom), (100, 100, 100), -1)  # Gray road
    cv2.rectangle(img, (road_left - 5, road_top), (road_left + marker_width - 5, road_bottom), (255, 232, 0), -1)  # Left yellow boundary
    cv2.rectangle(img, (road_right - marker_width + 5, road_top), (road_right + 5, road_bottom), (255, 232, 0), -1)  # Right yellow boundary

    # Draw the two lane markers (one between each pair of lanes)
    lane_marker_move_y += speed * 2
    if lane_marker_move_y >= marker_height * 2:
        lane_marker_move_y = 0
    for y in range(-marker_height * 2, road_bottom, marker_height * 2):
        # First lane marker (between left and center lanes)
        cv2.rectangle(img, (road_left + lane_width, y + lane_marker_move_y),
                      (road_left + lane_width + marker_width, y + lane_marker_move_y + marker_height),
                      (255, 255, 255), -1)
        # Second lane marker (between center and right lanes)
        cv2.rectangle(img, (road_left + 2 * lane_width, y + lane_marker_move_y),
                      (road_left + 2 * lane_width + marker_width, y + lane_marker_move_y + marker_height),
                      (255, 255, 255), -1)

    # Find hands and their landmarks
    hands, img = detector.findHands(img, flipType=False)  # with draw

    # Check for hands and simulate steering based on new regions
    if hands:
        for hand in hands:
            x, y, w, h = hand['bbox']
            # Hand detection for left, center, right
            if x < hand_left_bound:  # Left side detection
                player_x = lanes[0]  # Move to left lane
            elif hand_left_bound <= x <= hand_right_bound:  # Center side detection
                player_x = lanes[1]  # Move to center lane
            else:  # Right side detection
                player_x = lanes[2]  # Move to right lane

    # Move the obstacles
    if not gameOver:
        # Randomly generate obstacles
        if len(obstacles) < 2:
            lane = random.choice(lanes)
            obstacle_type = random.choice([imgPickupTruck, imgSemiTrailer, imgTaxi, imgVan])
            obstacles.append([obstacle_type, lane, road_top - 100])  # [image, lane, y position]

        # Update obstacles
        for obstacle in obstacles[:]:
            obstacle_image, obstacle_lane, obstacle_y = obstacle

            # Move the obstacle down
            obstacle_y += speed
            obstacle[2] = obstacle_y

            # If the obstacle goes off-screen, remove it and increment score
            if obstacle_y > road_bottom:
                obstacles.remove(obstacle)
                score += 1
                # Increase speed every 5 points
                if score % 5 == 0:
                    speed += 1

            else:
                # Draw the obstacle, centered between the lane markers
                img = cvzone.overlayPNG(img, obstacle_image, (obstacle_lane - obstacle_image.shape[1] // 2, obstacle_y - obstacle_image.shape[0] // 2))

    # Draw the player's car, centered between the lane markers
    img = cvzone.overlayPNG(img, imgCar, (player_x - imgCar.shape[1] // 2, player_y - imgCar.shape[0] // 2))

    # Show the final frame
    cv2.imshow("Car Game", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Stop the car running sound when the game is over
car_running_sound.stop()

# Release the video capture and close windows
cap.release()
cv2.destroyAllWindows()

