# WhatsApp Bulk Message Sender

A powerful Python automation tool that sends bulk WhatsApp messages from an Excel file of contacts. The script supports sending text messages, images, and videos with human-like behavior to avoid detection.

## Features

- ✅ **Excel Contact Processing**: Extracts phone numbers from Excel files
- ✅ **Text Messages**: Send multi-line text messages
- ✅ **Media Support**: Send images and videos (no file size limit)
- ✅ **Human-like Behavior**: Random delays and natural typing patterns
- ✅ **Contact Handling**: Works with both saved and unsaved contacts
- ✅ **No Restrictions**: No limits on number of contacts or messages
- ✅ **Browser Automation**: Uses Selenium with Chrome WebDriver
- ✅ **Comprehensive Logging**: Detailed logs for monitoring progress
- ✅ **Error Handling**: Robust error handling and recovery

## Prerequisites

- Python 3.7 or higher
- Google Chrome browser
- WhatsApp account
- Excel file with contact numbers

## Installation

1. **Clone or download the project files**

2. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure Google Chrome is installed** on your system

## Excel File Format

Your Excel file should contain phone numbers in one of these column names:
- `phone`
- `phone_number`
- `mobile`
- `mobile_number`
- `contact`
- `number`

If none of these column names are found, the script will use the first column.

### Example Excel Structure:
```
phone_number    | name
+1234567890    | John Doe
+1987654321    | Jane Smith
+1122334455    | Bob Johnson
```

**Important**: Phone numbers should include country code (e.g., +1 for US, +44 for UK, etc.)

## Usage

### Basic Usage (Text Only)
```bash
python whatsapp_bulk_sender.py contacts.xlsx "Hello! This is a test message."
```

### With Image
```bash
python whatsapp_bulk_sender.py contacts.xlsx "Check out this image!" --image /path/to/image.jpg
```

### With Video
```bash
python whatsapp_bulk_sender.py contacts.xlsx "Watch this video!" --video /path/to/video.mp4
```

### With Both Image and Video
```bash
python whatsapp_bulk_sender.py contacts.xlsx "Here's some media content!" --image /path/to/image.jpg --video /path/to/video.mp4
```

### Headless Mode (No Browser UI)
```bash
python whatsapp_bulk_sender.py contacts.xlsx "Automated message" --headless
```

## Command Line Arguments

- `excel_path`: Path to your Excel file with contacts
- `message`: Text message to send (supports multi-line)
- `--image`: Optional path to image file
- `--video`: Optional path to video file
- `--headless`: Run browser in headless mode (no visible browser)

## How It Works

1. **Setup**: Launches Chrome browser and opens WhatsApp Web
2. **Login**: You'll need to scan the QR code to login to WhatsApp Web
3. **Contact Processing**: Reads phone numbers from Excel file
4. **Message Sending**: For each contact:
   - Searches for the contact (works with saved and unsaved contacts)
   - Sends text message with human-like typing delays
   - Sends image/video if provided
   - Adds random delays between actions
5. **Logging**: Provides detailed progress logs

## Human-like Behavior Features

- **Random Delays**: 2-5 seconds between actions
- **Natural Typing**: Random delays between characters (0.01-0.05 seconds)
- **Contact Processing**: 3-8 seconds between different contacts
- **Anti-Detection**: Disabled automation flags and custom user agent

## Important Notes

### ⚠️ WhatsApp Terms of Service
- This tool is for educational purposes
- Respect WhatsApp's terms of service
- Don't spam or send unsolicited messages
- Use responsibly and ethically

### 🔒 Privacy and Security
- Your WhatsApp session remains private
- No data is stored or transmitted
- All processing happens locally

### 📱 WhatsApp Web Requirements
- Your phone must be connected to the internet
- WhatsApp Web session must remain active
- Don't log out of WhatsApp Web during automation

### 🚀 Performance Tips
- Use headless mode for faster execution
- Keep your computer awake during automation
- Ensure stable internet connection
- Don't use too frequently to avoid rate limiting

## Troubleshooting

### Common Issues

1. **Chrome Driver Issues**
   ```bash
   # Reinstall Chrome or update ChromeDriver
   pip install --upgrade webdriver-manager
   ```

2. **WhatsApp Web Not Loading**
   - Check internet connection
   - Clear browser cache
   - Try refreshing the page

3. **Contact Not Found**
   - Ensure phone numbers include country code
   - Check if numbers are in correct format
   - Verify Excel file format

4. **Media Upload Issues**
   - Check file path is correct
   - Ensure file exists and is accessible
   - Try with smaller file sizes first

### Log Files
- Check `whatsapp_sender.log` for detailed error information
- Logs include timestamps and error details

## File Structure

```
whatsapp-bulk-sender/
├── whatsapp_bulk_sender.py    # Main automation script
├── requirements.txt            # Python dependencies
├── README.md                  # This file
├── sample_contacts.xlsx       # Example Excel file
└── whatsapp_sender.log       # Generated log file
```

## Example Output

```
2024-01-15 10:30:15 - INFO - Chrome WebDriver setup completed successfully
2024-01-15 10:30:20 - INFO - Opened WhatsApp Web
2024-01-15 10:30:25 - INFO - Please scan the QR code to login to WhatsApp Web...
2024-01-15 10:31:10 - INFO - Successfully logged into WhatsApp Web
2024-01-15 10:31:15 - INFO - Loaded Excel file: contacts.xlsx
2024-01-15 10:31:16 - INFO - Extracted 3 phone numbers from Excel
2024-01-15 10:31:16 - INFO - Starting bulk message sending to 3 contacts
2024-01-15 10:31:20 - INFO - Processing contact 1/3: +1234567890
2024-01-15 10:31:25 - INFO - Found and selected contact: +1234567890
2024-01-15 10:31:30 - INFO - Text message sent successfully
2024-01-15 10:31:35 - INFO - Successfully sent message to +1234567890
...
2024-01-15 10:35:00 - INFO - Bulk messaging completed!
2024-01-15 10:35:00 - INFO - Successfully sent: 3
2024-01-15 10:35:00 - INFO - Failed: 0
```

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this tool.

## License

This project is for educational purposes. Please use responsibly and in accordance with WhatsApp's terms of service.

## Disclaimer

This tool is provided as-is for educational purposes. Users are responsible for complying with WhatsApp's terms of service and applicable laws. The authors are not responsible for any misuse of this tool.
