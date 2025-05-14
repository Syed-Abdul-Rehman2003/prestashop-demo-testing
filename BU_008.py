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

        # Fill fields
        driver.find_element(By.NAME, "firstname").send_keys(firstname)
        driver.find_element(By.NAME, "lastname").send_keys(lastname)
        driver.find_element(By.NAME, "email").send_keys(email)
        driver.find_element(By.NAME, "password").send_keys(password)
        bday = driver.find_element(By.NAME, "birthday")
        driver.execute_script("arguments[0].value = arguments[1];", bday, birthdate)

        # Checkboxes
        for name in ["optin", "newsletter", "customer_privacy", "psgdpr"]:
            checkbox = driver.find_element(By.NAME, name)
            driver.execute_script("arguments[0].click();", checkbox)

        # Submit
        driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary.form-control-submit").click()
        time.sleep(3)

    def test_password_visibility_toggle(self):
        """Test Case: Verify that the password visibility toggle works."""
        password = "Test@12!abcdefghij!"
        self.driver.get("https://disastrous-paper.demo.prestashop.com/en/registration")

        # Wait for password field and toggle button
        password_field = self.wait.until(EC.visibility_of_element_located((By.NAME, "password")))
        toggle_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-action='show-password']")))

        # Step 1: Enter password
        password_field.send_keys(password)
        time.sleep(1)

        # Step 2: Click toggle to show password
        toggle_button.click()
        time.sleep(1)

        # Check input type is now "text"
        input_type_after_show = password_field.get_attribute("type")
        self.assertEqual(input_type_after_show, "text", "Password should be visible (input type=text) after clicking 'Show'")

        # Step 3: Click toggle again to hide password
        toggle_button.click()
        time.sleep(1)

        # Check input type is now "password"
        input_type_after_hide = password_field.get_attribute("type")
        self.assertEqual(input_type_after_hide, "password", "Password should be hidden (input type=password) after clicking 'Hide'")

if __name__ == '__main__':
    unittest.main()
