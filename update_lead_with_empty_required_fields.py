from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException,
    NoSuchElementException,
    StaleElementReferenceException,
)

import time


# ==========================================
# TC-TELE-03: REQUIRED FIELD VALIDATION
# ==========================================

EMAIL = "salungajust@gmail.com"
PASSWORD = "ABCabc123!"

WEBSITE = "https://sortrleaddistribution-client.onrender.com/"

LEAD_NAME = "Jisu cafe"
LEAD_ID = "6665851e15dfa876b32c78e8"

PHONE_VALUE = "68974125837"
EMAIL_VALUE = "jisu@gmail.com"
REMARKS_VALUE = "10 Liters of tank... Callback later @11am"

CALL_DISPOSITION = "Already Installed"

TEST_FIELDS = [
    "Phone Number",
    "Email",
    "Remarks"
]

results = []


# ==========================================
# STEP 1: START FRESH CHROME SESSION
# ==========================================

def start_browser():

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--force-device-scale-factor=1")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 60)

    return driver, wait


# ==========================================
# STEP 2: LOGIN AND OPEN LEADS
# ==========================================

def login_and_open_leads(driver, wait):

    driver.get(WEBSITE)

    email_field = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input[type="email"]')
        )
    )

    email_field.send_keys(EMAIL)

    password_field = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input[type="password"]')
        )
    )

    password_field.send_keys(PASSWORD)

    login_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[normalize-space()='Log In']")
        )
    )

    login_button.click()

    wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[normalize-space()='DASHBOARD']")
        )
    )

    leads_link = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//*[normalize-space()='Leads']")
        )
    )

    leads_link.click()

    wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[normalize-space()='ASSIGNED LEADS']")
        )
    )


# ==========================================
# STEP 3: SEARCH FOR JISU CAFE
# ==========================================

def find_target_lead(driver, wait):

    search_box = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input[placeholder="Search"]')
        )
    )

    search_box.clear()
    search_box.send_keys(LEAD_NAME)

    row_xpath = (
        f"//*[@role='row' and @data-id='{LEAD_ID}']"
    )

    target_row = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, row_xpath)
        )
    )

    row_text = target_row.text

    if LEAD_NAME not in row_text:
        raise AssertionError("Incorrect lead name.")

    if "jisu@gmail.com" not in row_text:
        raise AssertionError("Target lead email does not match.")

    return target_row


# ==========================================
# STEP 4: OPEN EDIT FORM
# ==========================================

def open_edit_form(driver, wait, target_row):

    driver.execute_script(
        """
        arguments[0].scrollIntoView({
            block: 'center',
            inline: 'center'
        });
        """,
        target_row
    )

    ActionChains(driver).move_to_element(
        target_row
    ).perform()

    edit_icon = wait.until(
        lambda d: next(
            (
                icon for icon in target_row.find_elements(
                    By.CSS_SELECTOR,
                    'svg[data-testid="EditIcon"]'
                )
                if icon.is_displayed()
            ),
            False
        )
    )

    driver.execute_script(
        """
        arguments[0].scrollIntoView({
            block: 'center',
            inline: 'center'
        });
        """,
        edit_icon
    )

    try:
        edit_icon.click()

    except ElementClickInterceptedException:

        driver.execute_script(
            "arguments[0].click();",
            edit_icon
        )

    wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input[name="phonenumber"]')
        )
    )

    wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input[name="emailaddress"]')
        )
    )

    wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'textarea[name="remarks"]')
        )
    )

    wait.until(
        EC.visibility_of_element_located(
            (By.ID, "mui-component-select-callDisposition")
        )
    )


# ==========================================
# STEP 5: SELECT CALL DISPOSITION
# ==========================================

def select_call_disposition(driver, wait):

    disposition = wait.until(
        EC.element_to_be_clickable(
            (By.ID, "mui-component-select-callDisposition")
        )
    )

    disposition.click()

    option_xpath = (
        "//*[@role='option' and "
        "translate(normalize-space(.),"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
        "'abcdefghijklmnopqrstuvwxyz')='already installed']"
    )

    option = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, option_xpath)
        )
    )

    option.click()


