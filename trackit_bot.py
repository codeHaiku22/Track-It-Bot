import time
import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expcond
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

myNameIs = "Track-It! Bot 1.5"

ffoptions = webdriver.FirefoxOptions()
ffoptions.headless = True
driver = webdriver.Firefox(options=ffoptions)
waitSeconds = 10

#---[ Functions ]-------------------------------------------------------------------------------------------------------------------------------------

def log_in(url, user, passwd):
    try:
        driver.get(url)
        userId = WebDriverWait(driver, waitSeconds).until(expcond.presence_of_element_located((By.ID,"login-user-inputEl")))
        userId.send_keys(user)
        password = driver.find_element_by_id("login-password-inputEl")
        password.send_keys(passwd)
        login = driver.find_element_by_id("login-button-btnIconEl")
        login.click()
        time.sleep(2)
        workOrderId = driver.find_element_by_id("wo-browse-go-to-work-order-trigger-inputEl")
    except NoSuchElementException: #Still at login screen
        loginStatusMessage = driver.find_element_by_id("login-status")
        if (loginStatusMessage.text.strip() == ''):
            closeOtherLogIn = WebDriverWait(driver, waitSeconds).until(expcond.presence_of_element_located((By.ID,"button-1006-btnIconEl")))
            closeOtherLogIn.click()
        else:
            print(loginStatusMessage.text)
            log_out(False)
    except Exception as e:
        print(e)
        print("Error encountered while logging in.")
        log_out()

def find_work_order(workOder):
    try:
        workOrderId = WebDriverWait(driver, waitSeconds).until(expcond.presence_of_element_located((By.ID,"wo-browse-go-to-work-order-trigger-inputEl")))
        workOrderId.send_keys(Keys.CONTROL, "A")
        workOrderId.send_keys(Keys.DELETE)
        workOrderId.send_keys(workOrder)
        workOrderId.send_keys(Keys.ENTER)
        workOrderId = WebDriverWait(driver, waitSeconds).until(expcond.presence_of_element_located((By.ID,"wo-id-"+workOrder+"-inputEl")))
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
        workOrderId = WebDriverWait(driver, waitSeconds).until(expcond.presence_of_element_located((By.ID,"wo-id-"+workOrder+"-inputEl")))
        workOrderId_value = workOrderId.get_attribute('value')
        time.sleep(2)  #required otherwise finalStatusvalue is blank
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
        print("[ Track-It! ]   Summary: "+workOrderSummary_value)
        print("[ Track-It! ] Requestor: "+workOrderRequestor_value)
        print("[ Track-It! ]    Status: "+workOrderStatus_value)
        return status
    except Exception as e:
        print(e)
        print("Error encountered while retrieving work order status.")
        log_out()

def get_workorder_list(status):
    try:
        singleWO = []
        workOrderList = []
        viewsDropDown = WebDriverWait(driver, waitSeconds).until(expcond.presence_of_element_located((By.ID,"wo-browse-inner-view-button-btnWrap")))
        viewsDropDown.click()
        if (status == "c"):
            menuEntry = WebDriverWait(driver, waitSeconds).until(expcond.presence_of_element_located((By.LINK_TEXT,"Closed Work Orders")))
        elif (status == "o"):
            menuEntry = WebDriverWait(driver, waitSeconds).until(expcond.presence_of_element_located((By.LINK_TEXT,"My Open Work Orders")))
        menuEntry.click()  
        time.sleep(3)  #let table populate
        workOrderTable0 = driver.find_element_by_id("gridview-1027-table")
        for row0 in workOrderTable0.find_elements_by_class_name("x-grid-row"):
            workOrderTable1 = row0.find_element_by_class_name("x-grid-table")
            for row1 in workOrderTable1.find_elements_by_class_name("x-grid-data-row"):
                for cell in row1.find_elements_by_class_name("x-grid-cell"):
                    singleWO.append(cell.text)
                workOrderList.append(singleWO.copy())
                singleWO.clear()
        if (status == "c"):
            print("\nClosed work orders:\n")
            for list in workOrderList:
                datetimeObj = datetime.datetime.strptime(list[4].strip(), '%m/%d/%Y %I:%M:%S %p')
                print(list[2].ljust(9), "Closed   ", datetimeObj.strftime('%m/%d/%Y %H:%M').ljust(19), list[7].ljust(30), list[6][0:50])            
        elif (status == "o"):
            print("\nOpen work orders:\n")
            for list in workOrderList:
                datetimeObj = datetime.datetime.strptime(list[4].strip(), '%m/%d/%Y %I:%M:%S %p')
                print(list[2].ljust(9), "Open   ", datetimeObj.strftime('%m/%d/%Y %H:%M').ljust(19), list[3].ljust(25), list[6].ljust(30), list[5][0:50])
    except Exception as e:
        print(e)
        print("Error encountered while retrieving work order list.")
        log_out()         

