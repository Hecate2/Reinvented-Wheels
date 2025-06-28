import subprocess
import traceback
from random import randint
import time
import datetime
import re

'''input swipe 353 978 299 200 356'''
'''srcX, srcY, dstX, dstY, time(ms)'''
'''(x=0,y=0) at top left'''
'''resolution 1080 2400+'''


allowed_apps = {'com.xunmeng.pinduoduo', "com.sankuai.meituan", 'com.taobao.tao', "com.alipay.mobile", "com.eg.android.AlipayGphone", 'com.taobao.idlefish', "com.sina.weibo"}

app_name_regex = re.compile(r'mSurface=Surface\(name=(.*)\)')
app_area_regex = re.compile(r'rect=\(.*\) (\d+) x (\d+) transform=')
output_end_marker_regex = re.compile(r'^0$')


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


def allowed_app_focused(procId: subprocess.Popen) -> bool:
    cmd = """dumpsys window w | grep -v 'com.android.systemui.ImageWallpaper' | grep 'mSurface=Surface(name=com' -A 3 && echo \\0\n"""
    procId.stdin.write(cmd.encode())
    procId.stdin.flush()
    result = False
    output = ""
    # full output example for a split screen
    """
      mSurface=Surface(name=com.taobao.taobao/com.taobao.tao.welcome.Welcome)/@0xa8f1231
      Surface: shown=true layer=0 alpha=1.0 rect=(0.0,0.0) 1080 x 1528 transform=(1.0, 0.0, 1.0, 0.0)
      mDrawState=HAS_DRAWN       mLastHidden=false
      mEnterAnimationPending=false      mSystemDecorRect=[0,0][1080,2408] mLastClipRect=[0,0][0,0]
--
      mSurface=Surface(name=com.sankuai.meituan/com.sankuai.titans.adapter.mtapp.KNBWebViewActivity)/@0xa440d4a
      Surface: shown=true layer=0 alpha=1.0 rect=(0.0,0.0) 1080 x 872 transform=(1.0, 0.0, 1.0, 0.0)
      mDrawState=HAS_DRAWN       mLastHidden=false
      mEnterAnimationPending=false      mSystemDecorRect=[0,0][0,0] mLastClipRect=[0,0][0,0]
0   """
    try:
        while line := procId.stdout.readline().decode():
            if output_end_marker_regex.match(line):
                break
            output += line
    except subprocess.CalledProcessError as e:
        print(f"Error executing adb command: {e}")
    output_apps: list[str] = output.split('--')
    for output_app in output_apps:
        allowed_app_running = False
        if app_name := app_name_regex.search(output_app):
            app_name = app_name.group(1)
            for allowed_app in allowed_apps:
                if allowed_app in app_name:
                    allowed_app_running = True
                    break
            if allowed_app_running:
                if app_area := app_area_regex.search(output_app):
                    area_x, area_y = int(app_area.group(1)), int(app_area.group(2))
                    if area_y > 1400:
                        return True
    raise KeyboardInterrupt(f'Allowed apps not focused. Current app {output}')


def answer_call():
    # stop the whole program for now!
    raise NotImplementedError('DO NOT INVOKE THIS FUNCTION')
    # subprocess.call('adb shell input keyevent 5', shell=True)


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
                if not allowed_app_focused(procId):
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