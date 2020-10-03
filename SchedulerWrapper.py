from Scheduler import schedulerMain
import time

def main():

    while True:
        result = schedulerMain()
        print(result)
        time.sleep(1)

if __name__ == '__main__':
    main()