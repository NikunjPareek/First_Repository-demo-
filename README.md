# WhatsApp Bulk Message Sender

This small utility automates sending WhatsApp messages – plus optional images or videos – to a large list of phone numbers using **WhatsApp&nbsp;Web**.

It operates via Selenium-controlled Chrome, so **no official WhatsApp API or account limitations apply** (besides the usual WhatsApp spam rules – use responsibly!).

---

## Features

* Read unlimited phone numbers from an Excel workbook (.xlsx)
* Send multi-line text messages
* Optionally attach an image and/or video (no enforced size limits)
* Works with unsaved contacts through direct *https://wa.me* links
* Randomised delay between messages to mimic human behaviour
* Persists your WhatsApp login session if you point it at a reusable Chrome profile

## Installation

```bash
# (Recommended) inside a virtual environment
python -m venv .venv && source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

Chrome **must** be installed on the host system. `webdriver-manager` will download a matching ChromeDriver automatically.

## Preparing your Excel file

1. Create an Excel workbook (`.xlsx`).
2. Place phone numbers (including country code, e.g. `15551234567`) in **one column**.
3. Optionally name the column (e.g. `Phone`).

Example:

| Phone |
|--------|
| 15551230001 |
| 919876543210 |
| ... |

## Usage

```bash
python whatsapp_bulk_sender.py \
  --excel contacts.xlsx \
  --message "message.txt"            # or inline string

# Attach an image and a video, use custom sheet/column names, prepend default country code to local numbers
python whatsapp_bulk_sender.py \
  --excel numbers.xlsx \
  --sheet "Customers" \
  --column "Mobile" \
  --default-country-code 91 \
  --message "Hello!\nThis is a multi-line WhatsApp *test*." \
  --image promo.jpg \
  --video demo.mp4
```

Common flags:

* `--headless` – run Chrome without a visible window (login may fail if QR code cannot be scanned)
* `--user-data-dir /path/to/dir` – store Chrome profile to keep you logged in across runs
* `--delay-min 3 --delay-max 7` – control random wait between messages (seconds)

## How it works

1. The script launches Chrome and opens [web.whatsapp.com](https://web.whatsapp.com/).
2. You scan the QR code once. Session cookies are stored in the specified Chrome profile directory.
3. For every phone number in the sheet the script navigates to `https://web.whatsapp.com/send?phone=NUMBER`.
4. It pastes your text, attaches media if provided and hits **Send**.
5. A random pause (default 2–5 s) occurs before processing the next contact.

## Disclaimer

This tool is intended for legitimate notification or outreach purposes. **Do not spam.** Excessive or unsolicited messaging may result in your WhatsApp account being restricted or banned.
