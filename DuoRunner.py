import subprocess
import os
import time
import pyperclip



def main(triggerQueue, returnQueue):
    #
    # p1 = subprocess.run(['dir','dne'], shell=True, stderr=subprocess.DEVNULL)
    # print(p1.stderr)
    # subprocess.call("notepad.exe")
    # subprocess.run('cd C:\\Users\\camcd\\.android\\avd\\Duo_Slave.avd', shell=True)
    subprocess.Popen("emulator -avd Duo_Slave -no-snapshot-save", shell=True)
    os.chdir("C:\\Users\\camcd\\AppData\\Local\\Android\\Sdk\\platform-tools")
    # print('got past cd')
    status = subprocess.run("adb devices", capture_output=True, text=True)
    thirdStatus = subprocess.run('adb shell getprop init.svc.bootanim', capture_output=True, text=True, shell=True)

    while status.stdout.split()[-1] != 'device' or 'stopped' not in thirdStatus.stdout:
        time.sleep(0.25)
        status = subprocess.run("adb devices", capture_output=True, text=True)
        # print(status.stdout.split())
        # print('stopped' not in thirdStatus.stdout)
        otherStatus = subprocess.run("adb shell service call power 12", capture_output=True, text=True)
        otherStatus = subprocess.run('adb shell dumpsys power | find "mWakefulness="', capture_output=True, text=True, shell=True)
        thirdStatus = subprocess.run('adb shell getprop init.svc.bootanim', capture_output=True, shell=True, text=True)
        # print(type(otherStatus.stdout))
        # print(thirdStatus.stdout)
    # print('finished checking')
    # print(thirdStatus.stdout)
    # time.sleep(1)

    while triggerQueue.empty():
        continue
    time.sleep(1)
    subprocess.call('adb shell am start com.duosecurity.duomobile/.account_list.AccountListActivity"', shell=True)
    time.sleep(8)
    subprocess.call("adb shell input touchscreen tap 550 430", shell=True)
    time.sleep(1)
    subprocess.call("adb shell input touchscreen tap 250 1960", shell=True)
    time.sleep(0.5)
    # subprocess.run("adb shell kill-server", shell=True)
    subprocess.run("Taskkill /IM qemu-system-x86_64.exe /F /T", shell=True)
    returnQueue.put("We done")
    return
    # return duoCodeRaw

if __name__ == '__main__':
    from multiprocessing import SimpleQueue
    triggerQueue = SimpleQueue()
    triggerQueue.put('Go get em chief')
    main(triggerQueue, SimpleQueue())