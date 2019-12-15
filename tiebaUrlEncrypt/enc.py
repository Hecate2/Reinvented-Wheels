#coding:utf-8
#将url的字符全部加密，便于百度贴吧发帖
#可从命令行直接输入待加密字符串，也可以把待加密字符串写入input.txt
#输出为encrypted.txt

import logging,sys,getopt,time,os
#logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.basicConfig(level = logging.INFO,format = '[%(levelname)s] - %(message)s')
logger = logging.getLogger(__name__)
 
#logger.info("Start print log")
#logger.debug("Do something")
#logger.warning("Something maybe fail.")
#logger.info("Finish")

#str_in='https://github.com/Hecate2/ISML_auto_voter/raw/master/DestroyerIGN/CINT%20the%20Space%20Fleet%20Hecate2%20(%E6%9C%AA%E9%85%8D%E4%B9%90).docx'
#str_in='䁨䁴䁴䁰䁳䀺䀯䀯䁧䁩䁴䁨䁵䁢䀮䁣䁯䁭䀯䁈䁥䁣䁡䁴䁥䀲䀯䁉䁓䁍䁌䁟䁡䁵䁴䁯䁟䁶䁯䁴䁥䁲䀯䁲䁡䁷䀯䁭䁡䁳䁴䁥䁲䀯䁄䁥䁳䁴䁲䁯䁹䁥䁲䁉䁇䁎䀯䁃䁉䁎䁔䀥䀲䀰䁴䁨䁥䀥䀲䀰䁓䁰䁡䁣䁥䀥䀲䀰䁆䁬䁥䁥䁴䀥䀲䀰䁈䁥䁣䁡䁴䁥䀲䀥䀲䀰䀨䀥䁅䀶䀥䀹䁃䀥䁁䁁䀥䁅䀹䀥䀸䀵䀥䀸䁄䀥䁅䀴䀥䁂䀹䀥䀹䀰䀩䀮䁤䁯䁣䁸'
#str_in=r'''ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789%-_.~!*'();:@&=+$,/?#[]'''

pswd=16384

def enc(str_in,pswd):
    #seed(pswd)
    li_out=[chr(ord(i)^pswd) for i in str_in]
    return ''.join(li_out)

if __name__=='__main__':
    try:
        import pyperclip
    except Exception as e:
        logger.info('pip install pyperclip可享受剪贴板输入输出！')
        os.system('pip install pyperclip')
        import pyperclip
    sleepTime=10
    defaultFilename='input.txt'
    if len(sys.argv)>1:
        str_in=sys.argv[1]
    else:
        logger.info('正在从%s获取输入'%(defaultFilename))
        try:
            with open(defaultFilename,'r',encoding=('utf-8')) as f:
                str_in=f.read()
        except Exception:
            logger.warning('获取输入失败。请检查是否存在%s。%s秒后自动退出'%(defaultFilename,sleepTime))
            time.sleep(sleepTime)
            sys.exit(1)
    encrypted=enc(str_in,pswd)
    print('原字符串:%s'%(str_in))
    print('加密字符串:%s'%(encrypted))
    restored=enc(encrypted,pswd)
    print('还原后字符串:%s'%(restored))

    print()
    if restored!=str_in:
        logger.warning("还原后字符串与原始字符串不一致")
    else:
        logger.info("还原后字符串与原字符串一致")
    saveToFile=input("退出窗口或按Ctrl+C放弃本次结果\n输入任意内容，然后按Enter可将结果[覆盖]到encrypted.txt\n不论是否输入内容，按Enter可复制结果\n")
    if(saveToFile):
        with open('encrypted.txt','w',encoding=('utf-8')) as f:
            f.write(encrypted)
        logger.info('加密结果已保存到encrypted.txt')
    try:
        import pyperclip
        pyperclip.copy(encrypted)
        logger.info('复制成功')
    except Exception as e:
        logger.warning('复制失败：%s'%(str(e)))
    sleepTime/=2
    logger.info('%d秒后自动退出'%(sleepTime))
    time.sleep(sleepTime)
