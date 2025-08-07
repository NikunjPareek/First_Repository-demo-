# WhatsApp Web Bulk Sender

Send bulk WhatsApp messages from an Excel contact list using Selenium automation of WhatsApp Web. Supports multi-line text messages and optional image/video attachments, with human-like randomized delays.

## Prerequisites
- Python 3.9+
- Google Chrome (or Chromium) installed

## Install

```bash
pip install -r requirements.txt
```

## Prepare
- On first run, you will be prompted to scan the WhatsApp Web QR in the opened Chrome window.
- A persistent Chrome profile is stored at `.chrome-whatsapp-profile` by default so you usually only scan once.

## Excel format
- Provide an `.xlsx` file.
- The script autodetects a phone number column by common names like `phone`, `mobile`, `number`, `contact`. You can force a column with `--column`.
- Numbers may contain spaces, dashes, parentheses, `+`, or start with `00` – they will be normalized.
- Use `--country-code` (digits only, e.g., `1`, `44`, `91`) to prefix local numbers missing a country code.

## Usage

```bash
python whatsapp_bulk.py \
  --excel /absolute/path/contacts.xlsx \
  --column phone \
  --message-file /absolute/path/message.txt \
  --image /absolute/path/promo.jpg \
  --video /absolute/path/demo.mp4 \
  --country-code 1 \
  --min-delay 3.5 \
  --max-delay 8.0
```

Notes:
- You may use `--message "Line1\\nLine2"` for a multi-line message without a file.
- Either or both of `--image` and `--video` can be supplied. The script does not impose a file size limit, but WhatsApp may enforce its own platform limits.
- Delays are randomized between `--min-delay` and `--max-delay` to mimic human behavior.
- Headless mode is available via `--headless`. You must already be logged in within the specified profile for headless to work.

## Examples

- Text only:
```bash
python whatsapp_bulk.py --excel /abs/contacts.xlsx --column phone --message "Hello!\\nThis is a multi-line test." --country-code 91
```

- Text + image:
```bash
python whatsapp_bulk.py --excel /abs/contacts.xlsx --message-file msg.txt --image /abs/banner.png --country-code 44
```

- Text + video:
```bash
python whatsapp_bulk.py --excel /abs/contacts.xlsx --message "Hi there" --video /abs/clip.mp4 --country-code 1
```

## Tips
- If ChromeDriver fails to launch due to a version mismatch, update Google Chrome or set a compatible ChromeDriver. This project uses `webdriver-manager` to auto-install a matching driver where possible.
- If a number is not registered on WhatsApp, the script logs a warning and continues.
- To re-login with a different account, delete the `.chrome-whatsapp-profile` directory or pass a different `--profile-dir` path.

## Disclaimer
This script automates WhatsApp Web for legitimate use cases. Respect WhatsApp's Terms of Service and local regulations. Excessive messaging may trigger rate limits or account restrictions. The author is not responsible for misuse.
