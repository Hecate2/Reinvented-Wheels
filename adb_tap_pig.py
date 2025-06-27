import subprocess
import traceback
from random import randint
import time
import datetime

allowed_apps = {"com.sankuai.meituan"}


def gen_tap_cmd():
    return f'input tap 554 758\n'


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
    output = ""
    try:
        while line := procId.stdout.readline().decode():
            output += line
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
        raise KeyboardInterrupt(f'Allowed apps not focused. Current app {output}')


def answer_call():
    # stop the whole program for now!
    raise NotImplementedError('DO NOT INVOKE THIS FUNCTION')
    subprocess.call('adb shell input keyevent 5', shell=True)


procId = subprocess.Popen('adb shell', stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
time.sleep(3)
while 1:
    try:
        swipe = gen_tap_cmd()
        sleep_time = 1
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