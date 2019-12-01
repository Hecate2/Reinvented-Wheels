#coding:utf-8

'''Play a 3-dimensional numpy array as a video on Windows'''
'''array[height, width, frames]'''
import cv2
import numpy as np
import threading,time
import win32gui,win32con #pip install pywin32

class ArrayVideo(threading.Thread):
    def __init__(self,array,fps=24,windowName='array video'):
        #array:被播放的视频
        #fps:帧率（控制方式为显示一帧后暂停1/fps秒，所以实际帧率不会特别精确）
        #windowName:播放窗口的名字
        shape=array.shape
        if(len(shape)==3):
            self.size=(shape[0],shape[1])#视频长宽尺寸
            self.frameCount=shape[2]#总帧数
        else:
            raise #后续应该加入自定义类型的异常
        self.array=array

        self.fps=fps
        self.windowName=windowName
        
##    def play(self):
##        print('About to play the array video')
##        interval=1/self.fps
##        for frameIndex in range(self.frameCount):#对于每一帧
##            #if win32gui.FindWindow(None,'cap video'):
##                frame=self.array[:,:,frameIndex]
##                cv2.imshow('cap video',frame)
##                cv2.waitKey(1)
##                time.sleep(interval)
##            #else:
##                #cv2.destroyAllWindows()
##                #break
##    def play_dilated(self,kernel=cv2.getStructuringElement(cv2.MORPH_RECT, (20, 20))):
##        print('About to play the dilated array video')
##        interval=1/self.fps
##        for frameIndex in range(self.frameCount):#对于每一帧
##            #if win32gui.FindWindow(None,'cap video'):
##                cv2.imshow('cap video',cv2.dilate(self.array[:,:,frameIndex],kernel))
##                cv2.waitKey(1)
##                time.sleep(interval)
##            #else:
##                #cv2.destroyAllWindows()
##                #break

    def play01(self):#原始数组为0-1取值
        print('About to play the 0-1 array video')
        interval=1/self.fps
        for frameIndex in range(self.frameCount):#对于每一帧
            cv2.imshow('cap video',self.array[:,:,frameIndex]*65535)
            cv2.waitKey(1)
            #cv2.waitKey(0) #此模式下按Ctrl+C可前进1帧
            time.sleep(interval)
            if win32gui.FindWindow(None,'cap video'):
                pass
            else:
                cv2.destroyAllWindows()
                break
        
if __name__=='__main__':
    img = np.ones([300,400,1],np.uint8) #创建一个只有一个信道的三维数组，初始为1
    #np.ones([height,width,1],np.uint8)
    #print(img)
    img = img * 127 #可以直接进行运算
    cv2.imshow("new image",img)
    cv2.waitKey(0)
