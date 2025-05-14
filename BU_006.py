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
        self.driver.get("https://disastrous-paper.demo.prestashop.com/en/registration")
        self.wait.until(EC.visibility_of_element_located((By.ID, "customer-form")))

    def tearDown(self):
        print("Closing browser...")
        time.sleep(2)
        self.driver.quit()

    def fill_form(self, firstname, lastname, email, password, birthdate):
        driver = self.driver

        # Select gender
        gender_label = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='field-id_gender-1']")))
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
        error_elements = self.driver.find_elements(By.CSS_SELECTOR, ".form-control-comment")
        all_messages = [el.text.strip() for el in error_elements if el.text.strip()]
        
        # Filter only actual error messages (customize if needed)
        filtered_messages = [
            msg for msg in all_messages
            if "allowed" in msg or "Invalid" in msg
        ]
    
        print("Captured error messages:", filtered_messages)
        return filtered_messages
    
    

    def test_invalid_name_fields(self):
        """Negative test: Invalid first and last name should show error messages"""
        self.fill_form(
            firstname="123",  # invalid
            lastname="@@@",   # invalid
            email="valid@gmail.com",
            password="Test@12!abcdefghest@124!Dex*()",
            birthdate="05/31/1990"
        )
        errors = self.get_validation_messages()
        self.assertIn("Only letters and the dot (.) character, followed by a space, are allowed.", errors, f"Expected format error not found. Got: {errors}")


if __name__ == '__main__':
    unittest.main()
