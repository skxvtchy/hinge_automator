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
    safe = text.replace(" ", "%s")
    driver.execute_script(
        "mobile: shell",
        {
            "command": "input",
            "args": ["text", safe]
        }
    )



def swipe_profile(
    driver,
    screen_width: int,
    retries: int = 2,
    delay_seconds: float = 0.2,
) -> None:
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
        for attempt in range(1, retries + 1):
            try:
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
                break
            except WebDriverException:
                if attempt == retries:
                    raise
                time.sleep(delay_seconds)
        time.sleep(random.uniform(0.01, 0.03))


def safe_screenshot(driver, path: str, retries: int = 3, delay_seconds: float = 0.2) -> None:
    for attempt in range(1, retries + 1):
        try:
            driver.save_screenshot(path)
            return
        except WebDriverException:
            if attempt == retries:
                raise
            time.sleep(delay_seconds)