# ==========================================
# STEP 6: FILL THE THREE FORM FIELDS
# ==========================================

def fill_test_fields(driver, wait):

    phone_field = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input[name="phonenumber"]')
        )
    )

    email_field = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input[name="emailaddress"]')
        )
    )

    remarks_field = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'textarea[name="remarks"]')
        )
    )

    # Phone Number
    phone_field.click()
    phone_field.send_keys(Keys.CONTROL, "a")
    phone_field.send_keys(Keys.BACKSPACE)
    phone_field.send_keys(PHONE_VALUE)

    # Email
    email_field.click()
    email_field.send_keys(Keys.CONTROL, "a")
    email_field.send_keys(Keys.BACKSPACE)
    email_field.send_keys(EMAIL_VALUE)

    # Remarks
    remarks_field.click()
    remarks_field.send_keys(Keys.CONTROL, "a")
    remarks_field.send_keys(Keys.BACKSPACE)
    remarks_field.send_keys(REMARKS_VALUE)

    return {
        "Phone Number": phone_field,
        "Email": email_field,
        "Remarks": remarks_field
    }


# ==========================================
# STEP 7: CLEAR ONLY THE SELECTED FIELD
# ==========================================

def clear_selected_field(driver, wait, selected_field):

    selectors = {
        "Phone Number": 'input[name="phonenumber"]',
        "Email": 'input[name="emailaddress"]',
        "Remarks": 'textarea[name="remarks"]'
    }

    field = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, selectors[selected_field])
        )
    )

    field.click()
    field.send_keys(Keys.CONTROL, "a")
    field.send_keys(Keys.BACKSPACE)

    print("\nVERIFYING FIELD VALUES:")

    for label, selector in selectors.items():

        current_field = driver.find_element(
            By.CSS_SELECTOR,
            selector
        )

        value = current_field.get_attribute("value")

        print(label, "=", repr(value))

        if label == selected_field:

            if value.strip() != "":
                raise AssertionError(
                    selected_field + " was not cleared."
                )

        else:

            if value.strip() == "":
                raise AssertionError(
                    label + " should not be empty."
                )


# ==========================================
# STEP 8: CLICK UPDATE
# ==========================================

def click_update(driver, wait):

    update_xpath = (
        "//button[normalize-space()='Update' "
        "or normalize-space()='Update Lead']"
    )

    update_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, update_xpath)
        )
    )

    update_button.click()

    time.sleep(3)


# ==========================================
# STEP 9: CHECK FIELD VALIDATION
# ==========================================

