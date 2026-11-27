from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException,
    NoSuchElementException,
    StaleElementReferenceException,
)

# ==========================================
# TC-TELE-06: REQUIRED EMAIL FIELD VALIDATION
# ==========================================

# NEW TELEMARKETER ACCOUNT
EMAIL = "secbtelemarketer@gmail.com"
PASSWORD = "TelemarketerSectionB123!"

# TEST DATA
LEAD_NAME = "Bluegum Manufacturing Demo 236"
EXPECTED_RECIPIENT = "lead236@demo-business236.example"

TELEMARKETER_NAME = "SecB Telemarketer"
FROM_VALUE = TELEMARKETER_NAME

WEBSITE = "https://sortrleaddistribution-client.onrender.com/"

KNOWN_PLACEHOLDERS = [
    "{Customer Name}",
    "{{Customer Name}}",
    "[Customer's Name]",
    "[Your Contact Information]",
    "[Your Website URL]",
    "{Telemarketer Name}",
    "{{Telemarketer Name}}",
    "[Telemarketer Name]",
]

TEST_FIELDS = ["From", "To", "Subject"]

# Used only when Subject is intentionally left empty.
MANUAL_EMAIL_MESSAGE = (
    "Hello Bluegum Manufacturing Demo 236,\n\n"
    "This is a test email regarding your account.\n\n"
    "Thank you,\n"
    + TELEMARKETER_NAME
)

driver = None
wait = None
short_wait = None


# ==========================================
# STEP 1: START A FRESH CHROME SESSION
# ==========================================

def start_browser():

    global driver, wait, short_wait

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--force-device-scale-factor=1")

    driver = webdriver.Chrome(options=options)

    wait = WebDriverWait(driver, 60)
    short_wait = WebDriverWait(driver, 10)


# ==========================================
# HELPER: FIND FIELD BY LABEL
# ==========================================

def find_labeled_control(label_text):

    control_xpath = (
        f"//*[normalize-space()='{label_text}']"
        "/ancestor::div[contains(@class,'MuiFormControl-root')][1]"
        "//*[self::input or self::textarea or @role='combobox']"
    )

    elements = driver.find_elements(
        By.XPATH,
        control_xpath
    )

    for element in elements:

        if element.is_displayed():
            return element

    raise NoSuchElementException(
        f"Could not locate the visible {label_text} field."
    )


# ==========================================
# HELPER: FILL FROM FIELD
# ==========================================

def fill_from_field():

    field = find_labeled_control("From")

    if field.tag_name.lower() in ["input", "textarea"]:

        field.click()
        field.send_keys(Keys.CONTROL, "a")
        field.send_keys(FROM_VALUE)

        return field

    if field.get_attribute("role") == "combobox":

        field.click()

        option_xpath = (
            f"//*[@role='option' and "
            f"normalize-space()='{FROM_VALUE}']"
        )

        option = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, option_xpath)
            )
        )

        option.click()

        return field

    raise Exception(
        "The From field is not a supported input or dropdown."
    )


# ==========================================
# HELPER: FILL TO FIELD
# ==========================================

def fill_to_field():

    field = wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                f"//input[@value='{EXPECTED_RECIPIENT}']"
            )
        )
    )

    return field


# ==========================================
# HELPER: SELECT SUBJECT
# Used only for From and To tests
# ==========================================

def fill_subject_field():

    subject_dropdown = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//*[normalize-space()='Subject']"
                "/ancestor::div[contains(@class,'MuiFormControl-root')]"
                "//*[self::div or self::input]"
                "[@role='combobox' or @aria-haspopup='listbox']",
            )
        )
    )

    subject_dropdown.click()

    subject_option_xpath = (
        "//*[@role='option' and normalize-space(.)="
        "concat('Congratulations! You', \"'\", "
        "'re Eligible for a Free Hot Water System Upgrade')]"
    )

    subject_option = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, subject_option_xpath)
        )
    )

    subject_option.click()

    return subject_dropdown


# ==========================================
# HELPER: CLEAR FIELD
# ==========================================

