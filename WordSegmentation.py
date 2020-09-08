import math
import cv2
import numpy as np
from os import path


def wordSegmentation(img, kernelSize=25, sigma=11, theta=7, minArea=0):
	"""Scale space technique for word segmentation proposed by R. Manmatha: http://ciir.cs.umass.edu/pubfiles/mm-27.pdf
	
	Args:
		img: grayscale uint8 image of the text-line to be segmented.
		kernelSize: size of filter kernel, must be an odd integer.
		sigma: standard deviation of Gaussian function used for filter kernel.
		theta: approximated width/height ratio of words, filter function is distorted by this factor.
		minArea: ignore word candidates smaller than specified area.
		
	Returns:
		List of tuples. Each tuple contains the bounding box and the image of the segmented word.
	"""

	# apply filter kernel
	kernel = createKernel(kernelSize, sigma, theta)
	imgFiltered = cv2.filter2D(img, -1, kernel, borderType=cv2.BORDER_REPLICATE).astype(np.uint8)
	(_, imgThres) = cv2.threshold(imgFiltered, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	imgThres = 255 - imgThres
	if path.exists('out/in_ws.png'):
		cv2.imwrite('out/in_ws1.png', imgThres)
	else:
		cv2.imwrite('out/in_ws.png', imgThres)

	# find connected components. OpenCV: return type differs between OpenCV2 and 3
	if cv2.__version__.startswith('3.'):
		(_, components, _) = cv2.findContours(imgThres, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	else:
		(components, _) = cv2.findContours(imgThres, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

	# append components to result
	res = []
	for c in components:
		# skip small word candidates
		if cv2.contourArea(c) < minArea:
			continue
		# append bounding box and image of word to result list
		currBox = cv2.boundingRect(c) # returns (x, y, w, h)
		(x, y, w, h) = currBox
		# x-=5
		# y-=5
		# w+=10
		# h+=10
		currImg = img[y:y+h, x:x+w]
		res.append((currBox, currImg))

	# return list of words, sorted by x-coordinate
	# return sorted(res, key=lambda entry:entry[0][0])
	return sortare(sorted(res, key=lambda entry:entry[0][1]))

def get_y(word):
	return word[0][1]

def get_h(word):
	return word[0][3]

def get_x(word):
	return word[0][0]

def get_w(word):
	return word[0][2]


def sortare(words):
	n = len(words)
	for i in range(n):
		for j in range(i+1, n):
			if get_x(words[i]) > get_x(words[j]) and (get_y(words[i])-10 < get_y(words[j]) < get_y(words[i])+10 or get_y(words[i]) + get_h(words[i]) -10 < get_y(words[j])+get_h(words[j]) < get_y(words[i])+ get_h(words[i])+10):
				aux = words[i]
				words[i] = words[j]
				words[j] = aux
	return words


def sortRois(rois) :
	for (i, img) in enumerate(rois):
		cv2.imwrite('out_sort/%d.png'%i, img[1])
	new_rois = []
	for current_roi in rois: # (x, y, w, h)
		x = current_roi[0][0]
		y = current_roi[0][1]
		h = current_roi[0][3]
		line = []
		for next_roi in rois:
			if next_roi[0][1] >= y-10 and next_roi[0][1] <= y + h+10 :
				if (next_roi[0][0] < x) :
					line.append(next_roi)
		line.reverse()
		for word in line:
			if word not in new_rois:
				new_rois.append(word)
		if current_roi not in new_rois:
			new_rois.append(current_roi)
	return new_rois

def prepareImg(img, height):
	"""convert given image to grayscale image (if needed) and resize to desired height"""
	assert img.ndim in (2, 3)
	if img.ndim == 3:
		img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	h = img.shape[0]
	factor = height / h
	return cv2.resize(img, dsize=None, fx=factor, fy=factor)


def createKernel(kernelSize, sigma, theta):
	"""create anisotropic filter kernel according to given parameters"""
	assert kernelSize % 2 # must be odd size
	halfSize = kernelSize // 2
	
	kernel = np.zeros([kernelSize, kernelSize])
	sigmaX = sigma
	sigmaY = sigma * theta
	
	for i in range(kernelSize):
		for j in range(kernelSize):
			x = i - halfSize
			y = j - halfSize
			
			expTerm = np.exp(-x**2 / (2 * sigmaX) - y**2 / (2 * sigmaY))
			xTerm = (x**2 - sigmaX**2) / (2 * math.pi * sigmaX**5 * sigmaY)
			yTerm = (y**2 - sigmaY**2) / (2 * math.pi * sigmaY**5 * sigmaX)
			
			kernel[i, j] = (xTerm + yTerm) * expTerm

	kernel = kernel / np.sum(kernel)
	return kernel
