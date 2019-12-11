# Reinvented-Wheels
一些小工具（重新发明的轮子）  
  
我们都不想重新发明轮子，然而有时候就是没有办法  
  
GPAcalc: Weighted average to calculate your GPA. (What a tiresome work to write such codes!)  
  
IgnaleoG: Combat-proven *destroyer* (a type of battleship) sending HTTP requests with stability and virtually unlimited concurrency. It runs as an HTTP server, and launches jobs when you visit it. Example offered at https://github.com/Hecate2/ISML_auto_voter and *mysql.py* in this repository. Recommended accessories: retryapi.py & compat.py.  

mysql.py & sqlalchemyOps.py: test the performance of mysql libraries with IgnaleoG. Gevent does not speed up SQL queries!  
  
retryapi.py & compat.py: They provide decorators for non-asynchronous functions. Retry running the decorated function for a few times when an Exception occurs in the function.  
  
arrayvideo: plays a 3-dimensional numpy array[height, width, number_of_frames] as a video on Windows  

grayimg: transform any image into gray a one. Just faster and more convenient than heavy softwares.  
  
tiebaUrlEncrypt: This is not meant to encrypt messages to confuse humans. You know Baidu Tieba forbids all kinds of URLs, so we have to post URLs encrypted with this tool (*enc.py*) to confuse Tieba.  
Example input and outut:  
**https://github.com/Hecate2/ISML_auto_voter/raw/master/DestroyerIGN/CINT%20the%20Space%20Fleet%20Hecate2%20(%E6%9C%AA%E9%85%8D%E4%B9%90).docx**  
**䁨䁴䁴䁰䁳䀺䀯䀯䁧䁩䁴䁨䁵䁢䀮䁣䁯䁭䀯䁈䁥䁣䁡䁴䁥䀲䀯䁉䁓䁍䁌䁟䁡䁵䁴䁯䁟䁶䁯䁴䁥䁲䀯䁲䁡䁷䀯䁭䁡䁳䁴䁥䁲䀯䁄䁥䁳䁴䁲䁯䁹䁥䁲䁉䁇䁎䀯䁃䁉䁎䁔䀥䀲䀰䁴䁨䁥䀥䀲䀰䁓䁰䁡䁣䁥䀥䀲䀰䁆䁬䁥䁥䁴䀥䀲䀰䁈䁥䁣䁡䁴䁥䀲䀥䀲䀰䀨䀥䁅䀶䀥䀹䁃䀥䁁䁁䀥䁅䀹䀥䀸䀵䀥䀸䁄䀥䁅䀴䀥䁂䀹䀥䀹䀰䀩䀮䁤䁯䁣䁸**  
*enc.py* uses simple XOR (exclusive OR, 0 xor 1 = 1) operations mapping URLs to Chinese characters. To restore the original URL, use the encrypted output as the input of *enc.py*. The encrypter and the decrypter should use the same program and the same parameter. Enjoy URLs of magic realism in Tieba!  
**Notice that *enc.py* is not safe at all as cryptography. Do not encrypt important messages only with *enc.py***.  
