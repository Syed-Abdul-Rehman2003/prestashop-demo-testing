import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
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

    def tearDown(self):
        print("Closing browser...")
        time.sleep(2)
        self.driver.quit()

    def test_forgot_password_redirection(self):
        """Test Case BU_009: Verify that the 'Forgot Password' link redirects to the password reset page."""
        driver = self.driver
        driver.get("https://stupendous-lunch.demo.prestashop.com/en/login?back=https%3A%2F%2Fstupendous-lunch.demo.prestashop.com%2Fen%2F%3Fid_module_showcased%3Dundefined")
        
        # Step 1: Wait for the sign-in page to load
        self.assertIn("login", driver.current_url, "Sign-in page did not load as expected")

        # Step 2: Click the 'Forgot your password?' link
        forgot_password_link = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.forgot-password a"))
        )
        forgot_password_link.click()

        # Step 3: Verify redirection to the password recovery page
        self.wait.until(EC.url_contains("password-recovery"))
        current_url = driver.current_url
        self.assertIn("password-recovery", current_url, "Did not redirect to the password reset page")

        # Step 4: Check that the email input field is present
        email_field = self.wait.until(EC.visibility_of_element_located((By.NAME, "email")))
        self.assertTrue(email_field.is_displayed(), "Email input field not found on password reset page")

if __name__ == '__main__':
    unittest.main()
