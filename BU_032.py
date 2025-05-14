from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import traceback

def test_empty_fields():
    """Test submitting contact form with empty fields (TC.2)."""
    driver = setup_driver()
    wait = WebDriverWait(driver, 20)
    try:
        print("Navigating to contact form page for empty fields test...")
        driver.get("https://puzzled-fairies.demo.prestashop.com/en/contact-us")
        driver.maximize_window()

        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(1)

        print("Submitting form with empty fields...")
        submit_button = wait.until(EC.element_to_be_clickable((By.NAME, "submitMessage")))
        submit_button.click()

        print("Verifying error message for empty fields...")
        error_message = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert.alert-danger")))
        assert error_message.is_displayed(), "Error message not displayed for empty fields."
        assert "fill" in error_message.text.lower() or "required" in error_message.text.lower(), \
            f"Expected error message for missing fields, got: {error_message.text}"
        print("Empty fields test passed: Error message displayed as expected.")

    except Exception as e:
        print(f"Empty fields test failed: {e}")
        traceback.print_exc()
        raise
    finally:
        driver.quit()

def test_invalid_email():
    """Test submitting contact form with invalid email (TC.3)."""
    driver = setup_driver()
    wait = WebDriverWait(driver, 20)
    try:
        print("Navigating to contact form page for invalid email test...")
        driver.get("https://silly-friend.demo.prestashop.com/en/contact-us")
        driver.maximize_window()

        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(1)

        print("Filling form with invalid email...")
        subject_dropdown = wait.until(EC.presence_of_element_located((By.ID, "id_contact")))
        subject_dropdown.click()
        subject_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//option[contains(text(), 'Customer service')]")))
        subject_option.click()

        email = "invalid.email"
        email_input = wait.until(EC.presence_of_element_located((By.ID, "email")))
        email_input.send_keys(email)

        message = "Test message"
        message_input = wait.until(EC.presence_of_element_located((By.ID, "contactform-message")))
        message_input.send_keys(message)

        assert email_input.get_attribute("value") == email, f"Email input mismatch. Expected: {email}, Got: {email_input.get_attribute('value')}"
        assert message_input.get_attribute("value") == message, f"Message input mismatch. Expected: {message}, Got: {message_input.get_attribute('value')}"
        assert subject_option.is_selected(), "Customer service subject not selected."

        print("Submitting form with invalid email...")
        submit_button = wait.until(EC.element_to_be_clickable((By.NAME, "submitMessage")))
        submit_button.click()

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
        driver.quit()

def test_message_character_limit():
    """Test submitting contact form with message exceeding character limit (TC.9)."""
    driver = setup_driver()
    wait = WebDriverWait(driver, 20)
    try:
        print("Navigating to contact form page for character limit test...")
        driver.get("https://silly-friend.demo.prestashop.com/en/contact-us")
        driver.maximize_window()

        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(1)

        print("Filling form with oversized message...")
        subject_dropdown = wait.until(EC.presence_of_element_located((By.ID, "id_contact")))
        subject_dropdown.click()
        subject_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//option[contains(text(), 'Customer service')]")))
        subject_option.click()

        email = "chatgpt@leverify.com"
        email_input = wait.until(EC.presence_of_element_located((By.ID, "email")))
        email_input.send_keys(email)

        # Generate a message exceeding 500 characters
        message = "A" * 501
        message_input = wait.until(EC.presence_of_element_located((By.ID, "contactform-message")))
        message_input.send_keys(message)

        assert email_input.get_attribute("value") == email, f"Email input mismatch. Expected: {email}, Got: {email_input.get_attribute('value')}"
        assert len(message_input.get_attribute("value")) == 501, f"Message length mismatch. Expected: 501, Got: {len(message_input.get_attribute('value'))}"
        assert subject_option.is_selected(), "Customer service subject not selected."

        print("Submitting form with oversized message...")
        submit_button = wait.until(EC.element_to_be_clickable((By.NAME, "submitMessage")))
        submit_button.click()

        print("Verifying error message for character limit...")
        try:
            error_message = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert.alert-danger")))
            assert error_message.is_displayed(), "Error message not displayed for oversized message."
            assert "message" in error_message.text.lower() and ("long" in error_message.text.lower() or "limit" in error_message.text.lower()), \
                f"Expected character limit error message, got: {error_message.text}"
            print("Character limit test passed: Error message displayed as expected.")
        except Exception as e:
            print(f"Character limit test may have failed due to TC.9 bug (no restriction): {e}")
            # As per TC.9, the form submits successfully, which is a bug
            try:
                success_message = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert.alert-success")))
                if success_message.is_displayed():
                    raise AssertionError("Form submitted successfully with oversized message, which is incorrect behavior (TC.9 bug).")
            except:
                pass  # No success message, but no error message either
            raise AssertionError("No error message displayed for oversized message, and form may have submitted (TC.9 bug).")

    except Exception as e:
        print(f"Character limit test failed: {e}")
        traceback.print_exc()
        raise
    finally:
        driver.quit()

def setup_driver():
    """Set up and return WebDriver instance."""
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    service = Service("C:\\WebDrivers\\msedgedriver.exe")
    return webdriver.Edge(service=service, options=options)

if __name__ == '__main__':
    try:
        print("Running empty fields test...")
        test_empty_fields()
        print("\nRunning invalid email test...")
        test_invalid_email()
        print("\nRunning message character limit test...")
        test_message_character_limit()
    except Exception as e:
        print("One or more tests failed:", e)
    print("All tests completed.")