import os
import cv2 
import numpy as np
from WordSegmentation import wordSegmentation, prepareImg
import DataLoader
import Model

images_for_model = []


def send_words_to_nn():
	list_word = getImages()
	NN = Model.NeuralNetwork(create=False)
	text = []
	print(len(list_word))
	for i in range(0,len(list_word)):
		#print(i)
		word = DataLoader.prepare_image('out/imageToSave.png/%d.png'%i)
		interpreted_text = NN.return_text(word)
		text.append(interpreted_text)
		#print(interpreted_text)
	return ' '.join(text)


def increase_contrast_and_apply_treshold():
	img = cv2.imread('data/imageToSave.png', 1)
	img = cv2.GaussianBlur(img, (5, 5), 0)

	# -----Converting image to LAB Color model-----------------------------------
	lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
		# -----Splitting the LAB image to different channels-------------------------
	l, a, b = cv2.split(lab)

	# -----Applying CLAHE to L-channel-------------------------------------------
	clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
	cl = clahe.apply(l)

	# -----Merge the CLAHE enhanced L-channel with the a and b channel-----------
	limg = cv2.merge((cl, a, b))

	# -----Converting image from LAB Color model to RGB model--------------------
	final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

	# read
	kernel = np.ones((3, 3))
	img = cv2.erode(final, kernel)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	# cv2.imwrite('erode.png', img)

	# ret, thresh1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
	# # cv2.imwrite('treshhold.png', thresh1)
	#
	# th2 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 61, 8)
	# cv2.imwrite('treshhold2.png', th2)

	th3 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 61, 14)
	# cv2.imwrite('treshold3.png', th3)
	return th3


def getImages():
	images_for_model.clear()
	"""reads images from data/ and outputs the word-segmentation to out/"""

	# read input images from 'in' directory
	imgFiles = os.listdir('data/')
	for (i,f) in enumerate(imgFiles):
		print('Segmenting words of sample %s'%f)
		
		# read image, prepare it by resizing it to fixed height and converting it to grayscale
		img = increase_contrast_and_apply_treshold()
		img = prepareImg(img, 270)
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
			# (x, y, w, h) = wordBox
			cv2.imwrite('out/%s/%d.png'%(f, j), wordImg) # save word
			# cv2.rectangle(img,(x,y),(x+w,y+h),0,1) # draw bounding box in summary image

			img_resized = DataLoader.extract_img(wordImg)

			# pxmin = np.min(img_resized)
			# pxmax = np.max(img_resized)
			# imgContrast = (img_resized - pxmin) / (pxmax - pxmin) * 255
			#
			# # increase line width
			# kernel = np.ones((3, 3), np.uint8)
			# imgMorph = cv2.erode(imgContrast, kernel, iterations=1)

			# write
			cv2.imwrite('out/%s/%d.png'%(f, j), img_resized)

			images_for_model.append(img_resized)

		# output summary image with bounding boxes around words
		cv2.imwrite('out/%s/summary.png'%f, img)
		print(len(images_for_model))
		return images_for_model

if __name__ == '__main__':
 	print(send_words_to_nn())