import utils.movement_planner as movement_planner
import mediapipe as mp
import time

from utils.calibrated_utils import *
from utils.functions import *
from config import *

mp_facedetector = mp.solutions.face_detection
mp_draw = mp.solutions.drawing_utils

cap_left = cv2.VideoCapture(left_camera, cv2.CAP_DSHOW)
cap_right = cv2.VideoCapture(right_camera, cv2.CAP_DSHOW)

setrez(cap_right)
setrez(cap_left)

splashing = False


def mouse_event(event, a, b, o, p):
    if event == cv2.EVENT_RBUTTONDOWN:
        movement_planner.toggle_splash(True)
    elif event == cv2.EVENT_RBUTTONUP:
        movement_planner.toggle_splash(False)


cv2.imshow("right cam", cap_right.read()[1])
cv2.imshow("left cam", cap_left.read()[1])

cv2.setMouseCallback("right cam", mouse_event)
cv2.setMouseCallback("left cam", mouse_event)


with mp_facedetector.FaceDetection(min_detection_confidence=detection_confidence, model_selection=1) as face_detection:
    while cap_right.isOpened() and cap_left.isOpened():

        succes_right, frame_right = cap_right.read()
        succes_left, frame_left = cap_left.read()

        frame_right, frame_left = undistort(frame_right, frame_left)

        if not succes_right or not succes_left:
            break

        else:
            frame_right_p = cv2.cvtColor(frame_right, cv2.COLOR_BGR2RGB)
            frame_left_p = cv2.cvtColor(frame_left, cv2.COLOR_BGR2RGB)

            results_right = face_detection.process(frame_right_p)
            results_left = face_detection.process(frame_left_p)

            center_right = 0
            center_left = 0

            if results_right.detections:
                for id, detection in enumerate(results_right.detections):
                    mp_draw.draw_detection(frame_right, detection)

                    bBox = detection.location_data.relative_bounding_box

                    h, w, c = frame_right.shape

                    boundBox = int(bBox.xmin * w), int(bBox.ymin * h), int(bBox.width * w), int(bBox.height * h)

                    center_point_right = (boundBox[0] + boundBox[2] / 2, boundBox[1] + boundBox[3] / 2)

                    cv2.putText(frame_right, f'{int(detection.score[0]*100)}%', (boundBox[0], boundBox[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 2)

            if results_left.detections:
                for id, detection in enumerate(results_left.detections):
                    mp_draw.draw_detection(frame_left, detection)

                    bBox = detection.location_data.relative_bounding_box

                    h, w, c = frame_left.shape

                    boundBox = int(bBox.xmin * w), int(bBox.ymin * h), int(bBox.width * w), int(bBox.height * h)

                    center_point_left = (boundBox[0] + boundBox[2] / 2, boundBox[1] + boundBox[3] / 2)

                    cv2.putText(frame_left, f'{int(detection.score[0]*100)}%', (boundBox[0], boundBox[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 2)

            if not results_right.detections:
                cv2.putText(frame_right, "TRACKING LOST", (75, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            if not results_left.detections:
                cv2.putText(frame_left, "TRACKING LOST", (75, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            if results_right.detections and results_left.detections:
                position = get_position(center_point_left, center_point_right)
                posstr = stringifypos(position)

                movement_planner.try_move(convert_pos(position))

                cv2.putText(frame_right, "Position: " + posstr, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,255,0),3)
                cv2.putText(frame_left, "Position: " + posstr, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,255,0),3)

            # Show the frames
            cv2.imshow("right cam", frame_right) 
            cv2.imshow("left cam", frame_left)

            key = cv2.waitKey(1)

            if key == esc_key:
                movement_planner.toggle_splash(False)
                time.sleep(0.5)
                break


cap_right.release()
cap_left.release()

cv2.destroyAllWindows()
