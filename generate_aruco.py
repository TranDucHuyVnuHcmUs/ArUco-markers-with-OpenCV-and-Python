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
ap.add_argument("-of", "--out_folder", type=str,
	default="aruco/",
	help="path to the parent folder containing output file(s)")
ap.add_argument("-i", "--id", type=int,
	default=0,
	help="ID of ArUCo tag to generate")
ap.add_argument("-d", "--dict", type=str,
	default="DICT_ARUCO_ORIGINAL",
	help="type of ArUCo tag to generate")
args = vars(ap.parse_args())


# verify that the supplied ArUCo tag exists and is supported by
# OpenCV
aruco_dict_type = utils.get_dict_from_string(args["dict"])
if aruco_dict_type is None:
	print("[INFO] ArUCo tag of '{}' is not supported".format(
		args["dict"]))
	sys.exit(0)

# load the ArUCo dictionary
arucoDict = cv2.aruco.getPredefinedDictionary(aruco_dict_type)

# allocate memory for the output ArUCo tag and then draw the ArUCo
# tag on the output image
print("[INFO] generating ArUCo tag type '{}' with ID '{}'".format(
	args["dict"], args["id"]))
tag = np.zeros((512, 512, 1), dtype="uint8")
cv2.aruco.generateImageMarker(arucoDict, args["id"], 512, tag, 1)

# write the generated ArUCo tag to disk and then display it to our
# screen

if not os.path.exists(args["out_folder"]):
	os.mkdir(args["out_folder"])
cv2.imwrite(os.path.join(args["out_folder"], args["dict"] + "_id" + (str)(args["id"]) + ".png" ), tag)
cv2.imshow("ArUCo Tag", tag)
cv2.waitKey(0)
