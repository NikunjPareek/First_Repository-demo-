#!/usr/bin/env python3
"""
whatsapp_bulk_sender.py
----------------------
Automates sending WhatsApp messages (and optional images/videos) in bulk based on an Excel
spreadsheet of phone numbers using WhatsApp Web.

Usage:
    python whatsapp_bulk_sender.py --excel contacts.xlsx --message "path_or_inline_message.txt" \
                                   [--image image.jpg] [--video clip.mp4] \
                                   [--sheet "Sheet1"] [--column "Phone"] \
                                   [--delay-min 2] [--delay-max 5] [--headless]

Notes:
    • Supports multi-line messages. If --message points to a readable file, the entire file
      content is used as the message, preserving newline characters.
    • Phone numbers must include country code (e.g. 15551234567). If they do not, provide
      --default-country-code so it will be prepended automatically (without leading '+').
    • The script launches Chrome via Selenium. On first run, you must scan the QR code.
      Your WhatsApp session cookies are stored in the Chrome profile directory so subsequent
      runs will reuse the logged-in session.
"""

import argparse
import os
import random
import sys
import time
from pathlib import Path
from typing import List, Optional

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


# --------------------------- Helper functions --------------------------- #

def read_numbers_from_excel(path: Path, sheet_name: Optional[str] = None, column: Optional[str] = None,
                            default_country_code: Optional[str] = None) -> List[str]:
    """Read phone numbers from an Excel file.

    If *column* is None, the first column is used.
    *default_country_code* (digits only) will be prepended to numbers lacking a country code.
    """
    if not path.exists():
        raise FileNotFoundError(f"Excel file not found: {path}")

    df = pd.read_excel(path, sheet_name=sheet_name, dtype=str)
    if df.empty:
        raise ValueError("Excel sheet is empty")

    if column and column not in df.columns:
        raise ValueError(f"Column '{column}' not found in Excel sheet; available columns: {list(df.columns)}")

    series = df[column] if column else df.iloc[:, 0]
    numbers: List[str] = []
    for raw in series.fillna(""):
        num = "".join(filter(str.isdigit, str(raw)))  # keep digits only
        if not num:
            continue
        if default_country_code and not num.startswith(default_country_code):
            num = f"{default_country_code}{num}"
        numbers.append(num)
    # deduplicate while preserving order
    seen = set()
    unique_numbers = []
    for n in numbers:
        if n not in seen:
            seen.add(n)
            unique_numbers.append(n)
    return unique_numbers


def setup_driver(headless: bool = False, user_data_dir: Optional[str] = None) -> webdriver.Chrome:
    """Create and return a Selenium Chrome WebDriver configured for WhatsApp Web."""
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    if headless:
        chrome_options.add_argument("--headless=new")
    if user_data_dir:
        chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.set_window_size(1200, 900)
    return driver


def wait_for_login(driver: webdriver.Chrome, timeout: int = 60):
    """Wait until WhatsApp Web is logged in or raise TimeoutException."""
    print("🕒 Waiting for WhatsApp Web login… Scan the QR code if presented.")
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[tabindex='-1'][role='textbox']"))
        )
    except TimeoutException:
        raise TimeoutException("Timed out waiting for WhatsApp Web login. Make sure to scan the QR code in time.")
    print("✅ Logged in to WhatsApp Web.")


def random_sleep(min_seconds: float, max_seconds: float):
    duration = random.uniform(min_seconds, max_seconds)
    time.sleep(duration)


def send_text(driver: webdriver.Chrome, message: str):
    """Send a (multi-line) text message in the currently open chat."""
    msg_box = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[tabindex='-1'][role='textbox']"))
    )
    for line in message.split("\n"):
        msg_box.send_keys(line)
        msg_box.send_keys(Keys.SHIFT + Keys.ENTER)
    # Remove the last newline by sending BACKSPACE once (optional)
    msg_box.send_keys(Keys.BACKSPACE)
    msg_box.send_keys(Keys.ENTER)


