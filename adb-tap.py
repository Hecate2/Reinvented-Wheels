import subprocess
import traceback
from random import randint
import time
import datetime

'''input swipe 353 978 299 200 356'''
'''srcX, srcY, dstX, dstY, time(ms)'''
'''(x=0,y=0) at top left'''
'''resolution 1080 2400+'''


allowed_apps = {"com.sankuai.meituan"}


def water():
    x = randint(893, 978)
    y = randint(1849, 1940)
    return f'input tap {x} {y}\n'


def manure():
    x = randint(309,370)
    y = randint(1399, 1457)
    yield f'input tap {x} {y}\n'
    yield f'input tap {757} {1790}\n'
    yield f'input tap {229} {1906}\n'
    yield f'input tap {746} {1317}\n'
    yield f'input tap {864} {1637}\n'


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


def execute_adb_command(procId, command: str):
    procId.stdin.write(command.encode())
    if (result := get_call_state(procId)) == 1:
        answer_call()
    if not meituan_focused(procId):
        raise KeyboardInterrupt
    # else:
    #     print(f"No call: {result}")
    # procId.stdin.write(water_command.encode())
    procId.stdin.flush()


procId = subprocess.Popen('adb shell', stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
time.sleep(3)
for i in range(5):  # manure
# while 1:
    for i in range(8):  # water
        try:
            water_command = water()
            sleep_time = 2.5
            print(f'{datetime.datetime.now().isoformat()} sleep {sleep_time} seconds after: {water_command}', end='')
            execute_adb_command(procId, water_command)
            while sleep_time > 1:
                print('\r', end='')
                print(f'{datetime.datetime.now().isoformat()} time.sleep({sleep_time})', end='')
                time.sleep(1)
                sleep_time -= 1
            else:
                print('\r', end='')
                print(f'{datetime.datetime.now().isoformat()} time.sleep({sleep_time})', end='')
                time.sleep(sleep_time)
            print('\r', end='')
        except (Exception, KeyboardInterrupt) as e:
            print(e)
            traceback.print_exc()
            input("Press Enter to continue")
    print(f"{datetime.datetime.now().isoformat()} manure")
    for cmd in manure():
        print(cmd, end='')
        execute_adb_command(procId, cmd)
        time.sleep(0.5)
