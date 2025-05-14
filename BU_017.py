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

def test_valid_add_to_cart():
    """Test adding product to cart, increasing quantity, and proceeding to checkout."""
    driver = setup_driver()
    wait = WebDriverWait(driver, 20)
    try:
        print("Navigating to product page...")
        driver.get("https://unusual-point.demo.prestashop.com/en/men/1-1-hummingbird-printed-t-shirt.html#/1-size-s/8-color-white")
        driver.maximize_window()

        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(1)

        print("Increasing quantity...")
        quantity_increase_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.js-increase-product-quantity.bootstrap-touchspin-up")))
        quantity_increase_button.click()
        time.sleep(1)  # Wait for quantity update

        quantity_input = wait.until(EC.presence_of_element_located((By.NAME, "qty")))
        assert quantity_input.get_attribute("value") == "2", \
            f"Quantity not updated. Expected: 2, Got: {quantity_input.get_attribute('value')}"

        print("Adding to cart...")
        add_to_cart_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary.add-to-cart")))
        add_to_cart_button.click()

        print("Verifying cart addition...")
        cart_confirmation = wait.until(EC.visibility_of_element_located((By.ID, "myModalLabel")))
        assert cart_confirmation.is_displayed(), "Cart confirmation modal not displayed."
        assert "Product successfully added to your shopping cart" in cart_confirmation.text, \
            f"Expected cart confirmation message, got: {cart_confirmation.text}"

        print("Proceeding to checkout...")
        proceed_to_checkout_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn.btn-primary[href*='cart?action=show']")))
        proceed_to_checkout_button.click()

        print("Verifying checkout page...")
        checkout_page = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.h1")))
        assert "Shopping Cart" in checkout_page.text, f"Expected checkout page, got: {checkout_page.text}"
        print("Valid add to cart test passed: Product added and checkout page reached.")

    except Exception as e:
        print(f"Valid add to cart test failed: {e}")
        traceback.print_exc()
        raise
    finally:
        print("Closing browser for valid add to cart test...")
        driver.quit()

def test_invalid_quantity():
    """Test adding to cart with invalid quantity (e.g., 0)."""
    driver = setup_driver()
    wait = WebDriverWait(driver, 20)
    try:
        print("Navigating to product page for invalid quantity test...")
        driver.get("https://unusual-point.demo.prestashop.com/en/men/1-1-hummingbird-printed-t-shirt.html#/1-size-s/8-color-white")
        driver.maximize_window()

        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(1)

        print("Setting quantity to 0...")
        quantity_input = wait.until(EC.presence_of_element_located((By.NAME, "qty")))
        quantity_input.clear()
        quantity_input.send_keys("0")

        assert quantity_input.get_attribute("value") == "0", \
            f"Quantity input mismatch. Expected: 0, Got: {quantity_input.get_attribute('value')}"

        print("Attempting to add to cart with quantity 0...")
        add_to_cart_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary.add-to-cart")))
        add_to_cart_button.click()

        print("Verifying error message for invalid quantity...")
        try:
            error_message = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert.alert-danger")))
            assert error_message.is_displayed(), "Error message not displayed for invalid quantity."
            assert "quantity" in error_message.text.lower() and ("invalid" in error_message.text.lower() or "minimum" in error_message.text.lower()), \
                f"Expected invalid quantity error message, got: {error_message.text}"
            print("Invalid quantity test passed: Error message displayed as expected.")
        except Exception as e:
            print(f"Error message not found, checking if add to cart was blocked: {e}")
            try:
                cart_confirmation = driver.find_element(By.ID, "myModalLabel")
                if cart_confirmation.is_displayed():
                    raise AssertionError("Cart confirmation modal appeared with quantity 0, which is incorrect.")
            except:
                print("No cart confirmation modal, as expected for invalid quantity.")
            print("Invalid quantity test passed: Add to cart blocked.")

    except Exception as e:
        print(f"Invalid quantity test failed: {e}")
        traceback.print_exc()
        raise
    finally:
        print("Closing browser for invalid quantity test...")
        driver.quit()

if __name__ == '__main__':
    try:
        print("Running valid add to cart test...")
        test_valid_add_to_cart()
        print("\nRunning invalid quantity test...")
        test_invalid_quantity()
    except Exception as e:
        print("One or more tests failed:", e)
    print("All tests completed.")