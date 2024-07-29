#!/usr/bin/env python

# import the necessary packages
import argparse
import imutils
import cv2
import sys
import utils

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image containing ArUCo tag")
ap.add_argument("-t", "--type", type=str,
	default="DICT_ARUCO_ORIGINAL",
	help="type of ArUCo tag to detect")
args = vars(ap.parse_args())


# load the input image from disk and resize it
print("[INFO] loading image...")
image = cv2.imread(args["image"])
image = imutils.resize(image, width=600)

# verify that the supplied ArUCo tag exists and is supported by
# OpenCV
if utils.ARUCO_DICT.get(args["dict"], None) is None:
	print("[INFO] ArUCo tag of '{}' is not supported".format(
		args["dict"]))
	sys.exit(0)

# load the ArUCo dictionary, grab the ArUCo parameters, and detect
# the markers
print("[INFO] detecting '{}' tags...".format(args["dict"]))
arucoDict = cv2.aruco.getPredefinedDictionary(utils.ARUCO_DICT[args["dict"]])
arucoParams = cv2.aruco.DetectorParameters()
arucoDetector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)
(corners, ids, rejected) = arucoDetector.detectMarkers(image)

# verify *at least* one ArUco marker was detected
if len(corners) > 0:
	# flatten the ArUco IDs list
	ids = ids.flatten()

	# loop over the detected ArUCo corners
	for (markerCorner, markerID) in zip(corners, ids):
		# extract the marker corners (which are always returned in
		# top-left, top-right, bottom-right, and bottom-left order)
		corners = markerCorner.reshape((4, 2))
		image = utils.draw_bounding_box(image, corners, markerID)
		print("[INFO] ArUco marker ID: {}".format(markerID))

	# show the output image
	cv2.imshow("Image", image)
	cv2.waitKey(0)