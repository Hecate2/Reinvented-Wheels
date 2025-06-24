import subprocess
import traceback
from random import randint
import time
import datetime

'''input swipe 353 978 299 200 356'''
'''srcX, srcY, dstX, dstY, time(ms)'''
'''(x=0,y=0) at top left'''
'''resolution 1080 2400+'''


allowed_apps = {'com.xunmeng.pinduoduo', "com.sankuai.meituan", 'com.taobao.tao', "com.alipay.mobile", "com.eg.android.AlipayGphone", 'com.taobao.idlefish'}


def gen_swipe_cmd():
    srcX = randint(137, 772)
    srcY = randint(823, 1400)
    return f'input swipe {srcX} {srcY} {srcX + randint(-77, 120)} {srcY - randint(223, 726)} {randint(50, 97)}\n'


def get_call_state(procId: subprocess.Popen) -> int:
    cmd = 'dumpsys telephony.registry | grep mCallState && echo \\0\n'
    procId.stdin.write(cmd.encode())
    procId.stdin.flush()
    try:
        current_state: int = 0
        while line := procId.stdout.readline().decode():
            if "mCallState" in line:
                call_state = line.split("=")[1].strip()
                if (call_state := int(call_state)) > current_state:
                    current_state = call_state
            if line.replace('\r', '') == '0\n':
                break
        return current_state
    except subprocess.CalledProcessError as e:
        print(f"Error executing adb command: {e}")


def meituan_focused(procId: subprocess.Popen) -> bool:
    cmd = 'dumpsys window | grep mCurrentFocus && echo \\0\n'
    procId.stdin.write(cmd.encode())
    procId.stdin.flush()
    result = False
    try:
        while line := procId.stdout.readline().decode():
            if not result:
                for app in allowed_apps:
                    if app in line:
                        result = True
            if line.replace('\r', '') == '0\n':
                break
    except subprocess.CalledProcessError as e:
        print(f"Error executing adb command: {e}")
    if result:
        return True
    else:
        raise KeyboardInterrupt('Allowed apps not focused')


def answer_call():
    # stop the whole program for now!
    raise NotImplementedError('DO NOT INVOKE THIS FUNCTION')
    subprocess.call('adb shell input keyevent 5', shell=True)


procId = subprocess.Popen('adb shell', stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
time.sleep(3)
while 1:
    try:
        swipe = gen_swipe_cmd()
        sleep_time = randint(3, 14)
        print(f'{datetime.datetime.now().isoformat()} sleep {sleep_time} seconds after: {swipe}', end='')
        while 1:
            try:
                if (result := get_call_state(procId)) == 1:
                    answer_call()
                if not meituan_focused(procId):
                    raise KeyboardInterrupt
                break
            except KeyboardInterrupt:
                raise
            except BrokenPipeError:
                procId.kill()
                traceback.print_exc()
                procId = subprocess.Popen('adb shell', stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
                time.sleep(3)
            # else:
            #     print(f"No call: {result}")
        while 1:
            try:
                procId.stdin.write(swipe.encode())
                procId.stdin.flush()
                break
            except BrokenPipeError:
                procId.kill()
                traceback.print_exc()
                procId = subprocess.Popen('adb shell', stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
                time.sleep(3)
        while sleep_time > 0:
            print('\r', end='')
            print(f'{datetime.datetime.now().isoformat()} time.sleep({sleep_time})', end='')
            time.sleep(1)
            sleep_time -= 1
        print('\r', end='')
    except (Exception, KeyboardInterrupt) as e:
        print(e)
        traceback.print_exc()
        input("Press Enter to continue")