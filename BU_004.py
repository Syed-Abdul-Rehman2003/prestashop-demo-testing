import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class RegistrationTest(unittest.TestCase):
    def setUp(self):
        # Setup Edge driver
        options = Options()
        options.add_argument('--ignore-certificate-errors')
        service = Service(r"C:\Windows\WebDriver\msedgedriver.exe")
        self.driver = webdriver.Edge(service=service, options=options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 15)
        self.driver.get("https://purple-time.demo.prestashop.com/en/registration")
        self.wait.until(EC.visibility_of_element_located((By.ID, "customer-form")))

    def tearDown(self):
        print("Closing browser...")
        time.sleep(2)
        self.driver.quit()

    def fill_form(self, firstname, lastname, email, password, birthdate, agree_terms=True):
        driver = self.driver

        # Select gender
        gender_label = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='field-id_gender-2']")))
        gender_label.click()

        # Fill fields with TAB to trigger validation
        fname = driver.find_element(By.NAME, "firstname")
        fname.send_keys(firstname)
        fname.send_keys(Keys.TAB)

        lname = driver.find_element(By.NAME, "lastname")
        lname.send_keys(lastname)
        lname.send_keys(Keys.TAB)

        email_field = driver.find_element(By.NAME, "email")
        email_field.send_keys(email)
        email_field.send_keys(Keys.TAB)

        pwd = driver.find_element(By.NAME, "password")
        pwd.send_keys(password)
        pwd.send_keys(Keys.TAB)

        # Set birthdate using JS (this input might be readonly)
        bday = driver.find_element(By.NAME, "birthday")
        driver.execute_script("arguments[0].value = arguments[1];", bday, birthdate)

        # Checkboxes (except terms if agree_terms is False)
        for name in ["optin", "newsletter", "customer_privacy"]:
            checkbox = driver.find_element(By.NAME, name)
            driver.execute_script("arguments[0].click();", checkbox)

        # Terms and Conditions (psgdpr checkbox)
        if agree_terms:
            terms_checkbox = driver.find_element(By.NAME, "psgdpr")
            driver.execute_script("arguments[0].click();", terms_checkbox)

        # Submit
        driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary.form-control-submit").click()
        time.sleep(3)

    def get_validation_messages(self):
        error_messages = []

        # Check for terms checkbox validation error
        try:
            terms_field = self.driver.find_element(By.NAME, "psgdpr")
            # Use JavaScript to check the validity state of the checkbox
            is_invalid = self.driver.execute_script("return !arguments[0].validity.valid;", terms_field)
            if is_invalid:
                validation_message = self.driver.execute_script("return arguments[0].validationMessage;", terms_field)
                if validation_message:
                    error_messages.append(validation_message.strip())
                else:
                    # Fallback: Check for custom error message near the checkbox
                    terms_group = terms_field.find_element(By.XPATH, "./ancestor::div[contains(@class, 'form-group')]")
                    error_elements = terms_group.find_elements(By.CSS_SELECTOR, ".form-control-comment, .help-block, .invalid-feedback")
                    for el in error_elements:
                        if el.is_displayed() and el.text.strip():
                            error_messages.append(el.text.strip())
        except:
            pass

        # Also check for any general form errors after submission
        try:
            form_errors = self.driver.find_elements(By.CSS_SELECTOR, ".alert.alert-danger li")
            error_messages.extend([el.text.strip() for el in form_errors if el.text.strip() and el.is_displayed()])
        except:
            pass

        print("Captured error messages:", error_messages)
        return error_messages

    def test_terms_checkbox_validation(self):
        """Test Case BU_004: Verify registration fails if terms checkbox is not selected"""
        # Test with terms checkbox unchecked
        print("Testing with terms checkbox unchecked...")
        self.fill_form(
            firstname="Alice",
            lastname="Brown",
            email="testuser4@example.com",
            password="Test@12345678!abc",
            birthdate="05/31/1990",
            agree_terms=False
        )
        errors = self.get_validation_messages()
        expected_error = "Please check this chekcbox if you want to proceed"
        self.assertTrue(any("check" in msg.lower() and "proceed" in msg.lower() for msg in errors),
                        f"Expected terms checkbox error not found. Got: {errors}")

        # Refresh page for next test
        self.driver.refresh()
        self.wait.until(EC.visibility_of_element_located((By.ID, "customer-form")))

        # Test with terms checkbox checked
        print("Testing with terms checkbox checked...")
        self.fill_form(
            firstname="Alice",
            lastname="Brown",
            email="testuser4@example.com",
            password="Test@12345678!abc",
            birthdate="05/31/1990",
            agree_terms=True
        )
        errors = self.get_validation_messages()
        self.assertEqual([], errors, f"Unexpected error messages when terms checkbox is checked. Got: {errors}")

        # Print "OK" if the test passes
        print("OK")


if __name__ == '__main__':
    unittest.main()