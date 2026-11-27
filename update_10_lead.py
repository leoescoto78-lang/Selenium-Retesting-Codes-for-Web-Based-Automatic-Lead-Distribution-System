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
# TC-TELE-04: UPDATE LEADS
# ==========================================

# TELEMARKETER LOGIN CREDENTIALS
EMAIL = "secbtelemarketer@gmail.com"
PASSWORD = "TelemarketerSectionB123!"

# ==========================================
# TEST DATA: 10 DISTINCT LEADS
# ==========================================

LEADS = [
    {"id": "b9ea", "name": "Bluegum Manufacturing Demo 236"},
    {"id": "b9ec", "name": "Peak Fitness Club Demo 238"},
    {"id": "b9ef", "name": "Copper Kettle Brewery Demo 241"},
    {"id": "b9f0", "name": "Happy Paws Pet Shop Demo 242"},
    {"id": "b9f1", "name": "Fresh Fold Laundry Demo 243"},
    {"id": "b9f3", "name": "Parkside Garage Demo 245"},
    {"id": "b9f4", "name": "Trusted Torque Mechanics Demo 246"},
    {"id": "b9f5", "name": "Riverside Butchery Demo 247"},
    {"id": "b9f6", "name": "Ereshfield Agriculture Demo 248"},
    {"id": "b9f7", "name": "Northview Learning Centre Demo 249"},
]

NEW_CITY = "Angeles"

# ==========================================
# CHROME CONFIGURATION
# ==========================================

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--force-device-scale-factor=1")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 60)

passed = 0
failed = 0
results = []

# ==========================================
# HELPER: LOCATE LEAD ROW
# ==========================================

def locate_lead_row(lead_id):

    row_xpath = (
        f"//tr[.//*[normalize-space()='{lead_id}']]"
        f" | //*[@role='row'][.//*[normalize-space()='{lead_id}']]"
    )

    return wait.until(
        EC.presence_of_element_located(
            (By.XPATH, row_xpath)
        )
    )

# ==========================================
# HELPER: OPEN EDIT FORM
# ==========================================

def open_edit_form(lead_id):

    row = locate_lead_row(lead_id)

    edit_button = row.find_element(
        By.XPATH,
        ".//button[.//*[@data-testid='EditIcon']]"
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        edit_button
    )

    try:
        edit_button.click()

    except ElementClickInterceptedException:
        driver.execute_script(
            "arguments[0].click();",
            edit_button
        )

    wait.until(
        EC.visibility_of_element_located(
            (By.NAME, "city")
        )
    )

    wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//button[@type='submit' and "
                "translate(normalize-space(.),"
                "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
                "'abcdefghijklmnopqrstuvwxyz')='update']"
            )
        )
    )

# ==========================================
# HELPER: UPDATE CITY
# ==========================================

def update_city(city_value):

    # LOCATE CITY TEXTBOX
    city_field = wait.until(
        EC.element_to_be_clickable(
            (By.NAME, "city")
        )
    )

    # CLEAR AND ENTER NEW CITY
    city_field.click()
    city_field.send_keys(Keys.CONTROL, "a")
    city_field.send_keys(Keys.BACKSPACE)
    city_field.send_keys(city_value)

    # VERIFY ENTERED VALUE
    entered_city = city_field.get_attribute("value")

    if entered_city != city_value:

        raise Exception(
            f"City input mismatch. "
            f"Expected: {city_value}, "
            f"Actual: {entered_city}"
        )

    print(f"City entered: {entered_city}")

    # LOCATE ACTUAL UPDATE BUTTON
    update_button = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//button[@type='submit' and "
                "translate(normalize-space(.),"
                "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
                "'abcdefghijklmnopqrstuvwxyz')='update']"
            )
        )
    )

    # SCROLL UPDATE BUTTON INTO VIEW
    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        update_button
    )

    # CLICK UPDATE
    update_button.click()

    print("Update button clicked.")

    # WAIT FOR EDIT FORM TO CLOSE
    wait.until(
        EC.invisibility_of_element_located(
            (By.NAME, "city")
        )
    )

# ==========================================
# STEP 1: OPEN APPLICATION
# ==========================================

