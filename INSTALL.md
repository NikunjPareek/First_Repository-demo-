# Installation Guide

This guide will help you set up the WhatsApp Bulk Sender on your system.

## System Requirements

- Python 3.7 or higher
- Google Chrome browser
- Internet connection
- WhatsApp account

## Step-by-Step Installation

### 1. Install System Dependencies

#### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install -y python3-venv python3-pip python3-dev
```

#### CentOS/RHEL:
```bash
sudo yum install -y python3-venv python3-pip python3-devel
```

#### macOS:
```bash
# Install Homebrew if you haven't already
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python3
```

#### Windows:
- Download Python from https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation

### 2. Install Google Chrome

#### Ubuntu/Debian:
```bash
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt update
sudo apt install -y google-chrome-stable
```

#### CentOS/RHEL:
```bash
sudo yum install -y google-chrome-stable
```

#### macOS:
- Download from https://www.google.com/chrome/

#### Windows:
- Download from https://www.google.com/chrome/

### 3. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate
```

### 4. Install Python Dependencies

```bash
# Make sure virtual environment is activated
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Test Installation

```bash
# Run the test script
python test_setup.py
```

If all tests pass, you're ready to use the WhatsApp Bulk Sender!

## Quick Start

1. **Prepare your Excel file** with phone numbers:
   ```
   phone_number    | name
   +1234567890    | John Doe
   +1987654321    | Jane Smith
   ```

2. **Run the automation**:
   ```bash
   python whatsapp_bulk_sender.py contacts.xlsx "Hello! This is a test message."
   ```

3. **Scan the QR code** when prompted to login to WhatsApp Web

4. **Watch the automation work!**

## Troubleshooting

### Common Issues

#### 1. "No module named 'selenium'"
```bash
# Make sure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

#### 2. "Chrome WebDriver not found"
```bash
# Install Chrome first, then reinstall webdriver-manager
pip install --upgrade webdriver-manager
```

#### 3. "Permission denied" when installing packages
```bash
# Use virtual environment instead of system packages
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 4. "Excel file not found"
- Make sure the Excel file path is correct
- Use absolute path if needed: `/full/path/to/contacts.xlsx`

#### 5. "WhatsApp Web not loading"
- Check internet connection
- Try refreshing the page
- Clear browser cache

### Getting Help

1. **Check the logs**: Look at `whatsapp_sender.log` for detailed error information
2. **Run tests**: Use `python test_setup.py` to verify your setup
3. **Check examples**: Run `python example_usage.py setup` to create sample files

## Advanced Usage

### Headless Mode (No Browser UI)
```bash
python whatsapp_bulk_sender.py contacts.xlsx "Message" --headless
```

### With Media Files
```bash
python whatsapp_bulk_sender.py contacts.xlsx "Check this out!" --image photo.jpg --video video.mp4
```

### Custom Excel Format
The script automatically detects phone number columns. Supported column names:
- `phone`
- `phone_number`
- `mobile`
- `mobile_number`
- `contact`
- `number`

If none are found, it uses the first column.

## Security Notes

- ✅ All processing happens locally
- ✅ No data is transmitted to external servers
- ✅ Your WhatsApp session remains private
- ⚠️ Use responsibly and ethically
- ⚠️ Respect WhatsApp's terms of service

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Look at the log files for detailed error messages
3. Ensure all dependencies are properly installed
4. Verify your Excel file format is correct
5. Make sure Google Chrome is installed and working

## File Structure

After installation, your directory should look like this:
```
whatsapp-bulk-sender/
├── venv/                     # Virtual environment
├── whatsapp_bulk_sender.py   # Main script
├── requirements.txt           # Dependencies
├── README.md                 # Documentation
├── INSTALL.md               # This file
├── test_setup.py            # Test script
├── example_usage.py         # Examples
├── config.py                # Configuration
├── install.py               # Auto-installer
├── sample_contacts.xlsx     # Sample data
└── whatsapp_sender.log     # Generated logs
```