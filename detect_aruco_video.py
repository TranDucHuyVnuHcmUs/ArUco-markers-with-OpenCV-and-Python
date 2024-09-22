#!/usr/bin/env python

# import the necessary packages
from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import sys
import utils

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dict", type=str,
	default="DICT_ARUCO_ORIGINAL",
	help="type of ArUCo tag to detect")
ap.add_argument("-c", "--camera",
	default=0,
	help="Camera index")
args = vars(ap.parse_args())


# verify that the supplied ArUCo tag exists and is supported by
# OpenCV
aruco_dict_type = utils.get_dict_from_string(args["dict"])

if aruco_dict_type is None:
	print("[INFO] ArUCo tag of '{}' is not supported".format(args["dict"]))
	sys.exit(0)

# load the ArUCo dictionary and grab the ArUCo parameters
print("[INFO] detecting '{}' tags...".format(args["dict"]))
arucoDict = cv2.aruco.getPredefinedDictionary(aruco_dict_type)
arucoParams = cv2.aruco.DetectorParameters()
arucoDetector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)

# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(src=args["camera"]).start()
time.sleep(2.0)


# loop over the frames from the video stream
while True:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 600 pixels
	frame = vs.read()
	# frame = imutils.resize(frame, width=1000)

	# detect ArUco markers in the input frame
	(corners, ids, rejected) = arucoDetector.detectMarkers(frame)

	# verify *at least* one ArUco marker was detected
	if len(corners) > 0:
		ids = ids.flatten()
		# loop over the detected ArUCo corners
		for (markerCorner, markerID) in zip(corners, ids):
			corners = markerCorner.reshape((4, 2))
			frame = utils.draw_bounding_box(frame, corners, markerID)

	# show the output frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
