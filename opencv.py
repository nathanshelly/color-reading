import numpy as np
import cv2
from colorthief import ColorThief

cap = cv2.VideoCapture(0)

counter = 0

while(True):
	# Capture frame-by-frame
	ret, frame = cap.read()

	# Our operations on the frame come here
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# Display the resulting frame
	cv2.imshow('frame',gray)

	if counter % 10 == 0:
		cv2.imwrite("frame.jpg", frame)
		color_thief = ColorThief('frame.jpg')
		# get the dominant color
		dominant_color = color_thief.get_color(quality=1)
		print(dominant_color)
		# build a color palette
		# palette = color_thief.get_palette(color_count=6)

	counter += 1
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()