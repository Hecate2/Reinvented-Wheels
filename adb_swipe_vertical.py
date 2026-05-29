import subprocess
import sys
import traceback
from random import randint
import time
import datetime
import re

'''input swipe 353 978 299 200 356'''
'''srcX, srcY, dstX, dstY, time(ms)'''
'''(x=0,y=0) at top left'''
'''resolution 1080 2400+'''


allowed_apps = {'com.xunmeng.pinduoduo', "com.sankuai.meituan", 'com.sankuai.meituan', 'com.taobao.tao', "com.alipay.mobile", "com.eg.android.AlipayGphone", 'com.taobao.idlefish', "com.sina.weibo", "com.tmall.wireless", "com.cat.readall"}

app_name_regex = re.compile(r'mSurface=Surface\(name=(.*?)\)')
focus_window_regex = re.compile(r'mCurrentFocus=Window\{[^}]+ ([^ ]+)\}')
window_header_regex = re.compile(r'Window #\d+ Window\{[^}]+ ([^ ]+)\}:')
window_config_regex = re.compile(r'mBounds=Rect\((\d+), (\d+) - (\d+), (\d+)\).*mWindowingMode=([a-z\-]+)')
output_end_marker_regex = re.compile(r'^0[\r]?$')
cmd_args = sys.argv
try: min_sleep_seconds = int(cmd_args[1])
except: min_sleep_seconds = 3
try: max_sleep_seconds = int(cmd_args[2])
except: max_sleep_seconds = 14

def rand_between(low: int, high: int) -> int:
    if low >= high:
        return low
    return randint(low, high)


def is_allowed_app(app_name: str) -> bool:
    for allowed_app in allowed_apps:
        if allowed_app in app_name:
            return True
    return False


def get_package_name(window_name: str) -> str:
    return window_name.split('/', 1)[0]


def is_same_app(window_name: str, focus_name: str) -> bool:
    if not window_name or not focus_name:
        return False
    return get_package_name(window_name) == get_package_name(focus_name)


def gen_swipe_cmd(bounds=None):
    # if bounds is None:
    srcX = randint(137, 772)
    srcY = randint(700, 750)
    return f'input swipe {srcX} {srcY} {srcX + randint(-77, 120)} {srcY - randint(600, 700)} {randint(50, 97)}\n'

    left, top, right, bottom = bounds
    width = max(right - left, 1)
    height = max(bottom - top, 1)
    srcX = rand_between(left + width // 8, left + width * 5 // 6)
    srcY = rand_between(top + height * 2 // 3, top + height * 9 // 10)
    dstX = max(left, min(right, srcX + randint(-77, 120)))
    dstY = rand_between(top + height // 5, top + height * 2 // 5)
    return f'input swipe {srcX} {srcY} {dstX} {dstY} {randint(50, 97)}\n'

def gen_small_swipe_cmd(bounds=None):
    # if bounds is None:
    return f'input swipe 237 223 237 123\n'

    left, top, right, bottom = bounds
    width = max(right - left, 1)
    height = max(bottom - top, 1)
    srcX = left + width // 2
    srcY = top + height * 3 // 4
    dstY = top + height * 2 // 3
    return f'input swipe {srcX} {srcY} {srcX} {dstY} {randint(30, 55)}\n'

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


def allowed_app_focused(procId: subprocess.Popen):
    cmd = "dumpsys window | grep -Ei 'mCurrentFocus='; dumpsys window windows && echo \\0\n"
    procId.stdin.write(cmd.encode())
    procId.stdin.flush()
    output = ""
    try:
        while line := procId.stdout.readline().decode():
            if output_end_marker_regex.match(line):
                break
            output += line
    except subprocess.CalledProcessError as e:
        print(f"Error executing adb command: {e}")

    focus_app = None
    visible_windows = []
    current_window = None

    def append_window(window):
        if not window:
            return
        if window.get('visible') and window.get('app_name') and window.get('bounds'):
            visible_windows.append(window)

    for raw_line in output.splitlines():
        line = raw_line.strip()
        if focus_match := focus_window_regex.search(line):
            focus_app = focus_match.group(1)
            continue
        if window_match := window_header_regex.search(line):
            append_window(current_window)
            current_window = {
                'window_name': window_match.group(1),
                'app_name': None,
                'bounds': None,
                'windowing_mode': None,
                'visible': False,
            }
            continue
        if current_window is None:
            continue
        if config_match := window_config_regex.search(line):
            current_window['bounds'] = tuple(int(value) for value in config_match.groups()[:4])
            current_window['windowing_mode'] = config_match.group(5)
            continue
        if app_name_match := app_name_regex.search(line):
            current_window['app_name'] = app_name_match.group(1)
            continue
        if 'Surface: shown=true' in line:
            current_window['visible'] = True

    append_window(current_window)

    top_split_window = None
    for window in visible_windows:
        if window['windowing_mode'] == 'split-screen-primary':
            top_split_window = window
            break

    if top_split_window is not None:
        top_app_name = top_split_window['app_name']
        if not is_allowed_app(top_app_name):
            raise KeyboardInterrupt(f'Upper split app not allowed. focus={focus_app} top={top_app_name}')
        top_focused = is_same_app(top_app_name, focus_app)
        return True, (not top_focused), top_split_window['bounds']

    for window in visible_windows:
        app_name = window['app_name']
        if is_allowed_app(app_name) and is_same_app(app_name, focus_app):
            return True, False, None

    visible_apps = [window['app_name'] for window in visible_windows]
    raise KeyboardInterrupt(f'Allowed apps not focused. focus={focus_app} visible={visible_apps}')


def answer_call():
    # stop the whole program for now!
    raise NotImplementedError('DO NOT INVOKE THIS FUNCTION')
    # subprocess.call('adb shell input keyevent 5', shell=True)


procId = subprocess.Popen('adb shell', stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
time.sleep(3)
while 1:
    try:
        sleep_time = randint(min_sleep_seconds, max_sleep_seconds)
        while 1:
            try:
                if (result := get_call_state(procId)) == 1:
                    answer_call()
                (focused, should_focus_first, swipe_bounds) = allowed_app_focused(procId)
                if not focused:
                    raise KeyboardInterrupt
                swipe = gen_swipe_cmd(swipe_bounds)
                if should_focus_first:
                    swipe = gen_small_swipe_cmd(swipe_bounds) + swipe
                print(f'{datetime.datetime.now().isoformat()} sleep {sleep_time} seconds after: {swipe}', end='')
                break
            except KeyboardInterrupt:
                raise
            except (BrokenPipeError, OSError):
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
