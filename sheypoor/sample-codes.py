## https://cagriuysal.github.io/Simple-Captcha-Breaker/

pattern = 1
# use median blur for pattern1 and gaussian blur for patter2 images as pre-processing

srcImage = cv2.medianBlur(image_sharp, 3) if pattern == 1 else cv2.GaussianBlur(image_sharp, (3,3), 0)


#obtained through experiment 
pattern1_thresh = 250
pattern2_thresh = 155
thresh = pattern1_thresh if pattern == 1 else pattern2_thresh
ret, threshImage = cv2.threshold(srcImage, thresh, 255, cv2.THRESH_BINARY_INV)

min_connected_len = 15
# get connected components
numLabel, labelImage, stats, centroids = cv2.connectedComponentsWithStats(threshImage, 8, cv2.CV_32S)
# holds if component will be included to foreground
foreComps = [i for i in range(1, numLabel) if stats[i, cv2.CC_STAT_AREA] >= min_connected_len]
# Get binary image after erasing some connected components those areas under the threshold
binaryImage = np.zeros_like(srcImage)
labelImage = np.array(labelImage)
for k in [np.where(labelImage == i) for i in foreComps]:
	binaryImage[k] = 255

minCol = 20; # seen that all digits start at 30th column 
			# no need for additional computation
# find the boundaries where digits present in the image 
array = np.array([stats[i, cv2.CC_STAT_LEFT] + stats[i, cv2.CC_STAT_WIDTH]  for i in foreComps])
maxCol = max(array[np.where(array < 130)]) # observed that digits right boundary never exceeds 125th pixel 
									# thus this one prevents false boundaries
# find boundaries in y axis
minRow = min([stats[i, cv2.CC_STAT_TOP] for i in foreComps])
maxRow = max([stats[i, cv2.CC_STAT_TOP] + stats[i, cv2.CC_STAT_HEIGHT] for i in foreComps])
subImage = threshImage[minRow:maxRow, minCol:maxCol]


# Sub image divided to half in order to segment digit's more precisely
subImage1 = subImage[:, :int(subImage.shape[1]/2)]
subImage2 = subImage[:, int(subImage.shape[1]/2):]
colIncrement1 = subImage1.shape[1] / 2
colIncrement2 = subImage2.shape[1] / 2
# get segmented digits as list
digitList1 = []
digitList2 = []
col1 = 0
col2 = 0
for i in range(2):
	digitList1.append(subImage1[:, int(col1):int(col1+colIncrement1)])
	digitList2.append(subImage2[:, int(col2):int(col2+colIncrement2)])
	col1 += colIncrement1
	col2 += colIncrement2
digitList1.append(subImage1[:, int(col1):])
digitList2.append(subImage2[:, int(col2):])
digitList = digitList1 + digitList2

plt.imshow(image_gray); plt.show()
plt.imshow(subImage); plt.show()
for x in digitList:
	plt.imshow(x)
	plt.show()