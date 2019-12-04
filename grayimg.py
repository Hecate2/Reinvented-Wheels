import cv2

dir='IMG_0044.jpg'
image=cv2.imread(dir)
imgray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) #彩色转灰度
cv2.imshow("imgray", imgray)
#cv2.waitKey(0)
cv2.imwrite('gray_'+dir,imgray)
