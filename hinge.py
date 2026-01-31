import random
import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.common.exceptions import WebDriverException

from PIL import Image
import pytesseract

from hinge_utils import (
    generate_chill_one_liner,
    click_random_point,
    type_text,
    swipe_profile,
    safe_screenshot,
    append_one_liners_to_csv,
)


def run_session(driver) -> None:
    # Tap example
<<<<<<< HEAD
    # safe_screenshot(driver, "people/screenshot.png")

    text = ""

    for i in range(5):  # 5 swipes
=======
    safe_screenshot(driver, "people/screenshot.png")

    text = ""

    for i in range(1):  # 6 swipes
>>>>>>> origin/main
        # Take screenshot first
        safe_screenshot(driver, f"people/screenshot_{i}.png")
        img = Image.open(f"people/screenshot_{i}.png")

        # Read text and filter out system/debug lines
        lines = pytesseract.image_to_string(img).splitlines()
        filtered_lines = [
            line for line in lines
            if not any(keyword in line for keyword in ["P:0/1", "dX:", "GY2=", "Xv:", "Yv:", "Prono", "Size:"])
        ]
        screenshot_text = " ".join(filtered_lines).replace("©", "").strip()
        text += screenshot_text + " "

        swipe_profile(driver, driver.get_window_size()["width"])

    one_liner = generate_chill_one_liner(text)
    print(text)
    print(one_liner)

    click_random_point(driver, 916, 960, 1800, 1900)
    swipe_profile(driver, driver.get_window_size()["width"])
    time.sleep(random.uniform(0.01, 0.03))

    click_random_point(driver, 150, 900, 1900, 2000)

    type_text(driver, one_liner[1].replace(" ", "%s").encode("ascii", "ignore").decode())
    append_one_liners_to_csv(one_liner[0], one_liner[1])

    # click_random_point(driver, 87, 172, 2021, 2113)
    # time.sleep(random.uniform(0.01, 0.03))

    # click_random_point(driver, 470, 920, 2090, 2155)


# Setup driver once and reuse across all sessions
opts = UiAutomator2Options()
opts.platform_name = "Android"
opts.device_name = "Android Emulator"
opts.automation_name = "UiAutomator2"
opts.app_package = "co.hinge.app"
opts.app_activity = "co.hinge.app.ui.AppActivity"
opts.no_reset = True

driver = webdriver.Remote("http://127.0.0.1:4723", options=opts)
driver.implicitly_wait(5)

try:
    for i in range(1):
        try:
            run_session(driver)
        except WebDriverException:
            time.sleep(0.3)
finally:
    driver.quit()