import time as sleeper

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

try:
    import secrets
    ASK_CREDENTIALS = False
except:
    ASK_CREDENTIALS = True

# Should exception messages be printed
PRINT_EXCEPTIONS = True

# The time to wait before the webdriver decides that the element does not exist
WAIT_TIME = 40.0

########################################
#       ----- UNUSED CODE ------       #
# USED TO ACCESS SALESFORCE TABLE DATA #
########################################


def get_number_of_rows(driver):
    """
    Get the number of row in the table ie. the number of accounts
    :param driver:  The webdriver instance
    :return: The number of rows
    """
    
    sleeper.sleep(0.5)
    
    print 'Finding the number of accounts on page...'

    xpath = '//*[@class="listBody"]/div[4]/div/div/div/div[1]/div[2]/div/*'
    WebDriverWait(driver, WAIT_TIME).until(ec.presence_of_element_located((By.XPATH, xpath)))
    num_rows = len(driver.find_elements_by_xpath(xpath))
    
    print '%d accounts were found on page' % num_rows
    
    return num_rows


def get_row_username(driver, row):
    """
    Get the username in row 'row'
    :param driver:  The webdriver instance
    :param row: The row number to check
    :return: The username of the row
    """
    
    print 'Getting row %d status...' % row
    xpath = '//*[@class="listBody"]/div[4]/div/div/div/div[1]/div[2]/div/div[%d]/table/tbody/tr/td[12]/div' % row
    username = WebDriverWait(driver, WAIT_TIME).until(ec.presence_of_element_located((By.XPATH, xpath))).text
    
    print 'The username found is: %s' % username
    
    return username
    
    
def click_on_row_link(driver, row):
    """
    Clicks on the link that opens the details user info screen
    :param driver: The webdriver instance
    :param row: The row to click in
    :return: None
    """

    print 'Pressing row %d link...' % row
    xpath = '//*[@class="listBody"]/div[4]/div/div/div/div[1]/div[2]/div/div[%d]/table/tbody/tr/td[5]/div/a' % row
    link = WebDriverWait(driver, WAIT_TIME).until(ec.presence_of_element_located((By.XPATH, xpath)))
    
    sleeper.sleep(0.5)

    link.click()
    

def get_assigned_details(driver):
    """
    Gets the username and password of the user
    :param driver: The webdriver instance
    :return: The username and password
    """

    print 'Getting username...'

    xpath = '//*[@id="ep"]/div[2]/div[4]/table/tbody/tr[1]/td[4]/div'
    username = WebDriverWait(driver, WAIT_TIME).until(ec.presence_of_element_located((By.XPATH, xpath))).text
    
    xpath = '//*[@id="ep"]/div[2]/div[6]/table/tbody/tr[5]/td[4]/div'
    password = WebDriverWait(driver, WAIT_TIME).until(ec.presence_of_element_located((By.XPATH, xpath))).text
    
    print 'Username found: %s' % username
    print 'Password found: %s' % ('*' * len(password))
    
    return username, password

########################
# ------- START ------ #
########################


def get_driver(incognito=False):
    """
    Get a FireFox webdriver instance
    :param incognito: Should an incognito window be used - Does not seem to work at this time
    :return: A webdriver instance
    """
    
    # Disabled this since it keeps opening new windows at a specific point
    # Rather have tabs open that entire new windows
    # And in any way, when closing a driver instance entire cache and history is wiped. New one is always fresh
    # if incognito:
    #     print "Initializing incognito webdriver"
    #
    #     firefox_profile = webdriver.FirefoxProfile()
    #     firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
    #
    #     driver = webdriver.Firefox(firefox_profile=firefox_profile)
    # else:

    print "Initializing the webdriver"
    
    driver = webdriver.Firefox()
    
    return driver


def close_driver(driver):
    """
    Stop the webdriver and close all web browser windows
    :return: None
    """
    
    print 'Closing and quiting...'
    
    driver.close()
    driver.quit()
    
    
def go_back(driver):
    """
    Goes back one page
    :param driver: The webdriver instance
    :return: None
    """

    sleeper.sleep(0.5)

    driver.execute_script("window.history.go(-1)")


