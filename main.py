from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import argparse


ascii_art = '''
                         _                  _                _               
                        (_)                (_)              | |              
  _   _  ___  ___ ______ _ ______ _ __ ___  _ ___ ___ ______| |__   ___ _ __ 
 | | | |/ _ \/ __|______| |______| '_ ` _ \| / __/ __|______| '_ \ / _ \ '__|
 | |_| |  __/\__ \      | |      | | | | | | \__ \__ \      | | | |  __/ |   
  \__, |\___||___/      |_|      |_| |_| |_|_|___/___/      |_| |_|\___|_|   
   __/ |                                                                     
  |___/   @ https://github.com/yes-i-miss-her/facebook-auto-message    

'''

print(ascii_art)

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description='Facebook Automate messages')

# Add command-line flag options
parser.add_argument('-u', '--username', type=str, help='-u youremailaddress@gmail or phone number like -u 987654310')
parser.add_argument('-p', '--password', type=str, help='-p yourpassword')
parser.add_argument('-t', '--target', type=str, help='-t 100079483187607 or -t cid.g.4183004461801550')
parser.add_argument('-f', '--file', type=str, help='-f gail.txt give the location of your file that has messages we want to send')



# Parse the command-line arguments
args = parser.parse_args()

username = args.username
password = args.password
target = args.target
file = args.file

if 'cid' not in target:
    url = "https://mbasic.facebook.com/messages/read/?fbid=" + target + "&entrypoint=profile_message_button"
else:
    url = "https://mbasic.facebook.com/messages/read/?tid=" + target + "&surface_hierarchy=unknown"





options = Options()
options.add_argument("--headless")  # Run Chrome in headless mode
options.add_argument("--disable-gpu")  # Disable GPU acceleration
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://mbasic.facebook.com/")  # Open a website
# print(driver.page_source)  # Print the page source

time.sleep(1)

# Find the email input element by ID
email_input = driver.find_element(By.ID, 'm_login_email')
# Clear any existing value in the input field
email_input.clear()
# Enter your email into the input field
email_input.send_keys(username)

time.sleep(1)

elements = driver.find_elements(By.CSS_SELECTOR, '[name="pass"]')
password_input = elements[0]
password_input.clear()
password_input.send_keys(password)

time.sleep(1)

button = driver.find_element(By.CSS_SELECTOR, 'input[name="login"]')
button.click()

time.sleep(3)

# Get the current cookies
cookies = driver.get_cookies()
# Visit example.com/myid
driver.get(url)
# Set the cookies for example.com/myid
for cookie in cookies:
    driver.add_cookie(cookie)
# Refresh the page to ensure the cookies are applied
driver.refresh()

time.sleep(5)

with open(file) as file:
    lines = file.readlines()
for line in lines:
    # Find the email input element by ID
    message_input = driver.find_element(By.ID, 'composerInput')
    # Clear any existing value in the input field
    message_input.clear()
    # Enter your email into the input field
    message_input.send_keys(line)

    time.sleep(2)

    # Find the button element by name
    button = driver.find_element(By.NAME, 'send')

    # Click the button
    button.click()
    time.sleep(2)

time.sleep(5)


# Take screenshots
# driver.save_screenshot("screenshot.png")

# Close the browser
driver.quit()
