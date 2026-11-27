from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException,
)

# ==========================================
# SCENARIO 5: SEND AN EMAIL
# ==========================================

# TEST ACCOUNT CREDENTIALS
EMAIL = "secbtelemarketer@gmail.com"
PASSWORD = "TelemarketerSectionB123!"

# TEST DATA
LEAD_NAME = "Bluegum Manufacturing Demo 236"
EXPECTED_RECIPIENT = "lead236@demo-business236.example"

TELEMARKETER_NAME = "SecB Telemarketer"

SUBJECT_TEMPLATE = (
    "Congratulations! You're Eligible for a Free Hot Water System Upgrade"
)

WEBSITE = "https://sortrleaddistribution-client.onrender.com/"

# ==========================================
# PLACEHOLDER VALIDATION
# ==========================================

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

# ==========================================
# STEP 1: CONFIGURE CHROME
# ==========================================

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--force-device-scale-factor=1")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 60)
short_wait = WebDriverWait(driver, 10)

try:
    print()
    print("==========================================")
    print("SCENARIO 5: SEND AN EMAIL")
    print("==========================================")

    # ==========================================
    # STEP 2: OPEN APPLICATION
    # ==========================================

    print("\nStep 1: Opening application...")
    driver.get(WEBSITE)

    # ==========================================
    # STEP 3: LOG IN
    # ==========================================

    print("\nStep 2: Logging in...")

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

    print("TEST PASSED: Login successful.")

    # ==========================================
    # STEP 4: OPEN LEADS PAGE
    # ==========================================

    print("\nStep 3: Opening Leads page...")

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

    print("Leads page opened.")

    # ==========================================
    # STEP 5: SEARCH FOR TARGET LEAD
    # ==========================================

    print("\nStep 4: Searching for target lead...")

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

    print("TEST PASSED: Target lead found.")

    # ==========================================
    # STEP 6: VERIFY RECIPIENT
    # ==========================================

    print("\nStep 5: Verifying recipient...")

    if EXPECTED_RECIPIENT.lower() not in target_row.text.lower():
        raise Exception(
            "Expected recipient was not found in the target lead row. "
            "Email was not sent."
        )

    print("Recipient verified:", EXPECTED_RECIPIENT)

    # ==========================================
    # STEP 7: LOCATE EMAIL ICON
    # ==========================================

    print("\nStep 6: Locating email icon...")

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
        print("Icon not found inside the target row.")
        print("Searching all email icons on the page...")

    if email_button is None:

        icons = wait.until(
            EC.presence_of_all_elements_located(
                (
                    By.CSS_SELECTOR,
                    'svg[data-testid="AttachEmailIcon"]'
                )
            )
        )

        print("Email icons found:", len(icons))

        for icon in icons:

            try:
                candidate = icon.find_element(
                    By.XPATH,
                    "./ancestor::button[1]"
                )

            except Exception:
                try:
                    candidate = icon.find_element(
                        By.XPATH,
                        "./ancestor::a[1]"
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
                EXPECTED_RECIPIENT,
            )

            if surrounding_html:
                email_button = candidate
                break

        if email_button is None:
            raise Exception(
                "Could not safely identify the email action "
                "for the target lead."
            )

    # ==========================================
    # STEP 8: CLICK EMAIL ICON
    # ==========================================

    print("\nStep 7: Clicking email icon...")

    driver.execute_script(
        """
        arguments[0].scrollIntoView({
            block: 'center',
            inline: 'center'
        });
        """,
        email_button,
    )

    wait.until(
        lambda d: (
            email_button.is_displayed()
            and email_button.is_enabled()
        )
    )

    try:
        email_button.click()

    except ElementClickInterceptedException:
        driver.execute_script(
            "arguments[0].click();",
            email_button
        )

    print("Email icon clicked.")

    # ==========================================
    # STEP 9: WAIT FOR EMAIL MODAL
    # ==========================================

    print("\nStep 8: Waiting for email modal...")

    wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[normalize-space()='Send An Email']")
        )
    )

    print("Email modal opened.")

    # ==========================================
    # STEP 10: VERIFY MODAL RECIPIENT
    # ==========================================

    print("\nStep 9: Verifying modal recipient...")

    recipient_field_xpath = (
        f"//input[@value='{EXPECTED_RECIPIENT}']"
    )

    recipient_field = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, recipient_field_xpath)
        )
    )

    if recipient_field.get_attribute("value") != EXPECTED_RECIPIENT:
        raise Exception(
            "Recipient mismatch. Email was not sent."
        )

    print("TEST PASSED: Modal recipient verified.")

    # ==========================================
    # STEP 11: SELECT SUBJECT TEMPLATE
    # ==========================================

    print("\nStep 10: Selecting subject template...")

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

    print("Subject dropdown opened.")

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

    print("Subject template selected.")

    # ==========================================
    # STEP 12: WAIT FOR TEMPLATE TEXT
    # ==========================================

    print("\nStep 11: Waiting for template text...")

    text_area_xpath = "//textarea[@name='text']"

    text_area = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, text_area_xpath)
        )
    )

    wait.until(
        lambda d: bool(
            d.find_element(
                By.XPATH,
                text_area_xpath
            ).get_attribute("value").strip()
        )
    )

    message_text = text_area.get_attribute("value") or ""

    print("TEST PASSED: Template text populated.")
    print("Message characters:", len(message_text))

    # ==========================================
    # STEP 13: REPLACE CUSTOMER NAME
    # ==========================================

    print("\nStep 12: Replacing customer name...")

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

    print("Customer name replaced with:", LEAD_NAME)

    # ==========================================
    # STEP 14: REPLACE TELEMARKETER NAME
    # ==========================================

    print("\nStep 13: Replacing telemarketer name...")

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

    print("Telemarketer name replaced with:", TELEMARKETER_NAME)

    # ==========================================
    # STEP 15: REPLACE OTHER PLACEHOLDERS
    # ==========================================

    print("\nStep 14: Replacing remaining known placeholders...")

    message_text = message_text.replace(
        "[Your Contact Information]",
        "Contact information not provided for this test"
    )

    message_text = message_text.replace(
        "[Your Website URL]",
        WEBSITE
    )

    # ==========================================
    # STEP 16: UPDATE EMAIL MESSAGE
    # ==========================================

    print("\nStep 15: Updating email message...")

    text_area = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, text_area_xpath)
        )
    )

    text_area.click()
    text_area.send_keys(Keys.CONTROL, "a")
    text_area.send_keys(Keys.BACKSPACE)
    text_area.send_keys(message_text)

    updated_message = (
        text_area.get_attribute("value") or ""
    )

    print("\nUpdated email message:")
    print("------------------------------------------")
    print(updated_message)
    print("------------------------------------------")

    # ==========================================
    # STEP 17: VERIFY CUSTOMER NAME
    # ==========================================

    print("\nStep 16: Verifying customer name...")

    if (
        "{Customer Name}" in updated_message
        or "{{Customer Name}}" in updated_message
        or "[Customer's Name]" in updated_message
    ):
        raise Exception(
            "Customer Name placeholder was not replaced. "
            "Email was NOT sent."
        )

    if LEAD_NAME not in updated_message:
        raise Exception(
            "Actual customer name was not found in the email. "
            "Email was NOT sent."
        )

    print("TEST PASSED: Customer name successfully replaced.")

    # ==========================================
    # STEP 18: VERIFY TELEMARKETER NAME
    # ==========================================

    print("\nStep 17: Verifying telemarketer name...")

    if (
        "{Telemarketer Name}" in updated_message
        or "{{Telemarketer Name}}" in updated_message
        or "[Telemarketer Name]" in updated_message
    ):
        raise Exception(
            "Telemarketer Name placeholder was not replaced. "
            "Email was NOT sent."
        )

    if TELEMARKETER_NAME not in updated_message:
        raise Exception(
            "Actual telemarketer name was not found in the email. "
            "Email was NOT sent."
        )

    print(
        "TEST PASSED: Telemarketer name successfully replaced."
    )

    # ==========================================
    # STEP 19: CHECK KNOWN PLACEHOLDERS
    # ==========================================

    print("\nStep 18: Checking remaining placeholders...")

    remaining_placeholders = [
        placeholder
        for placeholder in KNOWN_PLACEHOLDERS
        if placeholder in updated_message
    ]

    if remaining_placeholders:
        raise Exception(
            "Unedited placeholders remain: "
            + ", ".join(remaining_placeholders)
            + ". Email was NOT sent."
        )

    print("TEST PASSED: No known unresolved placeholders remain.")

    # ==========================================
    # STEP 20: LOCATE SEND BUTTON
    # ==========================================

    print("\nStep 19: Locating Send button...")

    send_button_xpath = (
        "//button[@type='submit' and normalize-space()='Send']"
    )

    send_button = short_wait.until(
        EC.presence_of_element_located(
            (By.XPATH, send_button_xpath)
        )
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        send_button
    )

    if not send_button.is_enabled():
        raise Exception(
            "Send button is disabled. Email was not sent."
        )

    print("TEST PASSED: Send button located and enabled.")

    # ==========================================
    # STEP 21: FINAL SAFETY CHECKS
    # ==========================================

    print("\nStep 20: Performing final checks...")

    recipient_field = driver.find_element(
        By.XPATH,
        recipient_field_xpath
    )

    text_area = driver.find_element(
        By.XPATH,
        text_area_xpath
    )

    final_recipient = recipient_field.get_attribute("value")
    final_message = text_area.get_attribute("value") or ""

    if final_recipient != EXPECTED_RECIPIENT:
        raise Exception(
            "Recipient changed before sending. Email was not sent."
        )

    if not final_message.strip():
        raise Exception(
            "Email message is empty. Email was not sent."
        )

    if LEAD_NAME not in final_message:
        raise Exception(
            "Customer name is missing from the final message. "
            "Email was not sent."
        )

    if TELEMARKETER_NAME not in final_message:
        raise Exception(
            "Telemarketer name is missing from the final message. "
            "Email was not sent."
        )

    remaining_placeholders = [
        placeholder
        for placeholder in KNOWN_PLACEHOLDERS
        if placeholder in final_message
    ]

    if remaining_placeholders:
        raise Exception(
            "Placeholders remain in the final message: "
            + ", ".join(remaining_placeholders)
            + ". Email was not sent."
        )

    print("Recipient:", final_recipient)
    print("Subject:", SUBJECT_TEMPLATE)
    print("Customer Name:", LEAD_NAME)
    print("Telemarketer Name:", TELEMARKETER_NAME)
    print("Message is complete.")
    print("Final safety checks passed.")

    # ==========================================
    # STEP 22: SEND EMAIL
    # ==========================================

    print("\nStep 21: Clicking Send...")

    send_button = short_wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, send_button_xpath)
        )
    )

    try:
        send_button.click()
        print("Standard Selenium click executed.")

    except ElementClickInterceptedException:
        print("Standard click intercepted.")
        print("Attempting JavaScript click...")

        send_button = driver.find_element(
            By.XPATH,
            send_button_xpath
        )

        driver.execute_script(
            "arguments[0].click();",
            send_button
        )

        print("JavaScript click executed.")

    print("Send action attempted. Waiting for confirmation...")

    # ==========================================
    # STEP 23: VERIFY APPLICATION RESPONSE
    # ==========================================

    print("\nStep 22: Verifying email submission...")

    try:
        success_message = WebDriverWait(
            driver,
            15
        ).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//*[contains(translate(normalize-space(.),"
                    "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
                    "'abcdefghijklmnopqrstuvwxyz'),"
                    "'email sent') or "
                    "contains(translate(normalize-space(.),"
                    "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
                    "'abcdefghijklmnopqrstuvwxyz'),"
                    "'successfully sent')]",
                )
            )
        )

        print("------------------------------------------")
        print("TEST PASSED: Success confirmation detected.")
        print("Confirmation:", success_message.text)
        print("------------------------------------------")

    except TimeoutException:
        print("------------------------------------------")
        print("No recognizable success message was detected.")
        print("Check for validation errors or whether the modal closed.")
        print("Verify the email in the application or backend logs.")
        print("------------------------------------------")

    # ==========================================
    # STEP 24: FINAL SUMMARY
    # ==========================================

    print("\n==========================================")
    print("SCENARIO 5: AUTOMATION FINISHED")
    print("Login successful.")
    print("Target lead verified.")
    print("Recipient checked.")
    print("Subject template selected.")
    print("Customer name automatically replaced.")
    print("Telemarketer name automatically replaced.")
    print("Remaining placeholders checked.")
    print("Send action attempted.")
    print("Confirm successful sending in the application.")
    print("==========================================")

except TimeoutException:
    print("\nSCENARIO 5: TEST FAILED")
    print("A required element did not appear in time.")

    try:
        print("Current URL:", driver.current_url)
    except Exception:
        pass

except Exception as error:
    print("\nSCENARIO 5: TEST FAILED")
    print("Error type:", type(error).__name__)
    print("Error details:", error)

finally:
    try:
        if driver and driver.session_id:
            input("\nPress Enter to close the browser...")
            driver.quit()
    except Exception:
        pass
