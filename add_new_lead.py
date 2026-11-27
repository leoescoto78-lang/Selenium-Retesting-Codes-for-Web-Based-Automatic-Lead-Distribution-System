
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException,
    WebDriverException,
)
from selenium.webdriver.common.keys import Keys

# ==========================================
# TC-LEADGEN-01: ADD A NEW LEAD
# ==========================================

EMAIL = "leoescoto78@gmail.com"
PASSWORD = "abc123!"

LEAD_NAME = "Dela Crey, Emmanuelies A."
LEAD_TYPE = "Schools"
PHONE = "0412345609"
STREET = "Baliko Test Street"
CITY = "San Fernando"
POSTCODE = "2000"
LEAD_EMAIL = "emmanuelies32@gmail.com"

WEBSITE = "https://sortrleaddistribution-client.onrender.com/"

# ==========================================
# STEP 1: OPEN CHROME
# ==========================================

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--force-device-scale-factor=1")
options.add_argument("--disable-backgrounding-occluded-windows")
options.add_argument("--disable-renderer-backgrounding")

driver = webdriver.Chrome(options=options)
driver.maximize_window()

wait = WebDriverWait(driver, 60)

try:

    print("TC-LEADGEN-01: ADD A NEW LEAD")
    print("-----------------------------------")

    # ==========================================
    # STEP 2: OPEN WEBSITE
    # ==========================================

    driver.get(WEBSITE)
    print("Website opened.")

    # ==========================================
    # STEP 3: ENTER EMAIL
    # ==========================================

    email_field = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input[type="email"]')
        )
    )

    email_field.send_keys(EMAIL)
    print("Email entered.")

    # ==========================================
    # STEP 4: ENTER PASSWORD
    # ==========================================

    password_field = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input[type="password"]')
        )
    )

    password_field.send_keys(PASSWORD)
    print("Password entered.")

    # ==========================================
    # STEP 5: CLICK LOG IN
    # ==========================================

    login_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[normalize-space()='Log In']")
        )
    )

    login_button.click()
    print("Log In button clicked.")

    # ==========================================
    # STEP 6: WAIT FOR DASHBOARD
    # ==========================================

    wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[normalize-space()='DASHBOARD']")
        )
    )

    print("Login successful.")

    # ==========================================
    # STEP 7: OPEN ADD NEW LEAD
    # ==========================================

    add_lead_link = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//*[normalize-space()='Add New Lead']")
        )
    )

    add_lead_link.click()
    print("Add New Lead page opened.")

    # ==========================================
    # STEP 8: ENTER LEAD NAME
    # ==========================================

    name_field = wait.until(
        EC.visibility_of_element_located(
            (By.NAME, "name")
        )
    )

    name_field.send_keys(LEAD_NAME)
    print("Lead name entered.")

    # ==========================================
    # STEP 9: SELECT LEAD TYPE
    # ==========================================

    print(f"Selecting Lead Type: {LEAD_TYPE}...")

    type_dropdown = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '[role="combobox"]')
        )
    )

    type_dropdown.click()
    print("Dropdown opened.")

    option_locator = (
        By.CSS_SELECTOR,
        f'li[role="option"][data-value="{LEAD_TYPE}"]'
    )

    type_option = wait.until(
        EC.presence_of_element_located(option_locator)
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        type_option
    )

    try:

        wait.until(
            EC.element_to_be_clickable(option_locator)
        ).click()

    except ElementClickInterceptedException:

        print("Option click intercepted. Using JavaScript click.")

        type_option = wait.until(
            EC.presence_of_element_located(option_locator)
        )

        driver.execute_script(
            "arguments[0].click();",
            type_option
        )

    # VERIFY SELECTED TYPE

    wait.until(
        lambda d: (
            LEAD_TYPE
            in [
                element.get_attribute("data-value")
                for element in d.find_elements(
                    By.CSS_SELECTOR,
                    '[role="option"][aria-selected="true"]'
                )
            ]
            or LEAD_TYPE
            in [
                element.get_attribute("value")
                for element in d.find_elements(
                    By.CSS_SELECTOR,
                    '[role="combobox"]'
                )
            ]
            or any(
                LEAD_TYPE in (element.text or "")
                for element in d.find_elements(
                    By.CSS_SELECTOR,
                    '[role="combobox"]'
                )
            )
        )
    )

    print(f"Lead type selected: {LEAD_TYPE}.")

    # ==========================================
    # STEP 10: ENTER PHONE NUMBER
    # ==========================================

    phone_field = wait.until(
        EC.visibility_of_element_located(
            (By.NAME, "phonenumber")
        )
    )

    phone_field.send_keys(PHONE)
    print("Phone number entered.")

    # ==========================================
    # STEP 11: ENTER STREET ADDRESS
    # ==========================================

    street_field = wait.until(
        EC.visibility_of_element_located(
            (By.NAME, "streetaddress")
        )
    )

    street_field.send_keys(STREET)
    print("Street address entered.")

    # ==========================================
    # STEP 12: ENTER CITY
    # ==========================================

    city_field = wait.until(
        EC.visibility_of_element_located(
            (By.NAME, "city")
        )
    )

    city_field.send_keys(CITY)
    print("City entered.")

    # ==========================================
    # STEP 13: ENTER POSTCODE
    # ==========================================

    postcode_field = wait.until(
        EC.visibility_of_element_located(
            (By.NAME, "postcode")
        )
    )

    postcode_field.send_keys(POSTCODE)
    print("Postcode entered.")

    # ==========================================
    # STEP 14: ENTER LEAD EMAIL
    # ==========================================

    lead_email_field = wait.until(
        EC.visibility_of_element_located(
            (By.NAME, "emailaddress")
        )
    )

    lead_email_field.send_keys(LEAD_EMAIL)
    print("Lead email entered.")

    print("Lead form completed.")

    # ==========================================
    # STEP 15: SUBMIT FORM
    # ==========================================

    submit_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'button[type="submit"]')
        )
    )

    submit_button.click()
    print("Submit button clicked.")

    # ==========================================
    # STEP 16: CHECK SUCCESS MESSAGE
    # ==========================================

    print("Waiting for success message...")

    success_locator = (
        By.XPATH,
        "//*[normalize-space()='New lead added!']"
    )

    try:

        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located(success_locator)
        )

        print("-----------------------------------")
        print("SUCCESS CONFIRMATION: PASSED")
        print("Success message: New lead added!")
        print(f"Lead submitted: {LEAD_NAME}")
        print("-----------------------------------")

    except TimeoutException:

        print("-----------------------------------")
        print("Success message was not detected.")
        print("Proceeding to verify the Leads page.")
        print("-----------------------------------")

    # ==========================================
    # STEP 17: OPEN LEADS PAGE
    # ==========================================

    print("Opening Leads page...")

    leads_link = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//li[contains(@class,'ps-menuitem-root')]"
                "[.//*[normalize-space()='Leads']]"
            )
        )
    )

    leads_link.click()
    print("Leads page opened.")

    # ==========================================
    # STEP 18: VERIFY CREATED LEAD
    # ==========================================

    print("Searching for the new lead...")

    created_lead = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located(
            (By.XPATH, f"//*[normalize-space()='{LEAD_NAME}']")
        )
    )

    if created_lead.is_displayed():

        print("-----------------------------------")
        print("TEST RESULT: PASS")
        print(f"Verified lead: {LEAD_NAME}")
        print("The newly created lead appeared")
        print("on the Leads page.")
        print("-----------------------------------")

# ==========================================
# ERROR HANDLING
# ==========================================

except TimeoutException:

    print("-----------------------------------")
    print("TEST EXECUTION ERROR")
    print("A required element did not appear in time.")
    print("Check the last progress message above.")

    try:
        print("Current URL:", driver.current_url)
    except WebDriverException:
        print("Chrome session is no longer available.")

    print("-----------------------------------")

except WebDriverException as error:

    print("-----------------------------------")
    print("TEST EXECUTION ERROR")
    print("A browser/WebDriver error occurred:")
    print(error)

    try:
        print("Current URL:", driver.current_url)
    except WebDriverException:
        print("Chrome session disconnected.")

    print("-----------------------------------")

except Exception as error:

    print("-----------------------------------")
    print("TEST EXECUTION ERROR")
    print("An unexpected error occurred:")
    print(error)
    print("-----------------------------------")

# ==========================================
# STEP 19: CLOSE BROWSER
# ==========================================

finally:

    try:

        input("\nPress Enter to close the browser...")

    except Exception:
        pass

    try:

        driver.quit()

    except Exception:
        pass

