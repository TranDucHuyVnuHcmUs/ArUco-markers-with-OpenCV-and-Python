import cv2
import argparse
import sys
import json
import numpy as np
import os
import time

from tqdm import tqdm

import pykinect_azure as pykinect
from pykinect_azure import K4A_CALIBRATION_TYPE_COLOR, K4A_CALIBRATION_TYPE_DEPTH, k4a_float2_t

import utils

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-cf", "--config", type=str, required=True,
    help="JSON file containing information about the needed board")
ap.add_argument("-o", "--output", type=str,
    default="charuco_board/camera_params.pckl",
    help="The path of the resulting camera parameter file.")
ap.add_argument("-cam", "--camera", type=int,
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

charuco_board = cv2.aruco.CharucoBoard( (config["x"], config["y"]), config["square_length"], config["marker_length"], aruco_dict)
charuco_detector = cv2.aruco.CharucoDetector(charuco_board)
print("Charuco detector initialized!")


camera = cv2.VideoCapture(0)

all_image_points = []
all_object_points = []
image_size = None           # for now

frame_count = 0

for i in tqdm(range(5)):
    frame_count += 1
    ret, frame = camera.read()
    (charuco_corners, charuco_ids, marker_corners, marker_ids) = charuco_detector.detectBoard(frame)
	
    annotated_image = frame

    if ( (charuco_corners is not None) and (len(charuco_corners) > 0) ):
        annotated_image = cv2.aruco.drawDetectedCornersCharuco(annotated_image, charuco_corners, charuco_ids, (255, 0, 0))
        (obj_points, img_points) = charuco_board.matchImagePoints(charuco_corners, charuco_ids)
        
        if (obj_points is None or obj_points.sum() == 0) or (img_points is None or img_points.sum() == 0): continue 
        all_image_points.append(img_points)
        all_object_points.append(obj_points)
        image_size = (frame.shape[0], frame.shape[1])

        cv2.imshow("Camera calibration using ChAruco board", annotated_image)

        cv2.waitKey(0)
        
camera_matrix = np.zeros((3,3))
dist_coeffs = np.zeros(())
(retval, camera_matrix, dist_coeffs, rvecs, tvecs) = cv2.calibrateCamera(all_object_points, all_image_points, image_size, camera_matrix, dist_coeffs)


# output 

output_filepath = args["output"]

calib_results = {
    "camera_matrix": camera_matrix,
    "dist_coeffs": dist_coeffs,
    "rvecs": rvecs,
    "tvecs": tvecs
}
print(calib_results)

import pickle
pickler = pickle.Pickler(open(output_filepath, "wb"))
pickler.dump(calib_results)