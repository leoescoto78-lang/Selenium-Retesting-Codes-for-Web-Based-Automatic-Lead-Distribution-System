from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# ==========================================
# TC-TELE-01: VERIFY ASSIGNED LEADS
# ==========================================

EMAIL = "secbtelemarketer@gmail.com"
PASSWORD = "TelemarketerSectionB123!"

EXPECTED_LEADS = [
    "b9ea", "b9ec", "b9ef", "b9f0", "b9f1",
    "b9f3", "b9f4", "b9f5", "b9f6", "b9f7"
]

EXPECTED_LEAD_COUNT = 10

# ==========================================
# OPEN CHROME
# ==========================================

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--force-device-scale-factor=1")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 60)

try:

    driver.get(
        "https://sortrleaddistribution-client.onrender.com/"
    )

    # ZOOM OUT
    driver.execute_script(
        "document.body.style.zoom='80%'"
    )

    # LOGIN
    wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input[type="email"]')
        )
    ).send_keys(EMAIL)

    driver.find_element(
        By.CSS_SELECTOR, 'input[type="password"]'
    ).send_keys(PASSWORD)

    wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[normalize-space()='Log In']")
        )
    ).click()

    wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[normalize-space()='DASHBOARD']")
        )
    )

    # OPEN LEADS
    wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//li[contains(@class,'ps-menuitem-root')]"
                "[.//*[normalize-space()='Leads']]"
            )
        )
    ).click()

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

    # VERIFY TARGET LEAD IDS
    found_leads = []

    for lead_id in EXPECTED_LEADS:

        lead_locator = (
            By.XPATH,
            f"//*[normalize-space()='{lead_id}']"
        )

        if driver.find_elements(*lead_locator):
            found_leads.append(lead_id)

    actual_lead_count = len(found_leads)

    missing_leads = [
        lead_id for lead_id in EXPECTED_LEADS
        if lead_id not in found_leads
    ]

    # TEST RESULT
    print("\nTC-TELE-01: VERIFY ASSIGNED LEADS")
    print("-----------------------------------")
    print(f"Expected assigned leads: {EXPECTED_LEAD_COUNT}")
    print(f"Verified assigned leads: {actual_lead_count}")

    if actual_lead_count == EXPECTED_LEAD_COUNT:

        print("BUG RETEST: PASSED")
        print("All 10 target leads were found.")

    else:

        print("BUG RETEST: FAILED")
        print(f"Missing lead IDs: {missing_leads}")

    print("-----------------------------------")

    # SCREENSHOT
    screenshot_name = "TC-TELE-01_Assigned_Leads.png"
    driver.save_screenshot(screenshot_name)

    print(f"Screenshot saved: {screenshot_name}")
    print("-----------------------------------")

except TimeoutException as error:

    print("\nTC-TELE-01: TEST EXECUTION ERROR")
    print("A required page element did not appear.")
    print("Current URL:", driver.current_url)
    print(error)

except Exception as error:

    print("\nTC-TELE-01: TEST EXECUTION ERROR")
    print(error)

finally:

    input("\nPress Enter to close the browser...")
    driver.quit()