def add_note(note):
    try:
        note = "[ Track-It! Bot ]: "+note
        workOrderNote = WebDriverWait(driver, waitSeconds).until(expcond.presence_of_element_located((By.ID,"wo-note-text-"+workOrder+"-inputEl")))
        workOrderNote.send_keys(note)
        addNote = driver.find_element_by_id("wo-note-add-"+workOrder+"-btnIconEl")
        addNote.click()
    except Exception as e:
        print(e)
        print("Error encountered while adding note.")
        log_out()

def close_work_order():
    try:
        closeWorkOrder = WebDriverWait(driver, waitSeconds).until(expcond.presence_of_element_located((By.ID,"wo-toggle-status-tb-button-"+workOrder+"-btnInnerEl")))
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

def log_out(loggedIn = True):
    try:
        if (loggedIn):
            logOut = driver.find_element_by_id("ti-log-out-btnIconEl")
            logOut.click()
            time.sleep(2)
    except Exception as e:
        print(e)
        print("Error encountered while logging out.")
    finally:
        print("\nExiting now.")
        print("\n###############################################################")
        driver.close()
        driver.quit()
        quit()        

#---[Actions]-----------------------------------------------------------------------------------------------------------------------------------------

#~~~[Log In]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
url = "http:\\\\<YourTrackItServer>\\TrackItWeb" 
user = "YourUserName"
passwd = "YourPassword"

print("\n###################### "+myNameIs+" ######################")
log_in(url, user, passwd)

#:::[ Outer Loop]:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
repeatMainMenu = True

while (repeatMainMenu == True):
    #~~~[Main Menu]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    menuEntryFOCQ = "x"

    while not(menuEntryFOCQ == "f" or menuEntryFOCQ == "o" or menuEntryFOCQ == "c" or menuEntryFOCQ == ""):
        menuEntryFOCQ = input ("\nSelect an action to perform [F/o/c]:\nf) Find a work order\no) Display open work orders\nc) Display closed work orders\nq) Quit\n").lower()
        if (menuEntryFOCQ == "q"):log_out()
        if (menuEntryFOCQ == "" or menuEntryFOCQ == "f"):
            pass
        elif (menuEntryFOCQ == "o" or menuEntryFOCQ == "c"):
            get_workorder_list(menuEntryFOCQ)
            menuEntryFOCQ = "x"
    
    #:::[ Inner Loop]:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    #~~~[Find Work Order]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    repeatFindWorkOrder = True

    while (repeatFindWorkOrder == True):
        workOrder = 0
        confirmYN = "n"

        while not(confirmYN == "y" or confirmYN == ""):
            workOrder = input("\nEnter work order#: ").lower()
            if (workOrder == "q"):log_out()
            confirmYN = input("Confirm work order# "+workOrder+" [Y/n]: ").lower()
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
            break

        actionsAC = "x"

        while not(actionsAC == "a" or actionsAC == "c" or actionsAC == ""):
            actionsAC = input("\nDo you wish to add a note or close the work order? [a/C]: ").lower()
            if (actionsAC == "q"): log_out()
            if (actionsAC == "a"):
                note = input("\nEnter text for note: ")
                add_note(note)
            elif (actionsAC == "c" or actionsAC == ""):
                contactEPV = ""
                note = "Work order request fulfilled.  Requestor/affected party has been notified via"
                while not(contactEPV == "e" or contactEPV == "p" or contactEPV == "v"):
                    contactEPV = input("\nSelect work order closing contact method [e/p/v]:\ne) email\np) phone\nv) voicemail\n").lower()
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
            saveYN = input("\nSave changes to work order? [Y/n]: ").lower()
            if (saveYN == "q"): log_out()
            saveWO = (saveYN == "y" or saveYN == "")

        if saveWO:
            save_work_order()
            get_status()

        close_work_order_tab()

        #~~~[Find Another Work Order?]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        updateAnotherWO = input("\nUpdate another work order? [Y/n]: ").lower()
        
        if not(updateAnotherWO == "y" or updateAnotherWO == ""):
            if (updateAnotherWO == "q"): log_out()
            repeatFindWorkOrder = False