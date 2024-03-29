import cv2
import numpy as np
#from matplotlib import pyplot as plt
import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

def detect(img):
	# converting image into grayscale image
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	# setting threshold of gray image
	_, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

	# using a findContours() function
	_, contours, _ = cv2.findContours(
		threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	i = 0

	# list for storing names of shapes
	for contour in contours:

		# here we are ignoring first counter because
		# findcontour function detects whole image as shape
		if i == 0:
			i = 1
			continue

		# cv2.approxPloyDP() function to approximate the shape
		approx = cv2.approxPolyDP(
			contour, 0.01 * cv2.arcLength(contour, True), True)
		
		# using drawContours() function
		cv2.drawContours(img, [contour], 0, (0, 0, 255), 5)

		# finding center point of shape
		M = cv2.moments(contour)
		if M['m00'] != 0.0:
			x = int(M['m10']/M['m00'])
			y = int(M['m01']/M['m00'])

		# putting shape name at center of each shape
		if len(approx) == 3:
			cv2.putText(img, 'Triangle', (x, y),
						cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
			return 'Triangle', img

		elif len(approx) == 4:
			cv2.putText(img, 'Quadrilateral', (x, y),
						cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
			return 'Quadrilateral', img

		elif len(approx) == 5:
			cv2.putText(img, 'Pentagon', (x, y),
						cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
			return 'Pentagon', img
		elif len(approx) == 6:
			cv2.putText(img, 'Hexagon', (x, y),
						cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
			return 'Hexagon', img
		else:
			cv2.putText(img, 'circle', (x, y),
						cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
			return 'circle', img
# displaying the image after drawing contours
def main():
	# reading image
	img = cv2.imread('circle.png')
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind((HOST, PORT))
		s.listen()
		conn, addr = s.accept()
		with conn:
			print('Connected by', addr)
			name,img=detect(img)
			name=bytes(name,'utf-8')
			conn.sendall(name)

	cv2.imshow('shapes', img)

	cv2.waitKey(0)
	cv2.destroyAllWindows()

main()
