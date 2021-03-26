import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expcond
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

ffoptions = webdriver.FirefoxOptions()
ffoptions.headless = True
driver = webdriver.Firefox(options=ffoptions)

def log_in(url, user, passwd):
    try:
        driver.get(url)
        userId = driver.find_element_by_id("login-user-inputEl")
        userId.send_keys(user)
        password = driver.find_element_by_id("login-password-inputEl")
        password.send_keys(passwd)
        login = driver.find_element_by_id("login-button-btnIconEl")
        login.click()
        time.sleep(2)
        workOrderId = driver.find_element_by_id("wo-browse-go-to-work-order-trigger-inputEl")
    except NoSuchElementException:
        closeOtherLogIn = driver.find_element_by_id("button-1006-btnIconEl")
        closeOtherLogIn.click()
    except Exception as e:
        print(e)
        print("Error encountered while logging in.")
        close_and_quit()

def find_work_order(workOder):
    try:
        workOrderId = WebDriverWait(driver, 5).until(expcond.presence_of_element_located((By.ID,"wo-browse-go-to-work-order-trigger-inputEl")))
        workOrderId.send_keys(workOrder)
        workOrderId.send_keys(Keys.ENTER)
    except Exception as e:
        print(e)
        print("Error encountered while finding work order.")
        close_and_quit()

def get_status():
    try:
        workOrderId = WebDriverWait(driver, 5).until(expcond.presence_of_element_located((By.ID,"wo-id-"+workOrder+"-inputEl")))
        workOrderId_value = workOrderId.get_attribute('value')
        time.sleep(2)  #required otherwise finalStatusvalue is blank
        workOrderStatus = driver.find_element_by_id("wo-status-"+workOrder+"-inputEl")
        workOrderStatus_value = workOrderStatus.get_attribute('value')
        workOrderSummary = driver.find_element_by_id("wo-summary-"+workOrder+"-inputEl")
        workOrderSummary_value = workOrderSummary.get_attribute('value')
        status = workOrderStatus_value.strip()
        print("\n")
        print("[ Track-It! ]     WO#: "+workOrderId_value)
        print("[ Track-It! ] Summary: "+workOrderSummary_value)
        print("[ Track-It! ]  Status: "+workOrderStatus_value)
        return status.lower()
    except Exception as e:
        print(e)
        print("Error encountered while retrieving work order status.")
        close_and_quit()

def add_note(note):
    try:
        note = "[ Track-It! Bot ]: "+note
        workOrderNote = WebDriverWait(driver, 5).until(expcond.presence_of_element_located((By.ID,"wo-note-text-"+workOrder+"-inputEl")))
        workOrderNote.send_keys(note)
        addNote = driver.find_element_by_id("wo-note-add-"+workOrder+"-btnIconEl")
        addNote.click()
    except Exception as e:
        print(e)
        print("Error encountered while adding note.")
        close_and_quit()

def close_work_order():
    try:
        closeWorkOrder = WebDriverWait(driver, 5).until(expcond.presence_of_element_located((By.ID,"wo-toggle-status-tb-button-"+workOrder+"-btnInnerEl")))
        closeWorkOrder.click()
        time.sleep(2)
    except Exception as e:
        print(e)
        print("Error encountered while closing work order.")
        close_and_quit()

def save_work_order():
    try:
        saveWorkOrder = driver.find_element_by_id("wo-save-tb-button-"+workOrder+"-btnInnerEl")
        saveWorkOrder.click()
    except Exception as e:
        print(e)
        print("Error encountered while saving work order.")
        close_and_quit()

def log_out():
    try:
        logOut = driver.find_element_by_id("ti-log-out-btnIconEl")
        logOut.click()
    except Exception as e:
        print(e)
        print("Error encountered while logging out.")
        close_and_quit()

def close_and_quit():
        print("\nExiting now.")
        driver.close()
        driver.quit()
        "\n###############################################################"
        quit()

#--[Actions]------------------------------------------------------------------------------------------------------------------------------------------

#~~~[Log In]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
For GitHub
url = "http:\\\\<YourTrackItServer>\\TrackItWeb" 
user = "YourUserName"
passwd = "YourPassword"
"""

print("\n###################### Track-It! Bot 1.0 ######################")
log_in(url, user, passwd)

#~~~[Find Work Order]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
workOrder = 0
confirmYN = "n"

while not(confirmYN == "y" or confirmYN == ""):
    workOrder = input("\nEnter WO#: ")
    confirmYN = input("Confirm WO# "+workOrder+" [Y/n]: ").lower()
    workOrder = workOrder.strip()

find_work_order(workOrder)

#~~~[Return Status]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
status = get_status()

#~~~[Take Actions]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if (status == "closed"):
    print("\nWork Order has a status of closed.")
    time.sleep(7)
    log_out()
    close_and_quit()

actionsAC = "x"

while not(actionsAC == "a" or actionsAC == "c" or actionsAC == ""):
    actionsAC = input("\nDo you wish to add a note or close the work order? [a/C]:").lower()
    if (actionsAC == "a"):
        note = input("\nEnter text for note:")
        add_note(note)
    elif (actionsAC == "c" or actionsAC == ""):
        contactEPV = ""
        note = "Work order request fulfilled.  Requestor/affected party has been notified via"
        while not(contactEPV == "e" or contactEPV == "p" or contactEPV == "v"):
            contactEPV = input("\nSelect WO closing contact method [e/p/v]:\ne) email\np) phone\nv) voicemail\n").lower()
            if (contactEPV == "e"):
                note = note+" email."
            elif (contactEPV == "p"):
                note = note+" phone."
            else:
                note = note+" voicemail."
        add_note(note)
        close_work_order()

#~~~[Confirm and Save]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
saveYN = "x"
saveWO = False

while not(saveYN == "y" or saveYN == "n" or saveYN == ""):
    saveYN = input("\nSave changes to work order? [Y/n]:").lower()
    saveWO = (saveYN == "y" or saveYN == "")

if saveWO:
    save_work_order()
    get_status()
    time.sleep(7)

log_out()
close_and_quit()