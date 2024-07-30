import cv2 
import utils
import argparse
import sys
import numpy as np
import os
import json

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dict", type=str,
    default="DICT_4X4_50",
    help="Aruco dictionary")
ap.add_argument("-x", "--x", type=int,
    default=8)
ap.add_argument("-y", "--y", type=int,
    default=5)
ap.add_argument("-of", "--out_folder", type=str,
	default="charuco_board/",
	help="Output folder for output charuco boards.")
args = vars(ap.parse_args())

# verify that the supplied ArUCo tag exists and is supported by
# OpenCV
if utils.ARUCO_DICT.get(args["dict"], None) is None:
	print("[INFO] ArUCo tag of '{}' is not supported".format(
		args["dict"]))
	sys.exit(0)
	

# load the ArUCo dictionary and grab the ArUCo parameters
print("[INFO] generating '{}' charuco board...".format(args["dict"]))
arucoDict = cv2.aruco.getPredefinedDictionary(utils.ARUCO_DICT[args["dict"]])
arucoParams = cv2.aruco.DetectorParameters()

# define charuco board attributes
config = {
	"dictionary": args["dict"],
	"x": args["x"], 
	"y": args["y"],
	"square_length": 100,
	"marker_length": 60,          # for some reasons, I have to use this, if 0.2 then it cause error?
}
print(config)

board_size = (1280, 720)

board = cv2.aruco.CharucoBoard( (config["x"], config["y"]), config["square_length"], config["marker_length"], arucoDict)
board_image = np.zeros( [board_size[0], board_size[1], 1], dtype=np.uint8)
board_image = board.generateImage(board_size, board_image)

output_folder_path = args["out_folder"]
if (not os.path.exists(output_folder_path)):
	os.mkdir(output_folder_path)

output_name = args["dict"]
output_name += "_x=" + (str)(config["x"])
output_name += "_y=" + (str)(config["y"])  
output_name += "_s=" + (str)(config["square_length"]) 
output_name += "_m=" + (str)(config["marker_length"])

output_file_path = os.path.join(output_folder_path, output_name + ".jpg")
	
cv2.imwrite(
		output_file_path,
		board_image
    )

with open(os.path.join(output_folder_path, output_name + ".json"), "w") as f:
	f.write(json.dumps( 
		config, 
		indent = 4
	))

cv2.imshow("Charuco board", board_image)
cv2.waitKey(0)

