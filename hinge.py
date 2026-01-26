import random
import time
import os
from appium import webdriver
from appium.options.android import UiAutomator2Options

from PIL import Image
import pytesseract



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
# Define square bounds
min_x, max_x = 87, 172
min_y, max_y = 2021, 2113

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
time.sleep(1.5)

driver.save_screenshot("people/screenshot.png")

size = driver.get_window_size()
w = size["width"]

text = ''

for i in range(6):  # 6 swipes
    # Take screenshot first
    driver.save_screenshot(f"people/screenshot_{i}.png")
    img = Image.open(f"people/screenshot_{i}.png")

    # Read text and filter out system/debug lines
    lines = pytesseract.image_to_string(img).splitlines()
    filtered_lines = [
        line for line in lines
        if not any(keyword in line for keyword in ["P:0/1", "dX:", "GY2=", "Xv:", "Yv:", "Prono", "Size:"])
    ]
    screenshot_text = " ".join(filtered_lines).replace("©", "").strip()
    text += screenshot_text + " "

    # Then perform the swipe
    start_x = int(w * random.uniform(0.45, 0.55))
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



print(text)

driver.quit()
