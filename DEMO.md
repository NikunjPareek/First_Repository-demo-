# 🎬 Quick Demo Guide

## How to Test the WhatsApp Bulk Messenger

### 1. Start the Application
```bash
# Method 1: Use the run script
./run_app.sh

# Method 2: Manual start
source whatsapp_env/bin/activate
streamlit run app.py
```

### 2. Test with Sample Data
1. **Use the included sample file**: `sample_contacts.xlsx`
2. **Upload the sample file** in the web interface
3. **Select "Phone Numbers" column** from the dropdown
4. **Enter a test message** like:
   ```
   Hello! This is a test message from the WhatsApp Bulk Messenger.
   
   Best regards,
   Your Name
   ```

### 3. Test Features
- ✅ **Excel Upload**: Upload `sample_contacts.xlsx`
- ✅ **Column Selection**: Choose phone number column
- ✅ **Message Input**: Multi-line text support
- ✅ **Media Upload**: Try uploading an image (optional)
- ✅ **Validation**: App checks for required fields
- ✅ **UI Elements**: Progress bars, success/error messages

### 4. Safety Testing
⚠️ **Important**: For actual testing with real numbers:
- Use only your own phone numbers
- Test with 1-2 numbers first
- Ensure you have permission to message recipients
- Be aware of WhatsApp's rate limiting policies

### 5. Expected Flow
1. Upload Excel file → Preview appears
2. Select phone column → Numbers count updates
3. Enter message → Message length counter updates
4. Click "Done" → Browser opens with WhatsApp Web
5. Scan QR code → Login to WhatsApp
6. Confirm login → Automation starts
7. Watch progress → Real-time updates
8. View results → Success/failure summary

### 6. Troubleshooting Quick Checks
- ✅ Chrome browser installed
- ✅ Python 3.8+ available
- ✅ All dependencies installed
- ✅ Internet connection active
- ✅ WhatsApp account ready for QR scan

Happy Testing! 🚀