# 📱 WhatsApp Bulk Messenger

A user-friendly web application for sending bulk messages to multiple WhatsApp contacts with support for text messages and media attachments.

## ✨ Features

- 📁 **Excel File Upload**: Upload Excel files containing phone numbers
- 📝 **Multi-line Text Messages**: Write custom messages with line breaks
- 📎 **Media Support**: Attach images, videos, and documents (no file size limit)
- 🤖 **Automated Sending**: Fully automated WhatsApp Web integration
- 📱 **Unsaved Numbers**: Send to numbers not in your contact list
- ⏱️ **Human-like Behavior**: Random delays (1-5 seconds) between messages
- 📊 **Progress Tracking**: Real-time progress updates and success/failure reports
- 🎨 **Beautiful UI**: Modern and intuitive web interface

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Chrome browser
- WhatsApp account with active phone number

### Installation

1. **Clone or download this repository:**
   ```bash
   git clone <repository-url>
   cd whatsapp-bulk-messenger
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser:**
   The app will automatically open at `http://localhost:8501`

## 📋 Usage Instructions

### Step 1: Prepare Your Excel File
- Create an Excel file (.xlsx or .xls) with phone numbers in one column
- Phone numbers should include country code (e.g., +1234567890, 919876543210)
- Example format:
  ```
  Phone Numbers
  +1234567890
  +1987654321
  919876543210
  ```

### Step 2: Use the Web Application

1. **Upload Excel File**:
   - Click "Upload Excel file with phone numbers"
   - Select your Excel file
   - Choose the column containing phone numbers from the dropdown

2. **Write Your Message**:
   - Enter your text message in the text area
   - Use line breaks for multi-line messages

3. **Upload Media (Optional)**:
   - Click "Upload image/video (optional)"
   - Select image, video, or document files
   - Supported formats: JPG, PNG, GIF, MP4, AVI, MOV, PDF, DOC, DOCX

4. **Start Automation**:
   - Click "🎯 Done - Start Automation"
   - A new Chrome browser window will open with WhatsApp Web

5. **Login to WhatsApp**:
   - Scan the QR code with your phone's WhatsApp app
   - Wait for WhatsApp Web to load completely
   - Click "✅ I've logged in, start sending messages" in the web app

6. **Monitor Progress**:
   - Watch the real-time progress bar
   - View success/failure status for each number
   - See final statistics when complete

## 📱 Phone Number Format

The app accepts various phone number formats:
- `+1234567890` (with country code and +)
- `1234567890` (with country code, no +)
- `919876543210` (India example with country code)

**Important**: Always include the country code for best results.

## ⚠️ Important Notes

- **Keep WhatsApp Active**: Make sure WhatsApp is active on your phone during the process
- **Browser Window**: Don't close the Chrome browser window during automation
- **Rate Limiting**: The app includes random delays to avoid being flagged by WhatsApp
- **Account Safety**: Use responsibly to avoid WhatsApp account restrictions
- **Media Files**: Large media files are supported but may take longer to upload

## 🛠️ Technical Details

### Dependencies
- **Streamlit**: Web interface framework
- **Selenium**: Browser automation
- **Pandas**: Excel file processing
- **WebDriver Manager**: Automatic Chrome driver management

### File Structure
```
whatsapp-bulk-messenger/
├── app.py              # Main application
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

### Chrome Driver
The app automatically downloads and manages the Chrome driver using `webdriver-manager`. No manual driver installation required.

## 🔧 Troubleshooting

### Common Issues

1. **Chrome Driver Error**:
   - Make sure Google Chrome is installed
   - Update Chrome to the latest version
   - Restart the application

2. **WhatsApp Web Not Loading**:
   - Check internet connection
   - Clear Chrome cache and cookies
   - Try refreshing the browser

3. **Messages Not Sending**:
   - Verify phone numbers include country codes
   - Check WhatsApp Web is fully loaded
   - Ensure you're logged in correctly

4. **Excel File Issues**:
   - Verify file format (.xlsx or .xls)
   - Check column contains valid phone numbers
   - Remove empty rows from Excel file

### Error Messages

- **"Invalid phone number"**: Add country code to the number
- **"Timeout"**: WhatsApp Web is slow, try again
- **"Could not send media"**: Media file may be corrupted or too large

## 🚨 Disclaimer

This tool is for educational and legitimate business purposes only. Users are responsible for:
- Complying with WhatsApp's Terms of Service
- Respecting recipient privacy and consent
- Following anti-spam regulations in their jurisdiction
- Using the tool responsibly to avoid account restrictions

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all prerequisites are met
3. Ensure your Excel file format is correct
4. Make sure phone numbers include country codes

## 🔄 Updates

Keep the application updated by pulling the latest changes from the repository and reinstalling dependencies if needed.

---

**Happy Messaging! 📱✨**
