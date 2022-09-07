import cv2

left_camera = 0
right_camera = 1
fps = 30
frameSize = (1280, 720)
codec = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')

esc_key = ord('\x1b')

chessboardSize = (9, 6)
squareMM = 25

detection_confidence = 0.5

delta = 100
sleep_secs = 5

speed = "25000"
splash_power = "100"
baud_rate = 250000
r = 5.0
