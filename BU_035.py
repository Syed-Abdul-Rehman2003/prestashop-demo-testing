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

        # Navigate to the contact page (containing newsletter form)
        print("Navigating to contact page...")
        driver.get("https://silly-friend.demo.prestashop.com/en/contact-us")
        driver.maximize_window()

        # Wait for page to load
        wait = WebDriverWait(driver, 20)
        print("Waiting for page to be fully loaded...")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(1)  # Brief pause for JavaScript rendering

        # Fill newsletter form
        # Email
        print("Entering email...")
        email = "chatgpt@leverify.com"  # Unique email, consistent with previous scripts
        try:
            email_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='email'][aria-labelledby='block-newsletter-label']")))
            email_input.send_keys(email)
            print("Email entered using specific newsletter locator.")
        except Exception as e:
            print(f"Specific email locator failed: {e}")
            # Fallback: Try generic name='email'
            email_input = wait.until(EC.presence_of_element_located((By.NAME, "email")))
            email_input.send_keys(email)
            print("Email entered using name='email' fallback.")

        # Submit form
        print("Submitting newsletter form...")
        try:
            submit_button = wait.until(EC.element_to_be_clickable((By.NAME, "submitNewsletter")))
            submit_button.click()
            print("Form submitted using name='submitNewsletter'.")
        except Exception as e:
            print(f"Submit button click failed with name='submitNewsletter': {e}")
            # Fallback: Try class-based locator
            try:
                submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.btn.btn-primary.float-xs-right.hidden-xs-down")))
                submit_button.click()
                print("Form submitted using class='btn btn-primary float-xs-right hidden-xs-down'.")
            except Exception as e2:
                print(f"Fallback submit button click failed: {e2}")
                # Fallback: JavaScript click
                driver.execute_script("arguments[0].click();", submit_button)
                print("Form submitted using JavaScript click.")

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