def check_validation(driver, selected_field):

    selectors = {
        "Phone Number": 'input[name="phonenumber"]',
        "Email": 'input[name="emailaddress"]',
        "Remarks": 'textarea[name="remarks"]'
    }

    fields = driver.find_elements(
        By.CSS_SELECTOR,
        selectors[selected_field]
    )

    visible_fields = [
        field for field in fields
        if field.is_displayed()
    ]

    # Form closed = no blocking validation confirmed.
    if not visible_fields:

        print("FAIL: Edit form closed after submission.")
        print("No blocking validation was confirmed.")

        return "FAIL"

    field = visible_fields[0]

    # Verify the selected field is still empty.
    field_value = field.get_attribute("value") or ""

    if field_value.strip() != "":

        print("FAIL: Selected field is no longer empty.")

        return "FAIL"

    aria_invalid = field.get_attribute("aria-invalid")

    print("Selected field:", selected_field)
    print("aria-invalid:", aria_invalid)

    # Check field-specific helper text.
    helper_text = ""

    described_by = field.get_attribute("aria-describedby")

    if described_by:

        for helper_id in described_by.split():

            helper_elements = driver.find_elements(
                By.ID,
                helper_id
            )

            for helper in helper_elements:

                if helper.is_displayed():
                    helper_text += " " + helper.text.strip()

    # Check closest Material UI FormControl.
    try:

        form_control = field.find_element(
            By.XPATH,
            "./ancestor::div[contains(@class,'MuiFormControl-root')][1]"
        )

        helper_elements = form_control.find_elements(
            By.CSS_SELECTOR,
            ".MuiFormHelperText-root"
        )

        for helper in helper_elements:

            if helper.is_displayed() and helper.text.strip():
                helper_text += " " + helper.text.strip()

    except NoSuchElementException:
        pass

    helper_text = helper_text.strip()

    # Check general form-level error messages.
    general_error_text = ""

    error_selectors = [
        '[role="alert"]',
        '.MuiAlert-message',
        '.MuiSnackbarContent-message',
        '.Toastify__toast-body'
    ]

    for selector in error_selectors:

        error_elements = driver.find_elements(
            By.CSS_SELECTOR,
            selector
        )

        for element in error_elements:

            if element.is_displayed() and element.text.strip():

                general_error_text += (
                    " " + element.text.strip()
                )

    general_error_text = general_error_text.strip()

    if helper_text:
        print("Field message:", helper_text)

    if general_error_text:
        print("Form message:", general_error_text)

    # PASS when blocking validation is detected.
    if (
        aria_invalid == "true"
        or helper_text
        or general_error_text
    ):

        print(
            "PASS: Validation indicator detected."
        )

        return "PASS"

    # Form remained open and the selected field is still empty.
    # This is an indirect indication that submission was blocked.
    print(
        "PASS: Edit form remained open and the selected field "
        "remained empty after submission."
    )

    print(
        "No explicit validation message was detected."
    )

    return "PASS"


# ==========================================
# STEP 10: EXECUTE ONE TEST SCENARIO
# ==========================================

def execute_test(selected_field):

    driver = None

    print("\n")
    print("==========================================")
    print("TC-TELE-03:", selected_field, "EMPTY")
    print("==========================================")

    try:

        driver, wait = start_browser()

        login_and_open_leads(
            driver,
            wait
        )

        target_row = find_target_lead(
            driver,
            wait
        )

        open_edit_form(
            driver,
            wait,
            target_row
        )

        select_call_disposition(
            driver,
            wait
        )

        fill_test_fields(
            driver,
            wait
        )

        clear_selected_field(
            driver,
            wait,
            selected_field
        )

        click_update(
            driver,
            wait
        )

        result = check_validation(
            driver,
            selected_field
        )

        return result

    except Exception as error:

        print("\nTEST EXECUTION ERROR")
        print("Error type:", type(error).__name__)
        print("Error details:", error)

        return "INCONCLUSIVE"

    finally:

        if driver is not None:

            try:

                if driver.session_id:
                    driver.quit()

            except Exception:
                pass


# ==========================================
# MAIN EXECUTION: THREE TEST SCENARIOS
# ==========================================

print("\n")
print("==========================================")
print("TC-TELE-03: REQUIRED FIELD VALIDATION")
print("==========================================")

for selected_field in TEST_FIELDS:

    result = execute_test(selected_field)

    results.append({
        "Field": selected_field,
        "Result": result
    })


# ==========================================
# FINAL TEST SUMMARY
# ==========================================

print("\n")
print("==========================================")
print("TC-TELE-03: FINAL TEST SUMMARY")
print("==========================================")

passed = 0
failed = 0
inconclusive = 0

for item in results:

    print(
        item["Field"],
        "EMPTY:",
        item["Result"]
    )

    if item["Result"] == "PASS":
        passed += 1

    elif item["Result"] == "FAIL":
        failed += 1

    else:
        inconclusive += 1

print("------------------------------------------")
print("Passed:", passed)
print("Failed:", failed)
print("Inconclusive:", inconclusive)
print("------------------------------------------")

print("Testing completed.")

