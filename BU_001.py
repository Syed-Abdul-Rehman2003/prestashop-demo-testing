import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class RegistrationValidTest(unittest.TestCase):
    def setUp(self):
        options = Options()
        options.add_argument('--ignore-certificate-errors')
        service = Service(r"C:\Windows\WebDriver\msedgedriver.exe")
        self.driver = webdriver.Edge(service=service, options=options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 30)
        self.driver.get("https://demo.prestashop.com/#/en/front")

    def tearDown(self):
        print("Closing browser...")
        time.sleep(2)
        self.driver.quit()

    def navigate_to_registration(self):
        driver = self.driver
        wait = self.wait

        # Wait for iframe and switch to it
        iframe = wait.until(EC.presence_of_element_located((By.ID, "framelive")))
        driver.switch_to.frame(iframe)

        # Click "Sign in"
        sign_in = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".user-info a")))
        sign_in.click()

        # Click "No account? Create one here"
        create_one = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-link-action='display-register-form']")))
        create_one.click()

        # Wait for registration form to appear
        wait.until(EC.visibility_of_element_located((By.ID, "customer-form")))

    def fill_registration_form(self, firstname, lastname, email, password, birthdate):
        driver = self.driver

        # Select gender
        gender_label = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='field-id_gender-1']")))
        gender_label.click()

        # Fill fields
        driver.find_element(By.NAME, "firstname").send_keys(firstname)
        driver.find_element(By.NAME, "lastname").send_keys(lastname)
        driver.find_element(By.NAME, "email").send_keys(email)
        driver.find_element(By.NAME, "password").send_keys(password)

        # Set birthdate using JS (input is often readonly)
        bday = driver.find_element(By.NAME, "birthday")
        driver.execute_script("arguments[0].value = arguments[1];", bday, birthdate)

        # Check required checkboxes
        for name in ["customer_privacy", "psgdpr"]:
            checkbox = driver.find_element(By.NAME, name)
            if not checkbox.is_selected():
                driver.execute_script("arguments[0].click();", checkbox)

        # Optional checkboxes
        for name in ["optin", "newsletter"]:
            try:
                checkbox = driver.find_element(By.NAME, name)
                driver.execute_script("arguments[0].click();", checkbox)
            except:
                pass  # Ignore if not found

        # Submit
        driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary.form-control-submit").click()
        time.sleep(3)

    def test_register_with_valid_details(self):
        """Test Case BU_001: Verify that a user can register with valid details"""
        self.navigate_to_registration()
        self.fill_registration_form(
            firstname="John",
            lastname="Doe",
            email="testuser1@example.com",
            password="Test@12345678!2ZxDe&890",
            birthdate="05/31/1990"
        )

        # Check if account created — look for user name on top bar
        welcome_name = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".account span")))
        self.assertIn("John", welcome_name.text)
        print("Account created successfully with name:", welcome_name.text)


if __name__ == '__main__':
    unittest.main()
