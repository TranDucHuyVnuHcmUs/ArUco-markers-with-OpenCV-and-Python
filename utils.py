import cv2


# define names of each possible ArUco tag OpenCV supports
ARUCO_DICT = {
	"DICT_4X4_50": cv2.aruco.DICT_4X4_50,
	"DICT_4X4_100": cv2.aruco.DICT_4X4_100,
	"DICT_4X4_250": cv2.aruco.DICT_4X4_250,
	"DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
	"DICT_5X5_50": cv2.aruco.DICT_5X5_50,
	"DICT_5X5_100": cv2.aruco.DICT_5X5_100,
	"DICT_5X5_250": cv2.aruco.DICT_5X5_250,
	"DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
	"DICT_6X6_50": cv2.aruco.DICT_6X6_50,
	"DICT_6X6_100": cv2.aruco.DICT_6X6_100,
	"DICT_6X6_250": cv2.aruco.DICT_6X6_250,
	"DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
	"DICT_7X7_50": cv2.aruco.DICT_7X7_50,
	"DICT_7X7_100": cv2.aruco.DICT_7X7_100,
	"DICT_7X7_250": cv2.aruco.DICT_7X7_250,
	"DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
	"DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
#	"APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
#	"APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
#	"APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
#	"APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
}

def draw_bounding_box(frame, corners, id):
	(topLeft, topRight, bottomRight, bottomLeft) = corners

	# convert each of the (x, y)-coordinate pairs to integers
	topRight = (int(topRight[0]), int(topRight[1]))
	bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
	bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
	topLeft = (int(topLeft[0]), int(topLeft[1]))

	# draw the bounding box of the ArUCo detection
	cv2.line(frame, topLeft, topRight, (0, 255, 0), 2)
	cv2.line(frame, topRight, bottomRight, (0, 255, 0), 2)
	cv2.line(frame, bottomRight, bottomLeft, (0, 255, 0), 2)
	cv2.line(frame, bottomLeft, topLeft, (0, 255, 0), 2)

	# compute and draw the center (x, y)-coordinates of the
	# ArUco marker
	cX = int((topLeft[0] + bottomRight[0]) / 2.0)
	cY = int((topLeft[1] + bottomRight[1]) / 2.0)
	cv2.circle(frame, (cX, cY), 4, (0, 0, 255), -1)

	# draw the ArUco marker ID on the frame
	cv2.putText(frame, str(id),
		(topLeft[0], topLeft[1] - 15),
		cv2.FONT_HERSHEY_SIMPLEX,
		0.5, (0, 255, 0), 2)
	
	return frame



def get_center(corners):
	(topLeft, topRight, bottomRight, bottomLeft) = corners

	# convert each of the (x, y)-coordinate pairs to integers
	topRight = (int(topRight[0]), int(topRight[1]))
	bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
	bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
	topLeft = (int(topLeft[0]), int(topLeft[1]))

	cX = int((topLeft[0] + bottomRight[0]) / 2.0)
	cY = int((topLeft[1] + bottomRight[1]) / 2.0)

	return cX, cY