def login(driver, username, password):
    """
    Logs you in
    :param driver:  The webdriver instance
    :param username: The username to login with
    :param password: The password to login with
    :return: None
    """
    
    # Enter the login username
    username_field = WebDriverWait(driver, WAIT_TIME).until(ec.visibility_of_element_located((By.ID, "username")))
    username_field.send_keys(username)
    
    sleeper.sleep(0.5)
    
    # Enter the login password
    password_field = WebDriverWait(driver, WAIT_TIME).until(ec.presence_of_element_located((By.ID, "password")))
    password_field.send_keys(password)

    sleeper.sleep(0.5)

    # Press the login button
    button = WebDriverWait(driver, WAIT_TIME).until(ec.presence_of_element_located((By.ID, "Login")))
    button.click()
    
    sleeper.sleep(7.5)
    
    # Check that the login worked
    error = None
    try:
        error = WebDriverWait(driver, 10.0).until(ec.presence_of_element_located((By.ID, "error")))
    except:
        return
    
    if error is not None and "still can't log in" in error.text:
        raise Exception("Could not log in for some reason")


def print_fails(fails):
    """
    
    :param fails:
    :return:
    """

    from pprint import pprint
    
    # Write to a log file
    with open("error.log", "w") as f:
        pprint(fails, f)
    
    print 'The following accounts failed for some reason'
    pprint(fails)
    

def do_first_login(driver, username, new_password, current_password, community, url):
    """
    The first login for the newly created user. This uses the tmp_password. This sets the user's password to the one they
    suggested in the first place
    :param driver:
    :param username: The username to login with
    :param new_password:
    :param current_password: The password to login with - The tmp_password
    :param community:
    :param url: The URL to the login page
    :return: None
    """

    driver.get(url)

    login(driver, username, current_password)
    
    sleeper.sleep(1.0)
    
    print 'Entering the current password...'
    
    # Enter the required fields
    # Enter the current password
    current_password_field = WebDriverWait(driver, WAIT_TIME).until(ec.presence_of_element_located((By.ID, "currentpassword")))
    current_password_field.send_keys(current_password)

    sleeper.sleep(0.75)
    
    print 'Entering the new password...'

    # Enter the new password
    new_password_field = WebDriverWait(driver, WAIT_TIME).until(ec.presence_of_element_located((By.ID, "newpassword")))
    new_password_field.send_keys(new_password)

    sleeper.sleep(0.75)
    
    print 'Entering the new password again...'

    # Confirm the new password
    confirm_password_field = WebDriverWait(driver, WAIT_TIME).until(ec.presence_of_element_located((By.ID, "confirmpassword")))
    confirm_password_field.send_keys(new_password)
    
    sleeper.sleep(0.75)
    
    print 'Entering the community name as answer...'
    
    # Enter the community name
    answer_field = WebDriverWait(driver, WAIT_TIME).until(ec.presence_of_element_located((By.ID, "answer")))
    answer_field.send_keys(community)
    
    sleeper.sleep(1.25)
    
    print 'Pressing the button...'
    
    # Press the button
    button = WebDriverWait(driver, WAIT_TIME).until(ec.presence_of_element_located((By.ID, "password-button")))
    button.click()
    
    # close_popup(driver)

    sleeper.sleep(12.5)
    
    print 'Waiting time over... Closing browser'

    close_driver(driver)
    
    
def do_second_login(driver, username, password, url):
    """
    The second login for the newly created user. This sets so that the cellphone something:
    :param driver:
    :param username: The username to login with
    :param password: The password to login with
    :param url: The URL to the login page
    :return: None
    """

    driver.get(url)

    login(driver, username, password)

    sleeper.sleep(5.0)
    
    # Press the don't register text
    text = WebDriverWait(driver, WAIT_TIME).until(ec.presence_of_element_located((By.LINK_TEXT, "I Don't Want to Register My Phone")))
    driver.execute_script("arguments[0].click();", text)

    sleeper.sleep(12.5)

    print 'Waiting time over... Closing browser'
    
    close_driver(driver)
    
    
