#coding:utf-8
#将url的字符全部加密，便于百度贴吧发帖

#str_in='https://github.com/Hecate2/ISML_auto_voter/raw/master/DestroyerIGN/CINT%20the%20Space%20Fleet%20Hecate2%20(%E6%9C%AA%E9%85%8D%E4%B9%90).docx'
#str_in='䁨䁴䁴䁰䁳䀺䀯䀯䁧䁩䁴䁨䁵䁢䀮䁣䁯䁭䀯䁈䁥䁣䁡䁴䁥䀲䀯䁉䁓䁍䁌䁟䁡䁵䁴䁯䁟䁶䁯䁴䁥䁲䀯䁲䁡䁷䀯䁭䁡䁳䁴䁥䁲䀯䁄䁥䁳䁴䁲䁯䁹䁥䁲䁉䁇䁎䀯䁃䁉䁎䁔䀥䀲䀰䁴䁨䁥䀥䀲䀰䁓䁰䁡䁣䁥䀥䀲䀰䁆䁬䁥䁥䁴䀥䀲䀰䁈䁥䁣䁡䁴䁥䀲䀥䀲䀰䀨䀥䁅䀶䀥䀹䁃䀥䁁䁁䀥䁅䀹䀥䀸䀵䀥䀸䁄䀥䁅䀴䀥䁂䀹䀥䀹䀰䀩䀮䁤䁯䁣䁸'
#str_in=r'''ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789%-_.~!*'();:@&=+$,/?#[]'''
with open('input.txt','r',encoding=('utf-8')) as f:
    str_in=f.read()

pswd=16384

def enc(str_in,pswd):
    #seed(pswd)
    li_out=[chr(ord(i)^pswd) for i in str_in]
    return ''.join(li_out)

encrypted=enc(str_in,pswd)
print('原字符串:%s'%(str_in))
print('加密字符串:%s'%(encrypted))
print('还原后字符串:%s'%(enc(encrypted,pswd)))
with open('encrypted.txt','w',encoding=('utf-8')) as f:
    f.write(encrypted)
print('\n加密结果已保存到encrypted.txt')
