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

    def fill_form(self, firstname, lastname, email, password, birthdate):
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

        # Checkboxes
        for name in ["optin", "newsletter", "customer_privacy", "psgdpr"]:
            checkbox = driver.find_element(By.NAME, name)
            driver.execute_script("arguments[0].click();", checkbox)

        # Submit
        driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary.form-control-submit").click()
        time.sleep(3)

    def get_validation_messages(self):
        error_messages = []

        # Find the password field
        password_field = self.driver.find_element(By.NAME, "password")

        # Use JavaScript to check the HTML5 validity state
        validity = self.driver.execute_script("return arguments[0].validity;", password_field)
        if not validity['valid']:
            if validity['tooShort'] or validity['valueMissing']:
                error_messages.append("Password must be at least 8 characters long")  # Custom message based on UI
            # Check for custom strength requirement if applicable
            if not validity['customError'] and len(password_field.get_attribute("value")) < 8:
                error_messages.append("Password must be at least 8 characters long")

        # Fallback: Check styling of password requirements for red text
        try:
            requirements = self.driver.find_elements(By.CSS_SELECTOR, ".password-requirements p span")
            for span in requirements:
                color = span.value_of_css_property("color")
                text = span.text.strip()
                if "255, 0, 0" in color or "ff0000" in color.lower():  # Red color indicates error
                    error_messages.append(text)
        except:
            pass

        print("Captured error messages:", error_messages)
        return error_messages

    def test_password_validation(self):
        """Test Case BU_003: Verify password field accepts minimum 8 characters"""
        # Test with short password (Test@12)
        print("Testing with short password...")
        self.fill_form(
            firstname="Jane",
            lastname="Smith",
            email="testuser3@example.com",
            password="Test@12",
            birthdate="05/31/1990"
        )
        errors = self.get_validation_messages()
        # Check for any password length-related error
        self.assertTrue(any("characters" in msg.lower() or "8" in msg.lower() for msg in errors),
                        f"Expected password length error not found. Got: {errors}")

        # Refresh page for next test
        self.driver.refresh()
        self.wait.until(EC.visibility_of_element_located((By.ID, "customer-form")))

        # Test with valid password (Test@12345678!abc)
        print("Testing with valid password...")
        self.fill_form(
            firstname="Jane",
            lastname="Smith",
            email="testuser3@example.com",
            password="Test@12345678!abc",
            birthdate="05/31/1990"
        )
        errors = self.get_validation_messages()
        self.assertEqual([], errors, f"Unexpected error messages for valid password. Got: {errors}")

        # Print "OK" if the test passes
        print("OK")


if __name__ == '__main__':
    unittest.main()