import cv2 
import utils
import argparse
import sys
import numpy as np
import os

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dict", type=str,
    default="DICT_4X4_50",
    help="Aruco dictionary")
ap.add_argument("-x", "--x", type=int,
    default=8)
ap.add_argument("-y", "--y", type=int,
    default=5)
ap.add_argument("-o", "--output", type=str,
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
marker_count = (args["x"], args["y"])
print(marker_count)
square_length = 100
marker_length = 60           # for some reasons, I have to use this, if 0.2 then it cause error?

board = cv2.aruco.CharucoBoard( marker_count, square_length, marker_length, arucoDict)
# board_size = ( (int)(marker_count[0] * square_length) + 1, (int)(marker_count[1] * square_length) + 1 )
# board_image = np.zeros((board_size[0], board_size[1], 1), dtype="uint8")
board_size = (1280, 720)

board_image = np.zeros( [board_size[0], board_size[1], 1], dtype=np.uint8)

print(board_image.shape)

# generate chAruco
# board.generateImage(board_size, board_image)
board_image = board.generateImage(board_size, board_image)

output_folder_path = args["output"]
if (not os.path.exists(output_folder_path)):
	os.mkdir(output_folder_path)
	
cv2.imwrite(
	os.path.join(args["output"], 
        args["dict"] 
        + "_x" + (str)(marker_count[0]) + "y" + (str)(marker_count[1]) 
        + "_s" + (str)(square_length) + "_m" + (str)(marker_length))
		+ ".jpg",
		board_image
    )
cv2.imshow("Charuco board", board_image)
cv2.waitKey(0)

