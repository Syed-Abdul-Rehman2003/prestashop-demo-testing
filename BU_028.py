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

def test_valid_filter_and_clear():
    """Test clicking 'Men' filter link, verifying product list, and clearing filters."""
    driver = setup_driver()
    wait = WebDriverWait(driver, 20)
    try:
        print("Navigating to clothes category page...")
        driver.get("https://typical-land.demo.prestashop.com/en/3-clothes")
        driver.maximize_window()

        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(1)

        print("Clicking 'Men' category filter link...")
        men_filter_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='q=Categories-Men'].js-search-link")))
        men_filter_link.click()

        print("Verifying filter application...")
        wait.until(EC.url_contains("q=Categories-Men"))
        assert "q=Categories-Men" in driver.current_url, \
            f"URL did not update with Men filter. Expected: q=Categories-Men, Got: {driver.current_url}"

        print("Verifying product list update...")
        products = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product")))
        assert len(products) > 0, "No products displayed after applying Men filter."
        for product in products:
            product_title = product.find_element(By.CSS_SELECTOR, ".product-title").text.lower()
            assert "men" in product_title or "hummingbird" in product_title, \
                f"Product '{product_title}' does not appear to be in Men category."

        print("Clicking 'Clear all' button...")
        clear_all_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.js-search-filters-clear-all")))
        clear_all_button.click()

        print("Verifying filter reset...")
        wait.until(EC.url_to_be("https://typical-land.demo.prestashop.com/en/3-clothes"))
        assert "q=Categories-Men" not in driver.current_url, \
            f"URL did not reset after clearing filters. Got: {driver.current_url}"
        products_after_clear = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product")))
        assert len(products_after_clear) > len(products), \
            f"Product list did not expand after clearing filters. Got: {len(products_after_clear)} products."

        print("Valid filter and clear test passed: Men filter applied, products updated, and filters cleared.")

    except Exception as e:
        print(f"Valid filter and clear test failed: {e}")
        traceback.print_exc()
        raise
    finally:
        print("Closing browser for valid filter and clear test...")
        driver.quit()

def test_invalid_filter():
    """Test navigating to an invalid filter URL and verify handling."""
    driver = setup_driver()
    wait = WebDriverWait(driver, 20)
    try:
        print("Navigating to clothes category page with invalid filter...")
        invalid_filter_url = "https://typical-land.demo.prestashop.com/en/3-clothes?q=Categories-NonExistent"
        driver.get(invalid_filter_url)
        driver.maximize_window()

        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(1)

        print("Verifying product list or empty state...")
        try:
            products = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product")))
            assert len(products) > 0, "Products displayed for invalid filter, expected none or reset."
            print("Invalid filter test passed: Product list reset to all products.")
        except:
            empty_message = driver.find_elements(By.CSS_SELECTOR, ".no-products")
            if empty_message:
                assert "no products" in empty_message[0].text.lower(), "Expected empty product message."
                print("Invalid filter test passed: No products message displayed.")
            else:
                raise AssertionError("Neither products nor empty message displayed for invalid filter.")

    except Exception as e:
        print(f"Invalid filter test failed: {e}")
        traceback.print_exc()
        raise
    finally:
        print("Closing browser for invalid filter test...")
        driver.quit()

if __name__ == '__main__':
    try:
        print("Running valid filter and clear test...")
        test_valid_filter_and_clear()
        print("\nRunning invalid filter test...")
        test_invalid_filter()
    except Exception as e:
        print("One or more tests failed:", e)
    print("All tests completed.")