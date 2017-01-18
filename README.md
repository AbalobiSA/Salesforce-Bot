# Salesforce-Bot

**<u>About</u>**

A python script that automatically changes the passwords of users on the Salesforce site.<br>
The usernames, passwords and communities for each user is set in the <b>accounts.xml</b> file.

**<u>Requirements</u>**

* Firefox 48 or higher
* <a href="https://github.com/mozilla/geckodriver/releases"><i>Geckoriver</i></a>
* Selenium 3.x
* Python 2.7 - Untested on Python 3.x

**<u>Setup</u>**

* Install Selenium:

        $ pip install -r requirements.txt
   or
   
        $ pip install selenium

* Optional: Hardcode your login details<br>
    
    Create a new file in your local repo: <b>secrets.py</b> and add the following lines, replacing the string with the temp password:
    
        TMP_PASSWORD = "tmp_password"


**<u>Usage</u>**

* Edit the <b>accounts.xml</b> file as desired, specifying the usernames, passwords and community.
* Run <b>main.py</b>.
* Enter temp password if prompt - Only if <b>secrets.py</b> was not setup
* Watch and enjoy.

***

**<u>Notes</u>**

The wait and sleep times may have to be changed depending on your internet connection and computer performance.
