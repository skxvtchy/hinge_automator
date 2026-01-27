import random
import time
import os
from typing import Optional, Tuple
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.common.exceptions import NoSuchElementException, WebDriverException

from PIL import Image
import pytesseract

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


def generate_chill_one_liner(profile_text: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is missing from environment.")

    client = OpenAI(api_key=api_key)
    prompt = (
        "Write one super casual, chill, non-cringey one-liner you could say to "
        "someone you just matched with. Keep it short, simple, friendly, and "
        "don't use big words. Don't mention \"vibes\" or any weird words. Do not "
        "use an em dash. Use the profile text for context if helpful. No Interjections\n\n"
        f"Profile text: {profile_text}"
    )

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt,
        max_output_tokens=40,
        temperature=0.7,
    )
    return response.output_text.strip()



def click_random_point(min_x: int, max_x: int, min_y: int, max_y: int) -> None:
    # Pick a random point inside the square
    rand_x = random.randint(min_x, max_x)
    rand_y = random.randint(min_y, max_y)

    # Random duration
    duration = random.randint(20, 100)

    # Click at random point
    driver.execute_script(
        "mobile: clickGesture",
        {"x": rand_x, "y": rand_y, "duration": duration}
    )
    time.sleep(1)


def type_text(text: str) -> None:
    safe = text.replace(" ", "%s")
    driver.execute_script(
        "mobile: shell",
        {
            "command": "input",
            "args": ["text", safe]
        }
    )



def swipe_profile(screen_width: int) -> None:
    # Then perform the swipe
    start_x = int(screen_width * random.uniform(0.45, 0.55))
    start_y = 2021
    end_y = 550

    # Generate small intermediate points for a gentle curve
    points = []
    segments = 5
    for j in range(segments + 1):
        y = start_y - ((start_y - end_y) * j // segments)
        x = start_x + int(30 * (j / segments) * random.choice([-1, 1]))
        points.append((x, y))

    # Execute swipe in small steps
    for k in range(len(points) - 1):
        driver.execute_script(
            "mobile: swipeGesture",
            {
                "direction": "up",
                "percent": 0.9,
                "left": min(points[k][0], points[k+1][0]),
                "top": min(points[k][1], points[k+1][1]),
                "width": abs(points[k+1][0] - points[k][0]) + 1,
                "height": abs(points[k+1][1] - points[k][1]) + 1,
                "speed": random.randint(800, 1200)
            }
        )
        time.sleep(random.uniform(0.05, 0.15))


def safe_screenshot(path: str, retries: int = 3, delay_seconds: float = 0.6) -> None:
    for attempt in range(1, retries + 1):
        try:
            driver.save_screenshot(path)
            return
        except WebDriverException:
            if attempt == retries:
                raise
            time.sleep(delay_seconds)

# Setup
opts = UiAutomator2Options()
opts.platform_name = "Android"
opts.device_name = "Android Emulator"
opts.automation_name = "UiAutomator2"
opts.app_package = "co.hinge.app"
opts.app_activity = "co.hinge.app.ui.AppActivity"
opts.no_reset = True

driver = webdriver.Remote("http://127.0.0.1:4723", options=opts)
driver.implicitly_wait(10)

# Tap example

safe_screenshot("people/screenshot.png")

text = ''

for i in range(6):  # 6 swipes
    # Take screenshot first
    safe_screenshot(f"people/screenshot_{i}.png")
    img = Image.open(f"people/screenshot_{i}.png")

    # Read text and filter out system/debug lines
    lines = pytesseract.image_to_string(img).splitlines()
    filtered_lines = [
        line for line in lines
        if not any(keyword in line for keyword in ["P:0/1", "dX:", "GY2=", "Xv:", "Yv:", "Prono", "Size:"])
    ]
    screenshot_text = " ".join(filtered_lines).replace("©", "").strip()
    text += screenshot_text + " "

    swipe_profile(driver.get_window_size()["width"])

one_liner = generate_chill_one_liner(text)

click_random_point(916, 960, 1800, 1900)
swipe_profile(driver.get_window_size()["width"])
click_random_point(150, 900, 1900, 2000)


type_text(type_text(one_liner.replace(" ", "%s").encode("ascii", "ignore").decode()))
print(text)
print(one_liner)

click_random_point(87, 172, 2021, 2113)

driver.quit()
