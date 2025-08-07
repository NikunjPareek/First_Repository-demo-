#!/usr/bin/env python3
"""
Setup script for WhatsApp Bulk Sender

This script helps users install dependencies and set up the environment.
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    print("Checking Python version...")
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required.")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version OK: {sys.version}")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("\nInstalling Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def check_chrome():
    """Check if Chrome browser is installed"""
    print("\nChecking for Chrome browser...")
    
    system = platform.system().lower()
    
    if system == "windows":
        chrome_paths = [
            "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
        ]
    elif system == "darwin":  # macOS
        chrome_paths = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]
    else:  # Linux
        chrome_paths = ["/usr/bin/google-chrome", "/usr/bin/chromium-browser"]
    
    for path in chrome_paths:
        if os.path.exists(path):
            print(f"✅ Chrome found at: {path}")
            return True
    
    print("⚠️  Chrome browser not found. Please install Google Chrome.")
    print("Download from: https://www.google.com/chrome/")
    return False

def create_sample_files():
    """Create sample Excel file for testing"""
    print("\nCreating sample files...")
    try:
        import pandas as pd
        
        # Create sample contacts
        contacts = {
            'name': ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Wilson', 'Mike Brown'],
            'phone': ['1234567890', '9876543210', '5555555555', '1111111111', '9999999999'],
            'email': ['john@example.com', 'jane@example.com', 'bob@example.com', 'alice@example.com', 'mike@example.com']
        }
        
        df = pd.DataFrame(contacts)
        df.to_excel('sample_contacts.xlsx', index=False)
        print("✅ Sample Excel file created: sample_contacts.xlsx")
        print("   Please update with real phone numbers before using!")
        
        return True
    except Exception as e:
        print(f"❌ Error creating sample files: {e}")
        return False

def run_tests():
    """Run basic tests to verify installation"""
    print("\nRunning basic tests...")
    try:
        # Test imports
        import selenium
        import pandas as pd
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        print("✅ All imports successful!")
        
        # Test webdriver manager
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            print("✅ WebDriver manager available!")
        except ImportError:
            print("⚠️  WebDriver manager not found, installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "webdriver-manager"])
            print("✅ WebDriver manager installed!")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def show_next_steps():
    """Show user what to do next"""
    print("\n" + "="*50)
    print("🎉 Setup completed successfully!")
    print("="*50)
    print("\n📋 Next steps:")
    print("1. Update sample_contacts.xlsx with real phone numbers")
    print("2. Run: python example_usage.py")
    print("3. Choose option 3 to test with a single message first")
    print("4. Once confirmed working, use option 1 for bulk messaging")
    
    print("\n📖 Quick usage:")
    print("```python")
    print("from whatsapp_bulk_sender import WhatsAppBulkSender")
    print("sender = WhatsAppBulkSender()")
    print("sender.send_bulk_messages(")
    print("    excel_path='sample_contacts.xlsx',")
    print("    message='Hello from WhatsApp bulk sender!'")
    print(")")
    print("```")
    
    print("\n⚠️  Important reminders:")
    print("- Get consent before messaging contacts")
    print("- Test with small groups first")
    print("- Keep browser window visible during execution")
    print("- Check logs if you encounter issues")

def main():
    """Main setup function"""
    print("WhatsApp Bulk Sender - Setup Script")
    print("="*40)
    
    success = True
    
    # Check Python version
    if not check_python_version():
        success = False
    
    # Install dependencies
    if success and not install_dependencies():
        success = False
    
    # Check Chrome
    if success:
        check_chrome()  # Warning only, not critical
    
    # Run tests
    if success and not run_tests():
        success = False
    
    # Create sample files
    if success:
        create_sample_files()
    
    if success:
        show_next_steps()
    else:
        print("\n❌ Setup encountered errors. Please resolve them and try again.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    
    print(f"\nSetup {'completed' if exit_code == 0 else 'failed'}.")
    input("Press Enter to exit...")
    sys.exit(exit_code)