import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expcond
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

myNameIs = "Track-It! Bot 1.2"

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
        log_out()

def find_work_order(workOder):
    try:
        workOrderId = WebDriverWait(driver, 5).until(expcond.presence_of_element_located((By.ID,"wo-browse-go-to-work-order-trigger-inputEl")))
        workOrderId.send_keys(Keys.CONTROL, "A")
        workOrderId.send_keys(Keys.DELETE)
        workOrderId.send_keys(workOrder)
        workOrderId.send_keys(Keys.ENTER)
        workOrderId = WebDriverWait(driver, 5).until(expcond.presence_of_element_located((By.ID,"wo-id-"+workOrder+"-inputEl")))
        return True
    except TimeoutException:
        msgBoxTitle = driver.find_element_by_id("messagebox-1001_header_hd-textEl")
        msgBoxContent = driver.find_element_by_id("messagebox-1001-displayfield-inputEl")
        msgBoxOK = driver.find_element_by_id("button-1005-btnIconEl")
        print("\n")
        #print("[ Track-It! ] "+msgBoxTitle.text)
        print("[ Track-It! ] "+msgBoxContent.text)
        msgBoxOK.click()
        return False
    except Exception as e:
        print(e)
        print("Error encountered while finding work order.")
        log_out()

def get_status():
    try:
        workOrderId = WebDriverWait(driver, 5).until(expcond.presence_of_element_located((By.ID,"wo-id-"+workOrder+"-inputEl")))
        workOrderId_value = workOrderId.get_attribute('value')
        time.sleep(2)  #required otherwise finalStatusvalue is blank
        #workOrderOpenDate = driver.find_element_by_id("datefield-1507-inputEl")
        #workOrderOpenDate_value = workOrderOpenDate.get_attribute('value')
        #workOrderOpenTime = driver.find_element_by_id("timefield-1508-inputEl")
        #workOrderOpenTime_value = workOrderOpenTime.get_attribute('value')         
        workOrderStatus = driver.find_element_by_id("wo-status-"+workOrder+"-inputEl")
        workOrderStatus_value = workOrderStatus.get_attribute('value')
        workOrderSummary = driver.find_element_by_id("wo-summary-"+workOrder+"-inputEl")
        workOrderSummary_value = workOrderSummary.get_attribute('value')
        workOrderRequestor = driver.find_element_by_id("wo-requestor-"+workOrder+"-inputEl")
        workOrderRequestor_value = workOrderRequestor.get_attribute('value')
        status = workOrderStatus_value.strip()
        status = status.lower()
        print("\n")
        print("[ Track-It! ]       WO#: "+workOrderId_value)
        #print("[ Track-It! ]    Opened: "+workOrderOpenDate_value+" "+workOrderOpenTime_value)
        print("[ Track-It! ]   Summary: "+workOrderSummary_value)
        print("[ Track-It! ] Requestor: "+workOrderRequestor_value)
        print("[ Track-It! ]    Status: "+workOrderStatus_value)
        #if (status == "closed"):
        #    workOrderCloseDate = driver.find_element_by_id("datefield-1503-inputEl")
        #    workOrderCloseDate_value = workOrderCloseDate.get_attribute('value')
        #    workOrderCloseTime = driver.find_element_by_id("timefield-1504-inputEl")
        #    workOrderCloseTime_value = workOrderCloseTime.get_attribute('value')   
        #    print("[ Track-It! ]    Closed: "+workOrderCloseDate_value+" "+workOrderCloseTime_value)
        return status
    except Exception as e:
        print(e)
        print("Error encountered while retrieving work order status.")
        log_out()

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
        log_out()

def close_work_order():
    try:
        closeWorkOrder = WebDriverWait(driver, 5).until(expcond.presence_of_element_located((By.ID,"wo-toggle-status-tb-button-"+workOrder+"-btnInnerEl")))
        closeWorkOrder.click()
        time.sleep(2)
    except Exception as e:
        print(e)
        print("Error encountered while closing work order.")
        log_out()

def save_work_order():
    try:
        saveWorkOrder = driver.find_element_by_id("wo-save-tb-button-"+workOrder+"-btnInnerEl")
        saveWorkOrder.click()
    except Exception as e:
        print(e)
        print("Error encountered while saving work order.")
        log_out()

def close_work_order_tab():
    try:
        close_tab = driver.find_element_by_id("tab-wo-edit-"+workOrder+"-closeEl")
        close_tab.click()
    except Exception as e:
        print(e)
        print("Error encountered while closing work order tab.")
        log_out()

def log_out():
    try:
        logOut = driver.find_element_by_id("ti-log-out-btnIconEl")
        logOut.click()
        time.sleep(2)
        print("\nExiting now.")
        print("\n###############################################################")
        driver.close()
        driver.quit()
        quit()        
    except Exception as e:
        print(e)
        print("Error encountered while logging out.")
        driver.close()
        driver.quit()
        quit() 

#--[Actions]------------------------------------------------------------------------------------------------------------------------------------------

#~~~[Log In]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
For GitHub
url = "http:\\\\<YourTrackItServer>\\TrackItWeb" 
user = "YourUserName"
passwd = "YourPassword"
"""

url = "http:\\\\sjcvmtkitapp1\\TrackItWeb"
user = "dgrewal"
passwd = "isdtkitdeep"

print("\n###################### "+myNameIs+" ######################")
log_in(url, user, passwd)

repeat = True

while (repeat == True):
    #~~~[Find Work Order]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    workOrder = 0
    confirmYN = "n"

    while not(confirmYN == "y" or confirmYN == ""):
        workOrder = input("\nEnter WO#: ").lower()
        if (workOrder == "q"):log_out()
        confirmYN = input("Confirm WO# "+workOrder+" [Y/n]: ").lower()
        if (confirmYN == "q"):log_out()
        workOrder = workOrder.strip()

    if not(find_work_order(workOrder)):
        continue

    #~~~[Return Status]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    status = get_status()

    #~~~[Take Actions]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if (status == "closed"):
        #print("\nWork Order has a status of closed.")
        close_work_order_tab()
        continue

    actionsAC = "x"

    while not(actionsAC == "a" or actionsAC == "c" or actionsAC == ""):
        actionsAC = input("\nDo you wish to add a note or close the work order? [a/C]:").lower()
        if (actionsAC == "q"): log_out()
        if (actionsAC == "a"):
            note = input("\nEnter text for note:")
            add_note(note)
        elif (actionsAC == "c" or actionsAC == ""):
            contactEPV = ""
            note = "Work order request fulfilled.  Requestor/affected party has been notified via"
            while not(contactEPV == "e" or contactEPV == "p" or contactEPV == "v"):
                contactEPV = input("\nSelect WO closing contact method [e/p/v]:\ne) email\np) phone\nv) voicemail\n").lower()
                if (contactEPV) == "q": log_out()
                if (contactEPV == "e"):
                    note = note+" email."
                elif (contactEPV == "p"):
                    note = note+" phone."
                else:
                    note = note+" voicemail."
            add_note(note)
            close_work_order()

    #~~~[Confirm and Save]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    saveYN = "x"
    saveWO = False

    while not(saveYN == "y" or saveYN == "n" or saveYN == ""):
        saveYN = input("\nSave changes to work order? [Y/n]:").lower()
        if (saveYN == "q"): log_out()
        saveWO = (saveYN == "y" or saveYN == "")

    if saveWO:
        save_work_order()
        get_status()

    close_work_order_tab()

    #~~~[Loop?]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    goAgain = input("\nUpdate another work order? [Y/n]").lower()

    if not(goAgain == "y" or goAgain == ""):
        repeat = False

log_out()