from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import traceback

def setup_driver():
    """Set up and return WebDriver instance."""
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    service = Service("C:\\WebDrivers\\msedgedriver.exe")
    return webdriver.Edge(service=service, options=options)

def test_invalid_email():
    """Test submitting newsletter form with invalid email (TC.6)."""
    driver = setup_driver()
    wait = WebDriverWait(driver, 20)
    try:
        print("Navigating to contact page for invalid email test...")
        driver.get("https://puzzled-fairies.demo.prestashop.com/en/contact-us")
        driver.maximize_window()

        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(1)

        print("Entering invalid email...")
        email = "invalid.email"
        try:
            email_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='email'][aria-labelledby='block-newsletter-label']")))
            email_input.send_keys(email)
            print("Email entered using specific newsletter locator.")
        except Exception as e:
            print(f"Specific email locator failed: {e}")
            email_input = wait.until(EC.presence_of_element_located((By.NAME, "email")))
            email_input.send_keys(email)
            print("Email entered using name='email' fallback.")

        assert email_input.get_attribute("value") == email, f"Email input mismatch. Expected: {email}, Got: {email_input.get_attribute('value')}"

        print("Submitting newsletter form...")
        try:
            submit_button = wait.until(EC.element_to_be_clickable((By.NAME, "submitNewsletter")))
            submit_button.click()
            print("Form submitted using name='submitNewsletter'.")
        except Exception as e:
            print(f"Submit button click failed with name='submitNewsletter': {e}")
            try:
                submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.btn.btn-primary.float-xs-right.hidden-xs-down")))
                submit_button.click()
                print("Form submitted using class='btn btn-primary float-xs-right hidden-xs-down'.")
            except Exception as e2:
                print(f"Fallback submit button click failed: {e2}")
                driver.execute_script("arguments[0].click();", submit_button)
                print("Form submitted using JavaScript click.")

        print("Verifying error message for invalid email...")
        error_message = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert.alert-danger")))
        assert error_message.is_displayed(), "Error message not displayed for invalid email."
        assert "email" in error_message.text.lower() and "invalid" in error_message.text.lower(), \
            f"Expected invalid email error message, got: {error_message.text}"
        print("Invalid email test passed: Error message displayed as expected.")

    except Exception as e:
        print(f"Invalid email test failed: {e}")
        traceback.print_exc()
        raise
    finally:
        print("Closing browser for invalid email test...")
        driver.quit()

def test_existing_email():
    """Test submitting newsletter form with existing email (TC.5)."""
    driver = setup_driver()
    wait = WebDriverWait(driver, 20)
    try:
        print("Navigating to contact page for existing email test...")
        driver.get("https://silly-friend.demo.prestashop.com/en/contact-us")
        driver.maximize_window()

        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(1)

        print("Entering existing email...")
        email = "chatgpt@leverify.com"  # Assumed existing email from test case
        try:
            email_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='email'][aria-labelledby='block-newsletter-label']")))
            email_input.send_keys(email)
            print("Email entered using specific newsletter locator.")
        except Exception as e:
            print(f"Specific email locator failed: {e}")
            email_input = wait.until(EC.presence_of_element_located((By.NAME, "email")))
            email_input.send_keys(email)
            print("Email entered using name='email' fallback.")

        assert email_input.get_attribute("value") == email, f"Email input mismatch. Expected: {email}, Got: {email_input.get_attribute('value')}"

        print("Submitting newsletter form...")
        try:
            submit_button = wait.until(EC.element_to_be_clickable((By.NAME, "submitNewsletter")))
            submit_button.click()
            print("Form submitted using name='submitNewsletter'.")
        except Exception as e:
            print(f"Submit button click failed with name='submitNewsletter': {e}")
            try:
                submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.btn.btn-primary.float-xs-right.hidden-xs-down")))
                submit_button.click()
                print("Form submitted using class='btn btn-primary float-xs-right hidden-xs-down'.")
            except Exception as e2:
                print(f"Fallback submit button click failed: {e2}")
                driver.execute_script("arguments[0].click();", submit_button)
                print("Form submitted using JavaScript click.")

        print("Verifying error message for existing email...")
        error_message = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert.alert-danger")))
        assert error_message.is_displayed(), "Error message not displayed for existing email."
        assert "already" in error_message.text.lower() or "subscribed" in error_message.text.lower(), \
            f"Expected existing email error message, got: {error_message.text}"
        print("Existing email test passed: Error message displayed as expected.")

    except Exception as e:
        print(f"Existing email test failed: {e}")
        traceback.print_exc()
        raise
    finally:
        print("Closing browser for existing email test...")
        driver.quit()

if __name__ == '__main__':
    try:
        print("Running invalid email test...")
        test_invalid_email()
        print("\nRunning existing email test...")
        test_existing_email()
    except Exception as e:
        print("One or more tests failed:", e)
    print("All tests completed.")