try:

    print()
    print("=" * 50)
    print("TC-TELE-04: UPDATE LEADS")
    print("=" * 50)

    print("\nStep 1: Opening application...")

    driver.get(
        "https://sortrleaddistribution-client.onrender.com/"
    )

    # ==========================================
    # STEP 2: ZOOM OUT BROWSER
    # ==========================================

    driver.execute_script(
        "document.body.style.zoom='80%'"
    )

    print("Browser zoom set to 80%.")
    print("Application opened successfully.")

    # ==========================================
    # STEP 3: LOGIN
    # ==========================================

    print("\nStep 2: Logging in...")

    email_field = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input[type="email"]')
        )
    )

    email_field.clear()
    email_field.send_keys(EMAIL)

    password_field = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input[type="password"]')
        )
    )

    password_field.clear()
    password_field.send_keys(PASSWORD)

    login_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[normalize-space()='Log In']")
        )
    )

    login_button.click()

    # ==========================================
    # STEP 4: VERIFY DASHBOARD
    # ==========================================

    print("\nStep 3: Waiting for Dashboard...")

    wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[normalize-space()='DASHBOARD']")
        )
    )

    print("Login successful.")

    # ==========================================
    # STEP 5: OPEN LEADS PAGE
    # ==========================================

    print("\nStep 4: Opening Leads page...")

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

    wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//*[contains(translate(normalize-space(),"
                "'abcdefghijklmnopqrstuvwxyz',"
                "'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),"
                "'ASSIGNED LEADS')]"
            )
        )
    )

    print("Assigned Leads page opened.")

    # ==========================================
    # STEP 6: VERIFY 10 TARGET LEADS
    # ==========================================

    print("\nStep 5: Checking target lead records...")

    for lead in LEADS:

        locate_lead_row(lead["id"])

        print(
            f"Lead identified: "
            f"{lead['id']} - {lead['name']}"
        )

    print("------------------------------------------")
    print("TEST SETUP PASSED: All 10 target records identified.")
    print("------------------------------------------")

    # ==========================================
    # STEP 7: UPDATE AND VERIFY EACH LEAD
    # ==========================================

    print("\nStep 6: Updating City for each lead...")

    for index, lead in enumerate(LEADS, start=1):

        lead_id = lead["id"]
        lead_name = lead["name"]

        print()
        print("-" * 50)
        print(f"Record {index}/10: {lead_name}")
        print(f"Lead ID: {lead_id}")
        print(f"Target City: {NEW_CITY}")
        print("-" * 50)

        try:

            # OPEN CORRECT LEAD
            open_edit_form(lead_id)

            print("Edit form opened.")

            # UPDATE CITY
            update_city(NEW_CITY)

            print("City update submitted.")

            # ==========================================
            # VERIFY SAVED CITY
            # ==========================================

            print("Reopening record to verify saved City...")

            open_edit_form(lead_id)

            city_field = wait.until(
                EC.visibility_of_element_located(
                    (By.NAME, "city")
                )
            )

            saved_city = city_field.get_attribute("value")

            if saved_city.strip() == NEW_CITY:

                print("TEST PASSED: City update verified.")
                print(f"Lead ID: {lead_id}")
                print(f"Saved City: {saved_city}")

                passed += 1

                results.append(
                    {
                        "id": lead_id,
                        "name": lead_name,
                        "status": "PASS",
                        "city": saved_city,
                    }
                )

            else:

                print("TEST FAILED: City value did not match.")
                print(f"Expected: {NEW_CITY}")
                print(f"Actual: {saved_city}")

                failed += 1

                results.append(
                    {
                        "id": lead_id,
                        "name": lead_name,
                        "status": "FAIL",
                        "city": saved_city,
                    }
                )

            # CLOSE VERIFICATION FORM
            city_field.send_keys(Keys.ESCAPE)

            wait.until(
                EC.invisibility_of_element_located(
                    (By.NAME, "city")
                )
            )

        except Exception as error:

            print("TEST FAILED for this record.")
            print("Error type:", type(error).__name__)
            print("Error details:", error)

            failed += 1

            results.append(
                {
                    "id": lead_id,
                    "name": lead_name,
                    "status": "FAIL",
                    "city": str(error),
                }
            )

            # ATTEMPT TO CLOSE REMAINING FORM
            try:

                active_city = driver.find_elements(
                    By.NAME, "city"
                )

                if active_city and active_city[0].is_displayed():

                    active_city[0].send_keys(Keys.ESCAPE)

            except Exception:
                pass

    # ==========================================
    # STEP 8: FINAL TEST SUMMARY
    # ==========================================

    print()
    print("=" * 50)
    print("TC-TELE-04: FINAL TEST SUMMARY")
    print("=" * 50)

    for result in results:

        print(
            f"{result['id']} | "
            f"{result['name']} | "
            f"{result['status']}"
        )

    print("------------------------------------------")
    print(f"Total records tested: {len(LEADS)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print("------------------------------------------")

    if passed == 10 and failed == 0:

        print("TC-TELE-04: TEST PASSED")
        print("All 10 lead City updates were saved")
        print("and verified on their correct records.")

    else:

        print("TC-TELE-04: TEST FAILED")
        print("One or more lead City updates were not verified.")

    print("=" * 50)

    # ==========================================
    # STEP 9: CAPTURE SCREENSHOT
    # ==========================================

    screenshot_name = "TC-TELE-04_Update_Leads.png"

    driver.save_screenshot(screenshot_name)

    print(f"Screenshot saved: {screenshot_name}")

# ==========================================
# ERROR HANDLING
# ==========================================

except TimeoutException as error:

    print()
    print("=" * 50)
    print("TC-TELE-04: TEST EXECUTION ERROR")
    print("------------------------------------------")
    print("A required element did not appear in time.")
    print("Current URL:", driver.current_url)
    print("Error details:", error)
    print("=" * 50)

except Exception as error:

    print()
    print("=" * 50)
    print("TC-TELE-04: TEST EXECUTION ERROR")
    print("------------------------------------------")
    print("Error type:", type(error).__name__)
    print("Error details:", error)
    print("=" * 50)

finally:

    input("\nPress Enter to close the browser...")
    driver.quit()

