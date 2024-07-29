#!/usr/bin/env python

# import the necessary packages
import numpy as np
import argparse
import cv2
import sys
import os
import utils

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", required=True,
	help="path to the parent folder containing output file(s)")
ap.add_argument("-i", "--id", type=int, required=True,
	help="ID of ArUCo tag to generate")
ap.add_argument("-d", "--dict", type=str,
	default="DICT_ARUCO_ORIGINAL",
	help="type of ArUCo tag to generate")
args = vars(ap.parse_args())


# verify that the supplied ArUCo tag exists and is supported by
# OpenCV
if utils.ARUCO_DICT.get(args["dict"], None) is None:
	print("[INFO] ArUCo tag of '{}' is not supported".format(
		args["dict"]))
	sys.exit(0)

# load the ArUCo dictionary
arucoDict = cv2.aruco.getPredefinedDictionary(utils.ARUCO_DICT[args["dict"]])

# allocate memory for the output ArUCo tag and then draw the ArUCo
# tag on the output image
print("[INFO] generating ArUCo tag type '{}' with ID '{}'".format(
	args["dict"], args["id"]))
tag = np.zeros((300, 300, 1), dtype="uint8")
cv2.aruco.generateImageMarker(arucoDict, args["id"], 300, tag, 1)

# write the generated ArUCo tag to disk and then display it to our
# screen

if not os.path.exists(args["output"]):
	os.mkdir(args["output"])
cv2.imwrite(os.path.join(args["output"], args["dict"] + "_id" + (str)(args["id"]) + ".png" ), tag)
cv2.imshow("ArUCo Tag", tag)
cv2.waitKey(0)
