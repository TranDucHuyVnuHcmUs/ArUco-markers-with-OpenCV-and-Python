#!/usr/bin/env python

# import the necessary packages
import numpy as np
import argparse
import cv2
import sys
import os
import utils

from tqdm import tqdm

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-of", "--out_folder", type=str,
	default="aruco/",
	help="path to the parent folder containing output file(s)")
ap.add_argument("-mi", "--max_id", type=int,
	default=50,
	help="Maximum ID of ArUCo tag to generate")
ap.add_argument("-d", "--dict", type=str,
	default="DICT_ARUCO_ORIGINAL",
	help="type of ArUCo tag to generate")
ap.add_argument("-s", "--size", type=int,
	default=1024,
	help="Side length of each marker")
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

output_folder_path = os.path.join( args["out_folder"], args["dict"] )
if not os.path.exists(output_folder_path):
	os.mkdir(output_folder_path)

def generate_marker_with_id_and_dict(dict, id: int, size: int, output_folder_path: str):
	tag = np.zeros((512, 512, 1), dtype="uint8")
	cv2.aruco.generateImageMarker(arucoDict, id, size, tag, 1)
	cv2.imwrite(os.path.join(output_folder_path, args["dict"] + "_" + (str)(id) + ".png" ), tag)

max_id = args["max_id"]
size = args["size"]
for id in tqdm(range(max_id + 1)):
	generate_marker_with_id_and_dict(arucoDict, id, size, output_folder_path)
