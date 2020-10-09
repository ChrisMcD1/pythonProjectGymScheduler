from Scheduler import schedulerMain
import time
from datetime import datetime

def main():
    f = open('Log.txt', 'w')
    count = 0
    previousLine = ''
    while True:
        result = schedulerMain()
        now = datetime.now()
        currentTime = now.strftime("%H:%M:%S")
        if previousLine != result:
            f.write(f'{currentTime}: {result}\n')
        previousLine = result
        if count % 10 == 0:
            f.close()
            f = open('Log.txt', 'a+')
        print(result)
        count += 1
        time.sleep(1)

if __name__ == '__main__':
    main()