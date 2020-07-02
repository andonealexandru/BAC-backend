import os
import cv2
import numpy as np
from src.WordSegmentation import wordSegmentation, prepareImg
import DataLoader
import Model

images_for_model = []

def getImages():
	"""reads images from data/ and outputs the word-segmentation to out/"""

	# read input images from 'in' directory
	imgFiles = os.listdir('data/')
	for (i,f) in enumerate(imgFiles):
		print('Segmenting words of sample %s'%f)
		
		# read image, prepare it by resizing it to fixed height and converting it to grayscale
		img = prepareImg(cv2.imread('data/%s'%f), 270)
		
		# execute segmentation with given parameters
		# -kernelSize: size of filter kernel (odd integer)
		# -sigma: standard deviation of Gaussian function used for filter kernel
		# -theta: approximated width/height ratio of words, filter function is distorted by this factor
		# - minArea: ignore word candidates smaller than specified area
		res = wordSegmentation(img, kernelSize=25, sigma=11, theta=7, minArea=100)
		
		# write output to 'out/inputFileName' directory
		if not os.path.exists('out/%s'%f):
			os.mkdir('out/%s'%f)
		
		# iterate over all segmented words
		print('Segmented into %d words'%len(res))
		for (j, w) in enumerate(res):
			(wordBox, wordImg) = w
			(x, y, w, h) = wordBox
			cv2.imwrite('out/%s/%d.png'%(f, j), wordImg) # save word
			cv2.rectangle(img,(x,y),(x+w,y+h),0,1) # draw bounding box in summary image

			img_resized = DataLoader.resize_img('out/%s/%d.png'%(f, j), '', False)

			pxmin = np.min(img_resized)
			pxmax = np.max(img_resized)
			imgContrast = (img_resized - pxmin) / (pxmax - pxmin) * 255

			# increase line width
			kernel = np.ones((3, 3), np.uint8)
			imgMorph = cv2.erode(imgContrast, kernel, iterations=1)

			# write
			cv2.imwrite('out/%s/%d.png'%(f, j), imgMorph)

			images_for_model.append(imgMorph)

		# output summary image with bounding boxes around words
		cv2.imwrite('out/%s/summary.png'%f, img)
		return images_for_model

#if __name__ == '__main__':
#	main()