def close_popup(driver):
    """
    
    :param driver:
    :return: None
    """
    
    try:
        print 'Checking the checkbox...'
        
        # Click the checkbox
        checkbox = WebDriverWait(driver, WAIT_TIME).until(ec.presence_of_element_located((By.ID, "14:13;a")))
        checkbox.click()
        
        print 'Pressing the X button on the popup...'
        # Press the 'X' on the popup
        WebDriverWait(driver, WAIT_TIME).until(ec.presence_of_element_located((By.CLASS_NAME, "icon-fallback-text forceIcon")))
        xs = driver.find_elements_by_class_name("icon-fallback-text forceIcon")
        
        print len(xs)
        
        # xs[1].click()
    except Exception as e:
        if PRINT_EXCEPTIONS:
            print e
        else:
            print 'Something went wrong with closing the popup...'
    
    
def ask_credentials():
    """
    Ask the user for the temp password
    :return: The password
    """
    tmp_password = raw_input('Please enter the temp password: ')
    
    return tmp_password


def main():
    """
    Main method
    :return: None
    """
    
    fails = {}

    if ASK_CREDENTIALS:
        print 'No secrets.py file found, asking credentials:'
        _tmp_password = ask_credentials()
    else:
        _tmp_password = secrets.TMP_PASSWORD
    
    url = "https://eu5.salesforce.com/a0l?fcf=00B24000004ysrt"
    
    # parsed_accounts = parse_xml()
    parsed_accounts = parse_csv()
    num_accounts = len(parsed_accounts)

    for i in xrange(0, num_accounts):
        print 'Working with user: %s' % parsed_accounts[i][0]
        
        driver = None
        
        try:
            driver = get_driver(incognito=True)
            do_first_login(driver, parsed_accounts[i][0], parsed_accounts[i][1], _tmp_password, parsed_accounts[i][2], url)
            driver = None

            driver = get_driver(incognito=True)
            do_second_login(driver, parsed_accounts[i][0], parsed_accounts[i][1], url)
            driver = None
        except Exception as e:
            fails[parsed_accounts[i][0]] = [[parsed_accounts[i][0], '*' * len(parsed_accounts[i][1]), parsed_accounts[i][2], e.message]]
            
            if PRINT_EXCEPTIONS:
                print e
            else:
                print 'Something went wrong during execution... Moving on to next account'

        if driver is not None:
            try:
                close_driver(driver)
            except Exception as ex:
                if PRINT_EXCEPTIONS:
                    print ex
                else:
                    print 'Something went wrong with closing browser... Moving on to next account'

    if len(fails) > 0:
        print_fails(fails)

    print '=========='
    print 'Bye Bye :)'


def parse_xml():
    """
    Parse the accounts.xml file
    :return: A list of structure [[uesrname1, password1, community1], [username2, password2, community2]]
    """

    import os
    import sys

    import xml.etree.ElementTree
    
    if not os.path.exists(sys.path[0] + '/accounts.xml'):
        print 'The accounts.xml file does not exists. Exiting'
        exit()
    
    try:
        print "Parsing the accounts.xml file..."
    
        # List containing the username, password and community
        parsed_accounts = []
    
        e = xml.etree.ElementTree.parse(sys.path[0] + '/accounts.xml').getroot()
    
        accounts = e.findall('account')
        for account in accounts:
            username = str(account.get('username'))
            password = str(account.get('password'))
            community = str(account.get('community'))
        
            parsed_accounts.append([username, password, community])
    
        return parsed_accounts
    except Exception as e:
        print 'Something went wrong with parsing XML file. Exiting'
        raise e
    

def parse_csv():
    """
    Parse the CSV file
    :return: A list of structure [[username1, password1, community1], [username2, password2, community2]]
    """
    
    import os
    import sys
    import csv
    
    if not os.path.exists(sys.path[0] + '/test.csv'):
        print 'The test.csv file does not exists. Exiting'
        exit()
    
    try:
        print "Parsing the text.csv file..."

        # List containing the username, password and community
        parsed_accounts = []

        heading = True

        username_index = -1
        password_index = -1
        community_index = -1

        with open('test.csv', 'r') as f:
            reader = csv.reader(f)
        
            for row in reader:
                # print row
            
                if heading:
                    heading = False
                
                    username_index = row.index("Username")
                    password_index = row.index("Password")
                    community_index = row.index("Community")
                else:
                    parsed_accounts.append([row[username_index], row[password_index], row[community_index]])
                    # mappings.append([row[username_index]])
                
            # print parsed_accounts
    
        return parsed_accounts
    except Exception as e:
        print 'Something went wrong with parsing CSV file. Exiting'
        raise e

if __name__ == '__main__':
    main()
    # parse_csv()
