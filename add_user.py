
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException

# ==========================================
# TC-TEAM-03: ADD A NEW USER
# ==========================================

# TEAM LEADER TEST ACCOUNT
EMAIL = "3bteamleader@gmail.com"
PASSWORD = "3BTeamLeader123!"

# NEW USER TEST DATA
FULL_NAME = "Juan Dela Cruz"
NEW_EMAIL = "juan.delacruz.qa@example.com"
NEW_PASSWORD = "TestUser123!"
ROLE = "Telemarketer"

# ==========================================
# STEP 1: CONFIGURE MICROSOFT EDGE
# ==========================================

options = webdriver.EdgeOptions()

# Open Edge in maximized window
options.add_argument("--start-maximized")

# Set browser zoom to 80%
options.add_argument("--force-device-scale-factor=0.8")

driver = webdriver.Edge(options=options)

wait = WebDriverWait(driver, 60)

try:

    print("TC-TEAM-03: ADD NEW USER")
    print("-----------------------------------")

    # ======================================
    # STEP 2: OPEN THE WEBSITE
    # ======================================

    driver.get("https://sortrleaddistribution-client.onrender.com/")

    driver.execute_script("document.body.style.zoom='100%'")

    print("Website opened.")

    # ======================================
    # STEP 3: WAIT FOR EMAIL FIELD
    # ======================================

    email_field = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input[type="email"]')
        )
    )

    # ======================================
    # STEP 4: ENTER TEAM LEADER EMAIL
    # ======================================

    email_field.send_keys(EMAIL)

    print("Team Leader email entered.")

    # ======================================
    # STEP 5: FIND PASSWORD FIELD
    # ======================================

    password_field = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input[type="password"]')
        )
    )

    # ======================================
    # STEP 6: ENTER TEAM LEADER PASSWORD
    # ======================================

    password_field.send_keys(PASSWORD)

    print("Team Leader password entered.")

    # ======================================
    # STEP 7: FIND LOGIN BUTTON
    # ======================================

    login_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[normalize-space()='Log In']")
        )
    )

    # ======================================
    # STEP 8: CLICK LOGIN
    # ======================================

    login_button.click()

    print("Log In button clicked.")
    print("Waiting for Dashboard to load...")

    # ======================================
    # STEP 9: WAIT FOR DASHBOARD
    # ======================================

    dashboard = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[normalize-space()='DASHBOARD']")
        )
    )

    print("Team Leader successfully logged in.")
    print("Dashboard displayed.")

    # ======================================
    # STEP 10: OPEN ADD NEW USER
    # ======================================

    add_user_menu = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//span[normalize-space()='Add New User']")
        )
    )

    add_user_menu.click()

    print("Add New User menu clicked.")

    # ======================================
    # STEP 11: VERIFY CREATE NEW USER FORM
    # ======================================

    full_name_field = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "input[name='fullName']")
        )
    )

    email_input = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "input[name='email']")
        )
    )

    password_input = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "input[name='password']")
        )
    )

    print("Create New User form displayed.")

    # ======================================
    # STEP 12: ENTER NEW USER INFORMATION
    # ======================================

    full_name_field.send_keys(FULL_NAME)
    email_input.send_keys(NEW_EMAIL)
    password_input.send_keys(NEW_PASSWORD)

    print("New user information entered.")

    # ======================================
    # STEP 13: SELECT USER ROLE
    # ======================================

    role_dropdown = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//*[@role='combobox']")
        )
    )

    role_dropdown.click()

    role_option = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//*[@role='option' and normalize-space()='Telemarketer']"
            )
        )
    )

    role_option.click()

    print("Role selected: " + ROLE)

    # ======================================
    # STEP 14: VERIFY ENTERED INFORMATION
    # ======================================

    assert full_name_field.get_attribute("value") == FULL_NAME
    assert email_input.get_attribute("value") == NEW_EMAIL
    assert password_input.get_attribute("value") == NEW_PASSWORD

    print("Entered information verified.")

    # ======================================
    # STEP 15: CLICK ADD NEW USER BUTTON
    # ======================================

    add_button = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//button[@type='submit' and contains(normalize-space(.), 'Add New User')]"
            )
        )
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        add_button
    )

    add_button.click()

    print("Add New User button clicked.")
    print("Waiting for system response...")

    # ======================================
    # STEP 16: OPEN USERS PAGE
    # ======================================

    users_menu = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//span[normalize-space()='Users']")
        )
    )

    users_menu.click()

    print("Users page opened.")

    # ======================================
    # STEP 17: VERIFY NEW USER IN USERS LIST
    # ======================================

    try:

        new_user = wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    f"//*[contains(normalize-space(), '{NEW_EMAIL}')]"
                )
            )
        )

        if new_user.is_displayed():

            print()
            print("-----------------------------------")
            print("TC-TEAM-03: TEST PASSED")
            print("New user appears in the Users list.")
            print("Full Name:", FULL_NAME)
            print("Email:", NEW_EMAIL)
            print("Role:", ROLE)
            print("-----------------------------------")

    except TimeoutException:

        print()
        print("-----------------------------------")
        print("TC-TEAM-03: TEST FAILED")
        print("New user does not appear in the Users list.")
        print("-----------------------------------")

        driver.save_screenshot("TC_TEAM_03_failure.png")

except TimeoutException:

    print()
    print("-----------------------------------")
    print("TEST EXECUTION ERROR")
    print("An expected element did not appear within 60 seconds.")
    print("-----------------------------------")

    driver.save_screenshot("TC_TEAM_03_timeout.png")

except ElementClickInterceptedException as error:

    print()
    print("-----------------------------------")
    print("TEST EXECUTION ERROR")
    print("An element blocked the click.")
    print(error)
    print("-----------------------------------")

    driver.save_screenshot("TC_TEAM_03_click_error.png")

except Exception as error:

    print()
    print("-----------------------------------")
    print("TEST EXECUTION ERROR")
    print("An unexpected error occurred.")
    print(error)
    print("-----------------------------------")

    driver.save_screenshot("TC_TEAM_03_error.png")

finally:

    input("\nPress Enter to close the browser...")

    driver.quit()

