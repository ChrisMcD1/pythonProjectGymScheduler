from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
import time as sleepyTime
import sys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from GoogleCalendarParser import GoogleCalendarParser, updateGymEvent
from datetime import datetime, date, time
import DuoRunner
from multiprocessing import Process, SimpleQueue

def schedulerMain():

    def stdGet(condition, value):
        return stdWait.until(EC.element_to_be_clickable((condition, value)))

    def stdClick(condition, value):
        stdGet(condition, value).click()
        return

    lookahead = 100
    gymEvent, service = GoogleCalendarParser(lookahead)
    if gymEvent == []:
        return f'No gym event was found in next {lookahead} events'
    startDateTime = gymEvent['start']['dateTime']
    [gymDate, badGymTime] = startDateTime.split('T')
    currentDate = date.today()
    splitCurrentDate = [int(x) for x in str(currentDate).split('-')]
    splitGymDate = [int(x) for x in str(gymDate).split('-')]

    # print(gymEvent['summary'])
    if 'REGISTERED' in gymEvent['summary']:
        # print(f'Gym event found, but had already registered')
        return f'Gym event found, but had already registered'

    gymTime = badGymTime.split('-')[0]

    now = datetime.now()
    currentTime = now.strftime("%H:%M:%S")

    splitCurrentTime = [int(temp) for temp in currentTime.split(':')]
    splitGymTime = [int(temp) for temp in gymTime.split(':')]

    gymMinuteTime = splitGymTime[0] * 60 + splitGymTime[1]
    currentMinuteTime = splitCurrentTime[0] * 60 + splitCurrentTime[1]



    if (splitGymDate[2] >= splitCurrentDate[2] + 1) and (gymMinuteTime > currentMinuteTime + 2): #If there is not a gym event the next day
        return f'Found gym event on {splitGymDate} at {gymTime} and determined it was too far in the future'

    # print(f'Found gym event tomorrow that is {currentMinuteTime - gymMinuteTime} minutes before now')
#######################################################################################################################
    # We have identified an event and are now trying to register for it
    returnQueue = SimpleQueue()
    triggerQueue = SimpleQueue()
    duoProcess = Process(target=DuoRunner.main, args=(triggerQueue, returnQueue))
    duoProcess.start()
    driver = webdriver.Chrome()
    driver.get("https://mycrc.gatech.edu/")
    stdWait = WebDriverWait(driver, 10)

    # Have to accept cookies so it doesn't get in they way. Have some weird StaleElementReferenceException so resort to while True
    while True:
        try:
            stdClick(By.XPATH, "//button[@id='gdpr-cookie-accept']")
            break
        except StaleElementReferenceException:
            continue

    # Presses login link in the top right
    stdClick(By.ID, "loginLink")

    # Presses GT login button on center of page
    stdClick(By.XPATH, "//button[@class='loginOption btn btn-lg btn-block btn-social btn-linkedin']")

    # Input my username and password
    GTUsernameInput = stdGet(By.ID, "username")
    GTPasswordInput = stdGet(By.ID, "password")
    with open("GTCredentials.txt", "r") as f:
        combinedUserPassword = f.read().splitlines()
        username = combinedUserPassword[0]
        password = combinedUserPassword[1]
        GTUsernameInput.send_keys(username)
        GTPasswordInput.send_keys(password)

    # Submit login credentials
    stdClick(By.XPATH, "//input[@class='button btn-submit']")

    # Begin process of getting around 2-factor
    driver.switch_to.frame("duo_iframe")

    # Need to do these presses to make that clickable
    phoneElement = Select(stdGet(By.XPATH, "//select[@name='device']"))
    phoneElement.select_by_value("phone3")
    print('Selected Phone')
    # stdClick(By.XPATH, "//button[contains(text(), 'Send Me a Push ')]")
    stdClick(By.XPATH, "//fieldset[@data-device-index='phone3']//button[contains(text(), 'Send Me a Push')]")
    # driver.find_element(By.XPATH, "//button[contains(text(), 'Send Me a Push ')]").click()
    # stdClick(By.XPATH, "//button[contains(text(), 'Send Me a Push ')]/ancestor::fieldset[@data-device-index='phone3']")
    print('Sent push')
    triggerQueue.put('Go gettem chief')

    # Waiting until Duo finishes its processes
    while returnQueue.empty():
        continue

    # # This switch might be implicit because we go to a new page, but it doesn't seem to hurt

    driver.switch_to.parent_frame()

    # Presses Make a Reservation Button. I'm still mad that they changed their site
    stdClick(By.XPATH, "//*[text()='Make a Reservation']/parent::a[@class='Menu-Item']")

    # Presses 1st Floor access
    stdClick(By.XPATH, "//*[text()='CRC 1st Floor Fitness']")

    # Cleaning up formattedGymTime to match the correct input
    if splitGymTime[0] > 12:
        splitGymTime[0] = splitGymTime[0] - 12
    if splitGymTime[1] == 0:
        formattedGymTime = f'{splitGymTime[0]}:00:00'
    else:
        formattedGymTime = f'{splitGymTime[0]}:{splitGymTime[1]}:00'


    # Registering for the formatted time
    attempts = 0
    slotOpen = False
    while attempts < 100 and not slotOpen:
        try:
            registrationXPATH = f'//button[contains(@onclick, "{formattedGymTime}")]'
            stdClick(By.XPATH, registrationXPATH)
            slotOpen = True
        except:
            continue

    if not slotOpen:
        driver.close()
        return print(f'Unable to find registration for {formattedGymTime}')

    # Press accept waiver button. Has some hidden button so I tried this workaround
    waiverButton = stdGet(By.XPATH, "//button[contains(.,'Accept Now')]")
    driver.execute_script("arguments[0].click();", waiverButton)

    # Press first checkout button
    stdClick(By.XPATH, "//button[@id='checkoutButton']")


    # NOT PRESSING THE SECOND CHECKOUT BUTTON SO I DON'T SPAM THEM
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # # # Press the second checkout button
    # stdClick(By.XPATH, "//button[contains(.,'Checkout') and @class='card-item-2-large']")

    # Should be registered!

    # Update the google calendar events
    updateGymEvent(gymEvent, service)
    # print('tried to do the update')
    sleepyTime.sleep(100)
    driver.close()
    return 'Successfully registered!'

if __name__ == '__main__':
    schedulerMain()