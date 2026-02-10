import csv
import json
import os
import random
import time
from selenium.common.exceptions import WebDriverException

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

def generate_chill_one_liner(profile_text: str) -> list[str]:
    """Returns [name, opener] parsed from the model's JSON array."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is missing from environment.")

    client = OpenAI(api_key=api_key)

    prompt = (
    "Return a JSON array with exactly two elements:\n"
    "0: the person's name if it appears in the profile text, otherwise an empty string.\n"
    "1: a single natural one-line dating app opener.\n\n"
    "Requirements for the opener:\n"
    "- Relaxed, friendly, human, short, non-cringey.\n"
    "- Use simple everyday words.\n"
    "- Ask at most one light, interesting, or playful question.\n"
    "- Avoid greetings (hi, hey), their name, emojis, slang, interjections, clichés, or an em dash.\n"
    "- Use the profile text for context if helpful.\n"
    "- If the profile text gives nothing useful, write a safe neutral opener.\n"
    "- Each run should aim for diverse phrasing and style, avoid repeating previous formats.\n"
    "- Optionally reference hobbies, interests, or unique details subtly.\n\n"
    "Examples:\n"
    'Profile: "Loves hiking and Italian food" → ["", "Ever tried a mountain hike with pasta at the summit?"]\n'
    'Profile: "Bookworm, coffee addict" → ["", "Which book are you currently lost in over coffee?"]\n\n'
    "Return only the JSON array and nothing else.\n"
    f"Profile text: {profile_text}"
    )


    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt,
        max_output_tokens=40,
        temperature=0.7,
    )
    raw = response.output_text.strip()
    # Handle optional markdown code fence
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
    arr = json.loads(raw)
    if not isinstance(arr, list) or len(arr) != 2:
        raise ValueError(f"Expected 2-element JSON array, got: {raw}")
    return [str(arr[0]), str(arr[1])]


ONE_LINERS_CSV_PATH = "one_liners.csv"


def append_one_liners_to_csv(one_liner_0: str, one_liner_1: str) -> None:
    write_header = not os.path.exists(ONE_LINERS_CSV_PATH)
    with open(ONE_LINERS_CSV_PATH, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if write_header:
            w.writerow(["one_liner_0", "one_liner_1"])
        w.writerow([one_liner_0, one_liner_1])


def click_random_point(driver, min_x: int, max_x: int, min_y: int, max_y: int) -> None:
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
    time.sleep(0.1)



def type_text(driver, text: str) -> None:
    try:
        # 1. Set the device clipboard text
        # This uses Appium's internal helper app to store the string
        driver.set_clipboard_text(text)
        
        # 2. Wait for the UI/Keyboard to be ready after your click
        # Hinge animations need a moment to stabilize
        time.sleep(1.0)
        
        # 3. Trigger the 'Paste' Keyevent (279)
        # This sends the clipboard content to whatever is currently focused
        driver.execute_script(
            "mobile: shell",
            {
                "command": "input",
                "args": ["keyevent", "279"]
            }
        )
        
        # 4. Optional: Hit Enter to confirm (Keyevent 66)
        time.sleep(0.5)
        driver.execute_script("mobile: shell", {"command": "input", "args": ["keyevent", "66"]})
        
        print(f"Successfully pasted: {text}")

    except Exception as e:
        print(f"Clipboard paste failed: {e}")


def swipe_profile(driver, screen_width: int):
    # 1. Randomize the X-coordinate across most of the screen width
    # This ensures the 'tap' and 'drag' happen in different vertical lanes
    random_x = int(screen_width * random.uniform(0.15, 0.85))
    
    # 2. Define the vertical bounds
    start_y = 1500
    end_y = 1000
    swipe_height = start_y - end_y  # 300 pixel travel distance

    try:
        driver.execute_script(
            "mobile: swipeGesture",
            {
                "left": random_x,
                "top": end_y,            # The 'top' is the end of the upward swipe
                "width": 10,             # Keep width tiny to focus on the X-point
                "height": swipe_height,
                "direction": "up",
                "percent": 1.0,          # Drag the full 300px distance
                "speed": 5000           # Ultra-fast pixels per second
            }
        )
        time.sleep(1)
    except Exception as e:
        print(f"Swipe failed: {e}")


def safe_screenshot(driver, path: str, retries: int = 3, delay_seconds: float = 0.2) -> None:
    for attempt in range(1, retries + 1):
        try:
            driver.save_screenshot(path)
            return
        except WebDriverException:
            if attempt == retries:
                raise
            time.sleep(delay_seconds)