def send_attachment(driver: webdriver.Chrome, file_path: Path):
    """Attach and send an image or video file in the current chat."""
    if not file_path.exists():
        print(f"⚠️ Attachment not found: {file_path}")
        return
    # Click the clip (attach) button
    clip_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "span[data-testid='clip']"))
    )
    clip_button.click()

    # The input[type='file'] becomes visible after click; accept multiple mime types
    file_input = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file'][accept*='image'], input[type='file'][accept*='video']"))
    )
    file_input.send_keys(str(file_path.resolve()))

    # Wait for preview to load and send
    send_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "span[data-testid='send']"))
    )
    send_button.click()


def process_number(driver: webdriver.Chrome, number: str, message: str,
                   image: Optional[Path], video: Optional[Path], delay_range: tuple[float, float]):
    url = f"https://web.whatsapp.com/send?phone={number}&app_absent=0"
    driver.get(url)
    try:
        # Wait for chat box to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[tabindex='-1'][role='textbox']"))
        )
    except TimeoutException:
        print(f"❌ Failed to open chat for {number}")
        return False

    # Send text message
    if message:
        send_text(driver, message)

    # Send attachments
    if image:
        send_attachment(driver, image)
    if video:
        send_attachment(driver, video)

    random_sleep(*delay_range)
    print(f"✅ Message sent to {number}")
    return True


# --------------------------- Main entry point --------------------------- #

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bulk WhatsApp sender via WhatsApp Web")
    parser.add_argument("--excel", required=True, help="Path to Excel file containing contacts")
    parser.add_argument("--message", required=True,
                        help="Inline text message OR path to .txt file containing the message")
    parser.add_argument("--image", help="Optional path to image file to send")
    parser.add_argument("--video", help="Optional path to video file to send")
    parser.add_argument("--sheet", help="Excel sheet name (default: first sheet)")
    parser.add_argument("--column", help="Column name containing phone numbers (default: first column)")
    parser.add_argument("--default-country-code", help="Digits to prepend to numbers missing country code")
    parser.add_argument("--delay-min", type=float, default=2, help="Minimum random delay between messages (seconds)")
    parser.add_argument("--delay-max", type=float, default=5, help="Maximum random delay between messages (seconds)")
    parser.add_argument("--headless", action="store_true", help="Run Chrome in headless mode (login might fail)")
    parser.add_argument("--user-data-dir", help="Path to Chrome user data dir to persist session")
    return parser.parse_args()


def main():
    args = parse_args()

    excel_path = Path(args.excel).expanduser().resolve()
    image_path = Path(args.image).expanduser().resolve() if args.image else None
    video_path = Path(args.video).expanduser().resolve() if args.video else None

    # Load message (file or inline)
    if os.path.isfile(args.message):
        with open(args.message, "r", encoding="utf-8") as f:
            message_text = f.read().strip()
    else:
        message_text = args.message.replace("\\n", "\n")

    numbers = read_numbers_from_excel(
        excel_path,
        sheet_name=args.sheet,
        column=args.column,
        default_country_code=args.default_country_code,
    )
    if not numbers:
        print("No valid phone numbers found in Excel file.")
        sys.exit(1)

    print(f"Found {len(numbers)} unique numbers to message.")

    driver = setup_driver(headless=args.headless, user_data_dir=args.user_data_dir)

    try:
        driver.get("https://web.whatsapp.com/")
        wait_for_login(driver)

        failures: List[str] = []
        for idx, num in enumerate(numbers, start=1):
            print(f"[{idx}/{len(numbers)}] Processing {num}…")
            try:
                ok = process_number(
                    driver,
                    num,
                    message_text,
                    image_path,
                    video_path,
                    (args.delay_min, args.delay_max),
                )
                if not ok:
                    failures.append(num)
            except Exception as e:
                print(f"❌ Error while messaging {num}: {e}")
                failures.append(num)
                # Continue with next contact

        if failures:
            print("\nSome numbers could not be messaged:")
            for n in failures:
                print(" -", n)
        else:
            print("\nAll messages sent successfully!")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()