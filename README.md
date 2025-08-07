# WhatsApp Bulk Message Sender

A Python automation script for sending bulk WhatsApp messages from an Excel contact list. This tool uses WhatsApp Web through browser automation to send text messages, images, and videos to multiple contacts with human-like behavior patterns.

## ⚠️ Important Disclaimer

This tool is for educational and legitimate business purposes only. Please ensure you:
- Have explicit consent from recipients before sending messages
- Comply with WhatsApp's Terms of Service
- Follow local spam and privacy laws
- Use responsibly and ethically

## 🚀 Features

- ✅ **Excel Integration**: Read contacts from Excel files (.xlsx, .xls)
- ✅ **Text Messages**: Send multi-line text messages
- ✅ **Media Support**: Send images and videos (any file size)
- ✅ **Smart Detection**: Auto-detect phone number columns
- ✅ **Human-like Behavior**: Random delays between messages
- ✅ **Resume Capability**: Start from specific contact index
- ✅ **Error Handling**: Comprehensive logging and error handling
- ✅ **Session Persistence**: Saves WhatsApp Web login session
- ✅ **No Contact Limit**: Send to unlimited number of contacts
- ✅ **Unsaved Contacts**: Works with phone numbers not in contact list

## 📋 Prerequisites

1. **Python 3.7+** installed on your system
2. **Google Chrome** browser installed
3. **ChromeDriver** (automatically managed by webdriver-manager)
4. **WhatsApp Account** with access to WhatsApp Web

## 🔧 Installation

1. **Clone or download this repository**
```bash
git clone <repository-url>
cd whatsapp-bulk-sender
```

2. **Install required dependencies**
```bash
pip install -r requirements.txt
```

3. **Verify installation**
```bash
python -c "import selenium, pandas; print('Dependencies installed successfully!')"
```

## 📁 File Structure

```
whatsapp-bulk-sender/
├── whatsapp_bulk_sender.py    # Main automation class
├── example_usage.py           # Example usage scripts
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── whatsapp_session/          # Browser session data (auto-created)
└── whatsapp_bulk_sender.log   # Log file (auto-created)
```

## 📊 Excel File Format

Your Excel file should contain phone numbers in one of these column formats:

| Column Names (auto-detected) | Example Data |
|------------------------------|--------------|
| phone, mobile, number, contact, whatsapp | 9876543210 |
| Phone Number | +91 98765 43210 |
| Mobile | 919876543210 |

**Example Excel structure:**
```
| Name       | Phone      | Email             |
|------------|------------|-------------------|
| John Doe   | 9876543210 | john@example.com  |
| Jane Smith | 8765432109 | jane@example.com  |
```

## 🎯 Quick Start

### Method 1: Using the Example Script

1. **Run the example script:**
```bash
python example_usage.py
```

2. **Choose option 2 to create a sample Excel file**

3. **Update the sample file with real phone numbers**

4. **Run the script again and choose option 1**

### Method 2: Direct Usage

```python
from whatsapp_bulk_sender import WhatsAppBulkSender

# Initialize the sender
sender = WhatsAppBulkSender(headless=False)

# Define your message
message = """Hello! 👋

This is a bulk message from our system.

Have a great day!

Best regards,
Your Company"""

# Send bulk messages
sender.send_bulk_messages(
    excel_path="/path/to/your/contacts.xlsx",
    message=message,
    phone_column=None,  # Auto-detect
    image_path="/path/to/image.jpg",  # Optional
    video_path=None,  # Optional
    start_from=0,
    max_messages=None  # No limit
)
```

## 🔨 Usage Examples

### Text-Only Messages
```python
sender.send_bulk_messages(
    excel_path="contacts.xlsx",
    message="Hello! This is a text message.",
    image_path=None,
    video_path=None
)
```

### Messages with Image
```python
sender.send_bulk_messages(
    excel_path="contacts.xlsx",
    message="Check out this image!",
    image_path="promotional_image.jpg",
    video_path=None
)
```

