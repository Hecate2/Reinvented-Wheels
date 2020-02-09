#coding:utf-8
'''
写一个程序，统计一下 C 盘下面有多少个 .dll 文件；如果你是 Mac 或者 Linux 系统，统计一下 /usr 目录下有多少个 .so 文件.
注意不能使用 walkFileTree, os.walk 这类直接遍历所有目录的方法，而是要你自己实现它
'''
from __future__ import print_function
import os,platform

if platform.system() == "Windows":
    import ctypes, sys
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

import logging
#logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.basicConfig(level = logging.INFO,format = '[%(levelname)s] - %(message)s')
logger = logging.getLogger(__name__)

def scanner(file_dir='.',find_endswith='.dll',result=[]):
    if file_dir.endswith('/'):
        file_dir=file_dir[:-1]  #去除目录最后的'/'
    
    for filename in os.listdir(file_dir):  #当前路径下所有子文件和子目录
        #print(filename) 

        full_filename=file_dir+'/'+filename
        if os.path.isdir(full_filename):
            #如果是目录，先进入这个目录，扫描内部文件
            try:
                result=scanner(file_dir=full_filename)
                #print(len(result),full_filename)
            except PermissionError:
                result=[]
                #logger.warning('[PermissionError] '+full_filename)
                print('[PermissionError]',full_filename)

        elif filename.endswith(find_endswith):
            #如果不是目录，且是要找的文件
            print(full_filename)
            #logger.info(filename)
            result.append(full_filename)

    return result

if __name__=='__main__':
    if platform.system() == "Windows":
        if is_admin():
            result=scanner(file_dir='C:')
            length=len(result)
            print('共有%d个文件'%(length))
            #input("Press ENTER to exit")
        else:#获取管理员权限
            if sys.version_info[0] == 3:
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
            else:#in python2.x
                ctypes.windll.shell32.ShellExecuteW(None, u"runas", unicode(sys.executable), unicode(__file__), None, 1)
