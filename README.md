# ArUco-markers-with-OpenCV-and-Python

## What is ArUco
- Similar to AprilTags, **ArUco markers are 2D binary patterns** that computer 
vision algorithms can easily detect.

## ArUco Usability
1. Camera calibration
1. Object size estimation
1. Measuring the distance between camera and object
1. 3D position
1. Object orientation
1. Robotics and autonomous navigation
1. etc.

## ArUco over AprilTag
1. ArUco markers are **built into the OpenCV library** via the **cv2.aruco** 
submodule (i.e., we don’t need additional Python packages).
1. The OpenCV library itself can **generate ArUco markers** via the 
**cv2.aruco.drawMarker** function.
1. There are **online ArUco generators** that we can use if we don’t feel like 
coding (unlike AprilTags where no such generators are easily found).
1. There are **ROS (Robot Operating System) implementations** of ArUco markers.
1. And from an implementation perspective, ArUco marker detections tend to be 
**more accurate**, even when using the default parameters.

## Usage

### Generate Aruco markers

> python opencv_generate_aruco.py --id 24 --dict DICT_5X5_100 --output tags/DICT_5X5_100_id24.png

### Guess 

> python guess_aruco_type.py --image images/example_01.png

### Detect the markers from the images or video stream

> python detect_aruco_image.py --image images/example_01.png --dict DICT_5X5_100

> python detect_aruco_image.py --image images/example_02.png --dict DICT_ARUCO_ORIGINAL

> python detect_aruco_video.py

### Generate ChAruco boards

> python generate_charuco.py --dict DICT_4X4_50 -x 8 -y 5 --out_folder charuco_board/

### Calibrate camera using ChAruco board

Currently I use Pickle to pack up the calibration results.

> python charuco_calibration.py --config charuco_board\DICT_4X4_50_x=7_y=5_s=100_m=60.json

### Detect Charuco board, with pose estimation

You must run calibration scripts first to obtain camera parameters, then include it and the board configuration into this scripts, for example:

> python charuco_detection.py --config charuco_board\DICT_4X4_50_x=7_y=5_s=100_m=60.json --params charuco_board\calib_params.p

## References
1. https://www.pyimagesearch.com/2020/12/14/generating-aruco-markers-with-opencv-and-python/
1. https://www.pyimagesearch.com/2020/12/21/detecting-aruco-markers-with-opencv-and-python/
1. https://www.pyimagesearch.com/2020/12/28/determining-aruco-marker-type-with-opencv-and-python/
