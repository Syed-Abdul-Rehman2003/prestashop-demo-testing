from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import traceback

if __name__ == '__main__':
    try:
        # Set up options and driver
        options = Options()
        options.add_argument('--ignore-certificate-errors')
        service = Service("C:\\WebDrivers\\msedgedriver.exe")
        driver = webdriver.Edge(service=service, options=options)

        # Navigate to the registration page
        print("Navigating to registration page...")
        driver.get("https://silly-friend.demo.prestashop.com/en/registration")
        driver.maximize_window()

        # Wait for page to load
        wait = WebDriverWait(driver, 20)
        print("Waiting for page to be fully loaded...")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(1)  # Brief pause for JavaScript rendering

        # Fill form
        # Social title (radio buttons: 1 for Mr., 2 for Mrs.)
        gender = 1  # Hardcoded to Mr.
        print("Selecting gender...")
        try:
            # Check if radio button is present and visible
            radio_button = wait.until(EC.presence_of_element_located((By.ID, "field-id_gender-1")))
            print("Radio button found.")
            if not radio_button.is_displayed() or not radio_button.is_enabled():
                print("Radio button is not displayed or enabled.")
                raise Exception("Radio button not interactable")

            # Try standard click
            wait.until(EC.element_to_be_clickable((By.ID, "field-id_gender-1"))).click()
            print("Selected Mr. using ID locator (standard click).")
        except Exception as e:
            print(f"Standard click failed: {e}")
            try:
                # Fallback 1: Click the parent label
                label = driver.find_element(By.CSS_SELECTOR, "label[for='field-id_gender-1']")
                label.click()
                print("Selected Mr. by clicking parent label.")
            except Exception as e2:
                print(f"Label click failed: {e2}")
                # Fallback 2: JavaScript click
                driver.execute_script("arguments[0].click();", radio_button)
                print("Selected Mr. using JavaScript click.")

        # First name
        print("Entering first name...")
        first_name = "Asadullah"  # Hardcoded
        wait.until(EC.presence_of_element_located((By.ID, "field-firstname"))).send_keys(first_name)

        # Last name
        print("Entering last name...")
        last_name = "Wagan"  # Hardcoded
        driver.find_element(By.ID, "field-lastname").send_keys(last_name)

        # Email (must be unique)
        print("Entering email...")
        email = "chatgpt@leverify.com"  # Unique email using timestamp
        driver.find_element(By.ID, "field-email").send_keys(email)

        # Password
        print("Entering password...")
        password = "asad12345!"  # Hardcoded
        driver.find_element(By.ID, "field-password").send_keys(password)

        # Birthdate (optional)
        print("Entering birthdate...")
        birthdate = "05/31/1990"  # Hardcoded, or set to "" to skip
        if birthdate:
            birthdate_input = driver.find_element(By.ID, "field-birthday")
            birthdate_input.clear()
            birthdate_input.send_keys(birthdate)
            birthdate_input.send_keys(Keys.RETURN)

        # Checkboxes
        # Required: Terms and conditions
        print("Checking terms and conditions...")
        driver.find_element(By.NAME, "psgdpr").click()
        # Required: Customer data privacy
        print("Checking customer data privacy...")
        driver.find_element(By.NAME, "customer_privacy").click()

        # Optional: Newsletter
        newsletter = 1  # Hardcoded to Yes
        if newsletter == 1:
            print("Checking newsletter...")
            driver.find_element(By.NAME, "newsletter").click()

        # Optional: Partner offers
        optin = 0  # Hardcoded to No
        if optin == 1:
            print("Checking partner offers...")
            driver.find_element(By.NAME, "optin").click()

        # Submit
        print("Submitting form...")
        driver.find_element(By.CSS_SELECTOR, "button[data-link-action='save-customer']").click()

        # Wait to see result
        print("Waiting for result...")
        time.sleep(10)

        # Locate and click "Sign out" link
        print("Locating 'Sign out' link...")
        try:
            signout_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.logout")))
            print("Clicking 'Sign out' link...")
            signout_link.click()
        except Exception as e:
            print(f"Failed to click 'Sign out' link: {e}")
            # Fallback: Navigate directly to logout URL
            print("Navigating to logout URL as fallback...")
            driver.get("https://silly-friend.demo.prestashop.com/en/?mylogout=")

        # Wait to see result (e.g., redirect to login page)
        print("Waiting for logout result...")
        time.sleep(10)

        # Navigate to the login page
        print("Navigating to login page...")
        driver.get("https://silly-friend.demo.prestashop.com/en/login?back=https%3A%2F%2Fsilly-friend.demo.prestashop.com%2Fen%2F%3Fid_module_showcased%3Dundefined")
        driver.maximize_window()

        # Wait for page to load
        wait = WebDriverWait(driver, 20)
        print("Waiting for page to be fully loaded...")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(1)  # Brief pause for JavaScript rendering

        # Fill login form
        # Email (same format as registration)
        print("Entering email...")
        email = "chatgpt@leverify.com"  # Unique email using timestamp
        email_input = wait.until(EC.presence_of_element_located((By.ID, "field-email")))
        email_input.send_keys(email)

        # Password (same as registration)
        print("Entering password...")
        password = "asad12345!"  # Hardcoded
        password_input = wait.until(EC.presence_of_element_located((By.ID, "field-password")))
        password_input.send_keys(password)

        # Submit login form
        print("Submitting login form...")
        submit_button = wait.until(EC.element_to_be_clickable((By.ID, "submit-login")))
        submit_button.click()

        # Wait to see result (e.g., account page or error message)
        print("Waiting for login result...")
        time.sleep(10)

    except Exception as e:
        print("An error occurred:", e)
        traceback.print_exc()

    finally:
        # Close the browser
        print("Closing browser...")
        driver.quit()