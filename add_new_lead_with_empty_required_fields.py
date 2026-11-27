
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
)

import time


# ==========================================
# TC-LEADGEN-02: REQUIRED FIELD VALIDATION
# ==========================================

WEBSITE = "https://sortrleaddistribution-client.onrender.com/"

EMAIL = "leoescoto78@gmail.com"
PASSWORD = "abc123!"

LEAD_NAME = "Bawanan, Bernard Angelo G."
LEAD_TYPE = "Schools"

VALID_PHONE = "0412345678"
VALID_EMAIL = "bawanan23@gmail.com"

STREET = "maharot Street"
CITY = "San Fernando"
POSTCODE = "2004"

TEST_FIELDS = ["Phone Number", "Email Address"]

results = {}


# ==========================================
# START FRESH CHROME
# ==========================================

def start_browser():

    print("\nStarting a fresh Chrome session...")

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--force-device-scale-factor=1")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 30)

    return driver, wait


# ==========================================
# LOGIN AND OPEN ADD NEW LEAD
# ==========================================

def login_and_open_form(driver, wait):

    print("\nOpening application...")

    driver.get(WEBSITE)

    print("Logging in...")

    email_field = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input[type="email"]')
        )
    )

    password_field = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input[type="password"]')
        )
    )

    email_field.clear()
    email_field.send_keys(EMAIL)

    password_field.clear()
    password_field.send_keys(PASSWORD)

    login_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[normalize-space()='Log In']")
        )
    )

    login_button.click()

    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[normalize-space()='DASHBOARD']")
        )
    )

    print("Login successful.")

    add_lead_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//*[normalize-space()='Add New Lead']")
        )
    )

    add_lead_button.click()

    wait.until(
        EC.visibility_of_element_located(
            (By.NAME, "name")
        )
    )

    print("Add New Lead form opened.")


# ==========================================
# SELECT LEAD TYPE
# ==========================================

def select_lead_type(driver, wait):

    dropdown = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "[role='combobox']")
        )
    )

    dropdown.click()

    schools_option = wait.until(
        EC.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                'li[role="option"][data-value="Schools"]'
            )
        )
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        schools_option
    )

    # Use JavaScript click to avoid dropdown overlap/interception
    driver.execute_script(
        "arguments[0].click();",
        schools_option
    )

    print("Lead Type selected: Schools.")


# ==========================================
# FILL ADD NEW LEAD FORM
# ==========================================

def fill_lead_form(field_to_leave_empty, driver, wait):

    print("\nFilling Add New Lead form...")

    name_field = wait.until(
        EC.visibility_of_element_located(
            (By.NAME, "name")
        )
    )

    name_field.clear()
    name_field.send_keys(LEAD_NAME)

    print(f"Name: {LEAD_NAME}")

    select_lead_type(driver, wait)

    # PHONE NUMBER
    phone_field = wait.until(
        EC.visibility_of_element_located(
            (By.NAME, "phonenumber")
        )
    )

    phone_field.clear()

    if field_to_leave_empty == "Phone Number":
        print("Phone Number: EMPTY")
    else:
        phone_field.send_keys(VALID_PHONE)
        print(f"Phone Number: {VALID_PHONE}")

    # STREET ADDRESS
    street_field = wait.until(
        EC.visibility_of_element_located(
            (By.NAME, "streetaddress")
        )
    )

    street_field.clear()
    street_field.send_keys(STREET)

    # CITY
    city_field = wait.until(
        EC.visibility_of_element_located(
            (By.NAME, "city")
        )
    )

    city_field.clear()
    city_field.send_keys(CITY)

    # POSTCODE
    postcode_field = wait.until(
        EC.visibility_of_element_located(
            (By.NAME, "postcode")
        )
    )

    postcode_field.clear()
    postcode_field.send_keys(POSTCODE)

    # EMAIL ADDRESS
    email_field = wait.until(
        EC.visibility_of_element_located(
            (By.NAME, "emailaddress")
        )
    )

    email_field.clear()

    if field_to_leave_empty == "Email Address":
        print("Email Address: EMPTY")
    else:
        email_field.send_keys(VALID_EMAIL)
        print(f"Email Address: {VALID_EMAIL}")

    # ==========================================
    # VERIFY TEST DATA
    # ==========================================

    print("\nVERIFYING TEST DATA...")

    if name_field.get_attribute("value") == LEAD_NAME:
        print("Name verified.")
    else:
        raise Exception("Name verification failed.")

    print("Lead Type selected.")

    if field_to_leave_empty == "Phone Number":

        if phone_field.get_attribute("value") == "":
            print("Phone Number verified as EMPTY.")
        else:
            raise Exception("Phone Number was not empty.")

    else:

        if phone_field.get_attribute("value") == VALID_PHONE:
            print("Phone Number verified.")
        else:
            raise Exception("Phone Number verification failed.")

    if field_to_leave_empty == "Email Address":

        if email_field.get_attribute("value") == "":
            print("Email Address verified as EMPTY.")
        else:
            raise Exception("Email Address was not empty.")

    else:

        if email_field.get_attribute("value") == VALID_EMAIL:
            print("Email Address verified.")
        else:
            raise Exception("Email Address verification failed.")

    if street_field.get_attribute("value") == STREET:
        print("Street verified.")
    else:
        raise Exception("Street verification failed.")

    if city_field.get_attribute("value") == CITY:
        print("City verified.")
    else:
        raise Exception("City verification failed.")

    if postcode_field.get_attribute("value") == POSTCODE:
        print("Postcode verified.")
    else:
        raise Exception("Postcode verification failed.")

    print("\nForm preparation completed.")