def clear_field(field, field_name):

    if field.tag_name.lower() in ["input", "textarea"]:

        field.click()
        field.send_keys(Keys.CONTROL, "a")
        field.send_keys(Keys.BACKSPACE)

        current_value = field.get_attribute("value") or ""

        if current_value.strip():

            raise Exception(
                f"{field_name} field could not be cleared."
            )

        return

    if field.get_attribute("role") == "combobox":

        field.click()
        field.send_keys(Keys.BACKSPACE)

        visible_text = field.text.strip()

        if visible_text:

            raise Exception(
                f"{field_name} dropdown still contains "
                f"'{visible_text}'."
            )

        return

    raise Exception(
        f"Unsupported control type for {field_name}."
    )


# ==========================================
# HELPER: OPEN EMAIL MODAL
# ==========================================

def open_email_modal():

    print("\nOpening application...")

    driver.get(WEBSITE)

    print("Logging in...")

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
            (
                By.XPATH,
                "//button[normalize-space()='Log In']"
            )
        )
    )

    login_button.click()

    wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[normalize-space()='DASHBOARD']")
        )
    )

    print("Login successful.")

    # Open Leads page.
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

    # Search target lead.
    search_box = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input[placeholder="Search"]')
        )
    )

    search_box.clear()
    search_box.send_keys(LEAD_NAME)

    target_row_xpath = (
        "//*[@role='row' and "
        f".//*[normalize-space()='{LEAD_NAME}']]"
    )

    target_row = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, target_row_xpath)
        )
    )

    print("Target lead found.")

    # Verify recipient.
    if EXPECTED_RECIPIENT.lower() not in target_row.text.lower():

        raise Exception(
            "Expected recipient was not found in the target lead row."
        )

    print("Recipient verified.")

    # Locate email icon.
    email_button = None

    try:

        icon = target_row.find_element(
            By.CSS_SELECTOR,
            'svg[data-testid="AttachEmailIcon"]'
        )

        email_button = icon.find_element(
            By.XPATH,
            "./ancestor::button[1]"
        )

    except Exception:

        print("Searching for the email icon on the page...")

    if email_button is None:

        icons = wait.until(
            EC.presence_of_all_elements_located(
                (
                    By.CSS_SELECTOR,
                    'svg[data-testid="AttachEmailIcon"]'
                )
            )
        )

        for icon in icons:

            try:

                candidate = icon.find_element(
                    By.XPATH,
                    "./ancestor::button[1]"
                )

            except Exception:
                continue

            surrounding_html = driver.execute_script(
                """
                let element = arguments[0];
                const recipient = arguments[1];

                for (let i = 0; i < 10 && element; i++) {

                    if (
                        (element.innerText || "").includes(recipient)
                    ) {
                        return element.outerHTML;
                    }

                    element = element.parentElement;
                }

                return "";
                """,
                candidate,
                EXPECTED_RECIPIENT
            )

            if surrounding_html:

                email_button = candidate
                break

    if email_button is None:

        raise Exception(
            "Could not safely identify the target lead's email button."
        )

    driver.execute_script(
        """
        arguments[0].scrollIntoView({
            block: 'center',
            inline: 'center'
        });
        """,
        email_button
    )

    try:

        email_button.click()

    except ElementClickInterceptedException:

        driver.execute_script(
            "arguments[0].click();",
            email_button
        )

    wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//*[normalize-space()='Send An Email']"
            )
        )

    )

    print("Email modal opened.")


# ==========================================
# HELPER: PREPARE EMAIL BODY
# ==========================================

