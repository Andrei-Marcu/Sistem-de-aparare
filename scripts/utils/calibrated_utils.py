import cv2

cv_file = cv2.FileStorage()
cv_file.open('utils/stereo_map.xml', cv2.FileStorage_READ)

stereoMapL_x = cv_file.getNode('stereoMapL_x').mat()
stereoMapL_y = cv_file.getNode('stereoMapL_y').mat()
stereoMapR_x = cv_file.getNode('stereoMapR_x').mat()
stereoMapR_y = cv_file.getNode('stereoMapR_y').mat()

projMapL = cv_file.getNode('projMapL').mat()
projMapR = cv_file.getNode('projMapR').mat()


def undistort(frameR, frameL):
    undistortedL= cv2.remap(frameL, stereoMapL_x, stereoMapL_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
    undistortedR= cv2.remap(frameR, stereoMapR_x, stereoMapR_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
    return undistortedR, undistortedL


def get_position(left_point, right_point):
    hgCoords = cv2.triangulatePoints(projMapL, projMapR, left_point, right_point)
    return hgCoords[:3] / hgCoords[3]