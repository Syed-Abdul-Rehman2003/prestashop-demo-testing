from selenium import webdriver
from selenium.webdriver.common.by import By
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

        # Navigate to the contact form page
        print("Navigating to contact form page...")
        driver.get("https://silly-friend.demo.prestashop.com/en/contact-us")
        driver.maximize_window()

        # Wait for page to load
        wait = WebDriverWait(driver, 20)
        print("Waiting for page to be fully loaded...")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(1)  # Brief pause for JavaScript rendering

        # Fill contact form
        # Email
        print("Entering email...")
        email = "chatgpt@leverify.com"  # Unique email, consistent with previous scripts
        email_input = wait.until(EC.presence_of_element_located((By.ID, "email")))
        email_input.send_keys(email)

        # Message
        print("Entering message...")
        message = "Hello, I have a question about your products."  # Hardcoded message
        message_input = wait.until(EC.presence_of_element_located((By.ID, "contactform-message")))
        message_input.send_keys(message)

        # Submit form
        print("Submitting contact form...")
        try:
            submit_button = wait.until(EC.element_to_be_clickable((By.NAME, "submitMessage")))
            submit_button.click()
            print("Form submitted using name='submitMessage'.")
        except Exception as e:
            print(f"Submit button click failed with name='submitMessage': {e}")
            # Fallback: Try class-based locator
            try:
                submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.btn.btn-primary")))
                submit_button.click()
                print("Form submitted using class='btn btn-primary'.")
            except Exception as e2:
                print(f"Fallback submit button click failed: {e2}")
                raise Exception("Unable to locate submit button.")

        # Wait to see result (e.g., confirmation message or redirect)
        print("Waiting for form submission result...")
        time.sleep(10)

    except Exception as e:
        print("An error occurred:", e)
        traceback.print_exc()

    finally:
        # Close the browser
        print("Closing browser...")
        driver.quit()