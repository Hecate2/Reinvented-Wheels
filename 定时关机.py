import os, time

t=input(u'请输入几点几分关机(格式 05:59) :  ')
h_off, m_off = t.strip().split(":")
h_off, m_off = int(h_off), int(m_off)

t = time.localtime()
h, m = t.tm_hour, t.tm_min
print(f'当前时间：{h}:{m}')

if h > h_off:
    time_shut = h_off*3600 + m_off*60 - h*3600 - m*60 + 24*3600
else:
    time_shut = h_off*3600 + m_off*60 - h*3600 - m*60

print(time_shut)
os.system(f'shutdown -s -t {time_shut}')
print(f'关机计划完成,系统将在{time_shut}秒后关机....')
