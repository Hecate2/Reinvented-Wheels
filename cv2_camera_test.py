import numpy as np
import cv2

print('Ctrl+C结束测试')

camera_number = 0 
cap = cv2.VideoCapture( camera_number + cv2.CAP_DSHOW)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BAYER_BG2GRAY)
    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
        
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
