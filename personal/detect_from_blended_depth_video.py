import cv2
import argparse
import sys

import pykinect_azure as pykinect
from pykinect_azure import K4A_CALIBRATION_TYPE_COLOR, K4A_CALIBRATION_TYPE_DEPTH, k4a_float2_t

import utils

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--type", type=str,
	default="ARUCO_ORIGINAL",
	help="type of ArUCo tag to detect")
ap.add_argument("-c", "--camera",
	default=0,
	help="Camera index")
args = vars(ap.parse_args())

# verify that the supplied ArUCo tag exists and is supported by
# OpenCV
if utils.ARUCO_DICT.get(args["dict"], None) is None:
	print("[INFO] ArUCo tag of '{}' is not supported".format(
		args["dict"]))
	sys.exit(0)

# load the ArUCo dictionary and grab the ArUCo parameters
print("[INFO] detecting '{}' tags...".format(args["dict"]))
arucoDict = cv2.aruco.getPredefinedDictionary(utils.ARUCO_DICT[args["dict"]])
arucoParams = cv2.aruco.DetectorParameters()
arucoDetector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)



import pykinect_azure as pykinect

# Initialize the library, if the library is not found, add the library path as argument
pykinect.initialize_libraries()

# Modify camera configuration
device_config = pykinect.default_configuration
device_config.color_format = pykinect.K4A_IMAGE_FORMAT_COLOR_BGRA32
device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_720P
device_config.depth_mode = pykinect.K4A_DEPTH_MODE_WFOV_2X2BINNED
# print(device_config)

# Start device
device = pykinect.start_device(config=device_config)

cv2.namedWindow('Transformed Color Depth Image',cv2.WINDOW_NORMAL)
while True:
    
    # Get capture
    capture = device.update()

    # Get the color image from the capture
    ret_color, color_image = capture.get_color_image()

    # Get the colored depth
    ret_depth, transformed_colored_depth_image = capture.get_transformed_colored_depth_image()

    if not ret_color or not ret_depth:
        continue

    print(transformed_colored_depth_image.shape)

    # Combine both images
    combined_image = cv2.addWeighted(color_image[:,:,:3], 0.7, transformed_colored_depth_image, 0.3, 0)
    annotated_image = combined_image
	
    (corners, ids, rejected) = arucoDetector.detectMarkers(color_image)
	
    if len(corners) > 0:
        ids = ids.flatten()
        for (mCor, mId) in zip(corners, ids):
            m_cor = mCor.reshape((4,2))
            annotated_image = utils.draw_bounding_box(annotated_image, m_cor, mId)
		
    # Overlay body segmentation on depth image
    cv2.imshow('Transformed Color Depth Image With Aruco Markers Annotation',annotated_image)
    
    # Press q key to stop
    if cv2.waitKey(1) == ord('q'): 
        break