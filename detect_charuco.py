import cv2
import argparse
import sys
import json
import pickle

import pykinect_azure as pykinect
from pykinect_azure import K4A_CALIBRATION_TYPE_COLOR, K4A_CALIBRATION_TYPE_DEPTH, k4a_float2_t

import utils

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-cf", "--config", type=str, required=True,
    help="JSON file containing information about the needed board")
ap.add_argument("-p", "--params", type=str, required=True,
    help="Calibration result with ChAruco board")
ap.add_argument("-cam", "--camera",
	default=0,
	help="Camera index")

args = vars(ap.parse_args())


# load the ArUCo dictionary and grab the ArUCo parameters
with open(args["config"], "r") as f:
    config = json.loads(f.read())
    print(config)
    
# verify that the supplied ArUCo tag exists and is supported by
# OpenCV
if utils.ARUCO_DICT.get(config["dictionary"], None) is None:
	print("[INFO] ArUCo tag of '{}' is not supported".format(
		args["dict"]))
	sys.exit(0)

print("[INFO] detecting '{}' tags...".format(config["dictionary"]))
aruco_dict = cv2.aruco.getPredefinedDictionary(utils.ARUCO_DICT[config["dictionary"]])

with open(args["params"], "rb") as f:
    unpickler= pickle.Unpickler(f)
    params = unpickler.load()
print(params)

camera_matrix = params["camera_matrix"]
dist_coeffs = params["dist_coeffs"]


charuco_board = cv2.aruco.CharucoBoard( (config["x"], config["y"]), config["square_length"], config["marker_length"], aruco_dict)

charuco_params = cv2.aruco.CharucoParameters()
charuco_params.tryRefineMarkers = False
charuco_params.cameraMatrix = camera_matrix
charuco_params.distCoeffs = dist_coeffs
charuco_detector = cv2.aruco.CharucoDetector(charuco_board,charuco_params  ,cv2.aruco.DetectorParameters())
print("Charuco detector initialized!")


camera = cv2.VideoCapture(0)

while True:
    ret, frame = camera.read()
    (charuco_corners, charuco_ids, marker_corners, marker_ids) = charuco_detector.detectBoard(frame)
	
    annotated_image = frame
    print("Charuco corners: ", charuco_corners)

    if ( (charuco_corners is not None) and (len(charuco_corners) > 0) ):
        annotated_image = cv2.aruco.drawDetectedCornersCharuco(annotated_image, charuco_corners, charuco_ids, (0, 255, 0))
        (obj_points, img_points) = charuco_board.matchImagePoints(charuco_corners, charuco_ids)

        if (camera_matrix.sum() != 0 and dist_coeffs.sum() != 0 and charuco_ids.shape[0] >= 6):
            retval, rvec, tvec = cv2.solvePnP(obj_points, img_points, camera_matrix, dist_coeffs)
            annotated_image = cv2.drawFrameAxes(annotated_image, camera_matrix, dist_coeffs, rvec, tvec, 100)
    # Overlay body segmentation on depth image
    cv2.imshow('Transformed Color Depth Image With ChAruco Board Annotation',annotated_image)
    
    # Press q key to stop
    if cv2.waitKey(1) == ord('q'): 
        break