### Messages with Video
```python
sender.send_bulk_messages(
    excel_path="contacts.xlsx",
    message="Watch our latest video!",
    image_path=None,
    video_path="promo_video.mp4"
)
```

### Resume from Specific Contact
```python
sender.send_bulk_messages(
    excel_path="contacts.xlsx",
    message="Resuming from contact 50...",
    start_from=49,  # Zero-indexed (50th contact)
    max_messages=100
)
```

## ⚙️ Configuration Options

### WhatsAppBulkSender Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `headless` | bool | False | Run browser in background (not recommended) |

### send_bulk_messages Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `excel_path` | str | Required | Path to Excel file with contacts |
| `message` | str | Required | Text message to send |
| `phone_column` | str | None | Column name for phone numbers (auto-detect if None) |
| `image_path` | str | None | Path to image file (optional) |
| `video_path` | str | None | Path to video file (optional) |
| `start_from` | int | 0 | Contact index to start from (for resuming) |
| `max_messages` | int | None | Maximum number of messages to send |

## 🤖 Human-like Behavior Features

- **Random Delays**: 2-5 seconds between individual messages
- **Extended Breaks**: 10-20 seconds every 10 messages
- **Natural Typing**: Simulates human typing patterns
- **Session Persistence**: Maintains login between runs
- **Error Recovery**: Continues on failed messages

## 📝 Logging

The script creates detailed logs in `whatsapp_bulk_sender.log`:

```
2024-01-15 10:30:15 - INFO - Chrome WebDriver initialized successfully
2024-01-15 10:30:20 - INFO - Successfully logged in to WhatsApp Web
2024-01-15 10:30:25 - INFO - Excel file loaded with 100 rows
2024-01-15 10:30:25 - INFO - Extracted 95 valid phone numbers
2024-01-15 10:30:30 - INFO - Message sent successfully to 9876543210
2024-01-15 10:30:35 - INFO - Waiting 3.2 seconds before next message...
```

## 🔧 Troubleshooting

### Common Issues and Solutions

1. **"ChromeDriver not found"**
   - Solution: Install webdriver-manager: `pip install webdriver-manager`

2. **"Excel file not found"**
   - Solution: Use absolute file paths, check file exists

3. **"Could not find message box"**
   - Solution: Check if WhatsApp Web loaded properly, ensure phone number format

4. **"Login timeout"**
   - Solution: Scan QR code faster, check internet connection

5. **"Message sending failed"**
   - Solution: Check phone number format, ensure contact exists or number is valid

### Phone Number Format

The script automatically cleans and formats phone numbers:
- Removes spaces, dashes, and special characters
- Adds country code if missing (default: +91 for India)
- Validates minimum length (10 digits)

**Supported formats:**
- `9876543210`
- `+91 98765 43210`
- `91-9876543210`
- `(987) 654-3210`

## ⚡ Performance Tips

1. **Use smaller batches** for large contact lists (500-1000 at a time)
2. **Monitor for WhatsApp rate limits** - take breaks if needed
3. **Keep browser window visible** for better reliability
4. **Use wired internet connection** for stability
5. **Close other browser instances** to avoid conflicts

## 🛡️ Best Practices

### Security
- Never share your WhatsApp session data
- Use environment variables for sensitive paths
- Run on secure, private networks

### Compliance
- Get explicit consent before messaging
- Include unsubscribe instructions
- Respect recipient preferences
- Follow local privacy laws

### Technical
- Test with small groups first
- Monitor success/failure rates
- Keep backups of contact lists
- Update dependencies regularly

## 🐛 Known Limitations

- Requires manual QR code scan for first login
- May not work in some corporate networks
- WhatsApp Web UI changes may affect functionality
- Large media files may take longer to upload

## 📞 Support

If you encounter issues:

1. Check the log file for detailed error messages
2. Ensure all dependencies are installed correctly
3. Verify your Excel file format matches requirements
4. Test with a single contact first

## 📄 License

This project is provided as-is for educational purposes. Users are responsible for complying with all applicable laws and terms of service.

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

**Happy messaging! 📱✨**