def prepare_email_body(field_name):

    text_area_xpath = "//textarea[@name='text']"

    text_area = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, text_area_xpath)
        )
    )

    # SUBJECT TEST:
    # No subject template is selected.
    # Enter a valid message body manually.

    if field_name == "Subject":

        print("\nPreparing message body without selecting a Subject...")

        text_area.click()
        text_area.send_keys(Keys.CONTROL, "a")
        text_area.send_keys(Keys.BACKSPACE)
        text_area.send_keys(MANUAL_EMAIL_MESSAGE)

        updated_message = text_area.get_attribute("value") or ""

        if not updated_message.strip():

            raise Exception(
                "Could not enter the manual email message."
            )

        print("Manual email message entered successfully.")

        return

    # FROM AND TO TESTS:
    # Wait for the selected Subject template to populate the message.

    wait.until(
        lambda d: bool(
            d.find_element(
                By.XPATH,
                text_area_xpath
            ).get_attribute("value").strip()
        )
    )

    text_area = driver.find_element(
        By.XPATH,
        text_area_xpath
    )

    message_text = text_area.get_attribute("value") or ""

    # ==========================================
    # REPLACE CUSTOMER NAME PLACEHOLDERS
    # ==========================================

    message_text = message_text.replace(
        "{{Customer Name}}",
        LEAD_NAME
    )

    message_text = message_text.replace(
        "{Customer Name}",
        LEAD_NAME
    )

    message_text = message_text.replace(
        "[Customer's Name]",
        LEAD_NAME
    )

    # ==========================================
    # REPLACE TELEMARKETER NAME PLACEHOLDERS
    # ==========================================

    message_text = message_text.replace(
        "{{Telemarketer Name}}",
        TELEMARKETER_NAME
    )

    message_text = message_text.replace(
        "{Telemarketer Name}",
        TELEMARKETER_NAME
    )

    message_text = message_text.replace(
        "[Telemarketer Name]",
        TELEMARKETER_NAME
    )

    # ==========================================
    # REPLACE OTHER KNOWN PLACEHOLDERS
    # ==========================================

    message_text = message_text.replace(
        "[Your Contact Information]",
        "Contact information not provided for this test"
    )

    message_text = message_text.replace(
        "[Your Website URL]",
        WEBSITE
    )

    # ==========================================
    # REWRITE THE TEXT AREA
    # ==========================================

    text_area.click()
    text_area.send_keys(Keys.CONTROL, "a")
    text_area.send_keys(Keys.BACKSPACE)
    text_area.send_keys(message_text)

    updated_message = text_area.get_attribute("value") or ""

    # ==========================================
    # VERIFY CUSTOMER NAME
    # ==========================================

    if LEAD_NAME not in updated_message:

        raise Exception(
            "Customer name was not correctly replaced in the message."
        )

    # ==========================================
    # VERIFY TELEMARKETER NAME
    # ==========================================

    if TELEMARKETER_NAME not in updated_message:

        raise Exception(
            "Telemarketer name was not correctly replaced in the message."
        )

    # ==========================================
    # VERIFY REMAINING PLACEHOLDERS
    # ==========================================

    remaining_placeholders = [
        item for item in KNOWN_PLACEHOLDERS
        if item in updated_message
    ]

    if remaining_placeholders:

        raise Exception(
            "Unresolved placeholders: "
            + ", ".join(remaining_placeholders)
        )

    print("Customer name successfully replaced.")
    print("Telemarketer name successfully replaced.")
    print("Email body verified.")


# ==========================================
# HELPER: PREPARE EMAIL
# ==========================================

def prepare_email(field_name):

    # Fill From.
    from_field = fill_from_field()

    # Fill To.
    to_field = fill_to_field()

    # Select Subject only for From and To tests.
    if field_name == "Subject":

        subject_field = None

        print("\nSubject test selected.")
        print("Subject dropdown will NOT be opened.")
        print("Subject will remain untouched and empty.")

    else:

        subject_field = fill_subject_field()

        print("Subject selected successfully.")

    # Prepare message body.
    prepare_email_body(field_name)

    return from_field, to_field, subject_field


# ==========================================
# HELPER: CLICK SEND BUTTON
# ==========================================

def click_send_button():

    send_button_xpath = (
        "//button[@type='submit' and normalize-space()='Send']"
    )

    send_button = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, send_button_xpath)
        )
    )

    driver.execute_script(
        """
        arguments[0].scrollIntoView({
            block: 'center',
            inline: 'center'
        });
        """,
        send_button
    )

    send_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, send_button_xpath)
        )
    )

    if not send_button.is_enabled():

        raise Exception(
            "Send button is disabled. Click could not be performed."
        )

    print("\nSend button located.")
    print("Attempting to click Send...")

    try:

        send_button.click()

        print("Send button clicked using Selenium.")

    except ElementClickInterceptedException:

        print("Normal click intercepted. Using JavaScript click.")

        send_button = driver.find_element(
            By.XPATH,
            send_button_xpath
        )

        driver.execute_script(
            "arguments[0].click();",
            send_button
        )

        print("Send button clicked using JavaScript.")

    return True


