import numpy as np
import cv2, os, datetime
from colorthief import ColorThief
from multiprocessing import Process
from threading import Thread, Condition

# get music
import sys
sys.path.append('../color-coded-music')
from color_music import *

def read_image():
	cap = cv2.VideoCapture(0)

	pp = Process(target=process_image)
	first_time = True

	while(True):
		# Capture frame-by-frame
		ret, frame = cap.read()
		
		# Display the resulting frame
		cv2.imshow('frame',frame)

		half = cv2.resize(frame, (0,0), fx=0.5, fy=0.5) 

		if first_time:
			print("Dimensions: ", frame.shape)
			print("Half dimensions: ", half.shape)
			first_time = False
			pp.start()

		if pp and not pp.is_alive():
			# write frame to disk
			print("\n\nAnalyzing\n\n")
			cv2.imwrite("frame.jpg", half)
			print(datetime.datetime.now())
			pp = Process(target=process_image)
			pp.start()
			
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	# When everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()

def process_image():
	info('process_child')

	# do stuff
	color_thief = ColorThief('frame.jpg')
	# get the dominant color
	dominant_color = color_thief.get_color(quality=1)
	print("Dominant: ", dominant_color)
	addOrClear(dominant_color)
	# build a color palette
	# palette = color_thief.get_palette(color_count=6)
	# print("Palette: ", palette)

def info(title):
	print(title)
	print('module name:', __name__)
	print('parent process:', os.getppid())
	print('process id:', os.getpid())

if __name__ == '__main__':
	info('main line')
	drum_thread = Thread(name='consumer1', target=drum, args=())
	drum_thread.start()
	addOrClear((0, 0, 0))
	sleep(.2)
	addOrClear((0, 0, 0))
	sleep(.4)
	addOrClear((0, 0, 0))
	read_image()