# ==========================================
# SUBMIT FORM
# ==========================================

def submit_form(driver, wait):

    print("\nSubmitting form...")

    submit_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'button[type="submit"]')
        )
    )

    submit_button.click()

    print("Submit button clicked.")


# ==========================================
# CHECK REQUIRED FIELD VALIDATION
# ==========================================

def check_validation_response(field_name, driver, wait):

    print("\nChecking application response...")

    time.sleep(3)

    if field_name == "Phone Number":
        field_selector = '[name="phonenumber"]'
    else:
        field_selector = '[name="emailaddress"]'

    field = driver.find_element(
        By.CSS_SELECTOR,
        field_selector
    )

    validity = driver.execute_script("""
        const field = arguments[0];

        return {
            required: field.required,
            valueMissing: field.validity.valueMissing,
            valid: field.validity.valid,
            value: field.value
        };
    """, field)

    print("\nFIELD VALIDITY:")
    print(f"Required: {validity['required']}")
    print(f"Value Missing: {validity['valueMissing']}")
    print(f"Valid: {validity['valid']}")

    # ==========================================
    # RESULT EVALUATION
    # ==========================================

    if (
        validity["required"] is True
        and validity["valueMissing"] is True
        and validity["valid"] is False
        and validity["value"] == ""
    ):

        print("\nRESULT: PASS")
        print(
            f"Submission was blocked because "
            f"{field_name} was empty."
        )

        return "PASS"

    else:

        print("\nRESULT: FAIL")
        print(
            f"Required field validation did not behave "
            f"as expected for {field_name}."
        )

        return "FAIL"


# ==========================================
# MAIN TEST EXECUTION
# ==========================================

print("=" * 42)
print("TC-LEADGEN-02: REQUIRED FIELD VALIDATION")
print("=" * 42)


for field_to_leave_empty in TEST_FIELDS:

    print("\n")
    print("=" * 42)
    print(f"TESTING EMPTY FIELD: {field_to_leave_empty.upper()}")
    print("=" * 42)

    driver = None

    try:

        driver, wait = start_browser()

        login_and_open_form(driver, wait)

        fill_lead_form(
            field_to_leave_empty,
            driver,
            wait
        )

        submit_form(driver, wait)

        result = check_validation_response(
            field_to_leave_empty,
            driver,
            wait
        )

        results[field_to_leave_empty] = result

    except Exception as e:

        results[field_to_leave_empty] = "TEST SETUP ERROR"

        print("\nTEST SETUP ERROR")
        print(f"Field: {field_to_leave_empty}")
        print(f"Error type: {type(e).__name__}")
        print(f"Error details: {e}")

        if driver is not None:

            try:
                print(f"\nCurrent URL: {driver.current_url}")
            except Exception:
                pass

    finally:

        if driver is not None:

            print("\nClosing Chrome session...")

            try:
                driver.quit()
            except Exception:
                pass


# ==========================================
# FINAL TEST SUMMARY
# ==========================================

print("\n")
print("=" * 42)
print("TC-LEADGEN-02: FINAL TEST SUMMARY")
print("=" * 42)

for field, result in results.items():

    print(f"{field}: {result}")

print("-" * 42)

passed = sum(
    1 for result in results.values()
    if result == "PASS"
)

failed = sum(
    1 for result in results.values()
    if result == "FAIL"
)

inconclusive = sum(
    1 for result in results.values()
    if result == "INCONCLUSIVE"
)

setup_errors = sum(
    1 for result in results.values()
    if result == "TEST SETUP ERROR"
)

print(f"Passed: {passed}")
print(f"Failed: {failed}")
print(f"Inconclusive: {inconclusive}")
print(f"Setup errors: {setup_errors}")

print("-" * 42)
print("Testing completed.")