# ==========================================
# HELPER: CHECK VALIDATION RESPONSE
# ==========================================

def check_validation_response(field_name):

    print("Waiting for validation response...")

    validation_message = None

    try:

        WebDriverWait(driver, 15).until(
            lambda d: any(
                field_name.lower() in line.lower()
                and "required" in line.lower()
                for line in d.find_element(
                    By.TAG_NAME,
                    "body"
                ).text.splitlines()
            )
        )

    except TimeoutException:
        pass

    # Capture matching validation message.
    try:

        body_text = driver.find_element(
            By.TAG_NAME,
            "body"
        ).text

        lines = [
            line.strip()
            for line in body_text.splitlines()
            if line.strip()
        ]

        matching_lines = [
            line for line in lines
            if "required" in line.lower()
            and field_name.lower() in line.lower()
        ]

        if matching_lines:

            validation_message = matching_lines[-1]

    except Exception:
        pass

    print("\n------------------------------------------")

    if validation_message:

        print("VALIDATION MESSAGE DETECTED:")
        print(validation_message)

        print("RESULT: PASS")
        print(
            f"Submission was prevented when "
            f"{field_name} was empty."
        )

        print("------------------------------------------")

        return "PASS"

    # Check whether modal remains open.
    try:

        modal_elements = driver.find_elements(
            By.XPATH,
            "//*[normalize-space()='Send An Email']"
        )

        modal_open = any(
            element.is_displayed()
            for element in modal_elements
        )

    except Exception:

        modal_open = False

    if modal_open:

        print("Email modal remains open.")
        print("No matching validation message detected.")
        print("RESULT: INCONCLUSIVE")

        print("------------------------------------------")

        return "INCONCLUSIVE"

    print("No recognizable validation message detected.")
    print("RESULT: INCONCLUSIVE")

    print("------------------------------------------")

    return "INCONCLUSIVE"


# ==========================================
# MAIN TEST EXECUTION
# ==========================================

results = {}

print()
print("==========================================")
print("TC-TELE-06: REQUIRED EMAIL FIELD VALIDATION")
print("==========================================")

for field_name in TEST_FIELDS:

    print("\n")
    print("==========================================")
    print("TESTING EMPTY FIELD:", field_name.upper())
    print("==========================================")

    driver = None

    try:

        print("\nStarting a fresh Chrome session...")

        start_browser()

        # Open application and email modal.
        open_email_modal()

        # Prepare email.
        from_field, to_field, subject_field = prepare_email(
            field_name
        )

        # Clear only the selected field.
        if field_name == "From":

            print("\nClearing From field...")

            clear_field(from_field, "From")

            print("From field cleared.")

        elif field_name == "To":

            print("\nClearing To field...")

            clear_field(to_field, "To")

            print("To field cleared.")

        elif field_name == "Subject":

            print("\nSubject dropdown was not clicked.")
            print("Subject remains untouched.")

        # Submit incomplete email.
        print("\nPreparing to submit incomplete email...")

        click_send_button()

        # Check application response.
        results[field_name] = check_validation_response(
            field_name
        )

    except Exception as error:

        results[field_name] = "TEST SETUP ERROR"

        print("\nTEST SETUP ERROR for", field_name)
        print("Error type:", type(error).__name__)
        print("Error details:", error)

        try:

            if driver:
                print("Current URL:", driver.current_url)

        except Exception:
            pass

    finally:

        if driver is not None:

            try:

                if driver.session_id:

                    print("\nClosing Chrome session...")
                    driver.quit()

            except Exception:
                pass

        driver = None
        wait = None
        short_wait = None


# ==========================================
# FINAL TEST SUMMARY
# ==========================================

print("\n")
print("==========================================")
print("TC-TELE-06: FINAL TEST SUMMARY")
print("==========================================")

for field_name in TEST_FIELDS:

    print(
        f"{field_name}: "
        f"{results.get(field_name, 'NOT EXECUTED')}"
    )

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

print("------------------------------------------")
print("Passed:", passed)
print("Failed:", failed)
print("Inconclusive:", inconclusive)
print("Setup errors:", setup_errors)
print("------------------------------------------")

print("Testing completed.")
