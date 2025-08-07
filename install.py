#!/usr/bin/env python3
"""
Installation script for WhatsApp Bulk Sender
Automatically sets up the environment and installs dependencies
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    else:
        print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
        return True

def install_dependencies():
    """Install required Python packages"""
    print("\n📦 Installing dependencies...")
    
    try:
        # Upgrade pip first
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        
        # Install requirements
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        
        print("✅ Dependencies installed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_chrome():
    """Check if Google Chrome is installed"""
    system = platform.system().lower()
    
    chrome_paths = {
        'linux': [
            '/usr/bin/google-chrome',
            '/usr/bin/chromium-browser',
            '/usr/bin/chromium'
        ],
        'darwin': [
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            '/Applications/Chromium.app/Contents/MacOS/Chromium'
        ],
        'windows': [
            r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
        ]
    }
    
    paths = chrome_paths.get(system, [])
    
    for path in paths:
        if os.path.exists(path):
            print(f"✅ Google Chrome found at: {path}")
            return True
    
    print("⚠️  Google Chrome not found in standard locations")
    print("Please install Google Chrome manually:")
    
    if system == 'linux':
        print("Ubuntu/Debian: sudo apt install google-chrome-stable")
        print("CentOS/RHEL: sudo yum install google-chrome-stable")
    elif system == 'darwin':
        print("Download from: https://www.google.com/chrome/")
    elif system == 'windows':
        print("Download from: https://www.google.com/chrome/")
    
    return False

def create_sample_files():
    """Create sample files for testing"""
    print("\n📄 Creating sample files...")
    
    try:
        # Create sample Excel file
        import pandas as pd
        
        sample_data = {
            'phone_number': ['+1234567890', '+1987654321', '+1122334455'],
            'name': ['John Doe', 'Jane Smith', 'Bob Johnson']
        }
        
        df = pd.DataFrame(sample_data)
        df.to_excel("sample_contacts.xlsx", index=False)
        print("✅ Created sample_contacts.xlsx")
        
        # Create sample image
        from PIL import Image
        img = Image.new('RGB', (100, 100), color='red')
        img.save("sample_image.jpg")
        print("✅ Created sample_image.jpg")
        
        # Create placeholder video file
        with open("sample_video.mp4", "w") as f:
            f.write("This is a placeholder video file")
        print("✅ Created sample_video.mp4 (placeholder)")
        
    except Exception as e:
        print(f"⚠️  Could not create sample files: {e}")

def run_tests():
    """Run the test script to verify installation"""
    print("\n🧪 Running tests...")
    
    try:
        result = subprocess.run([sys.executable, "test_setup.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ All tests passed!")
            return True
        else:
            print("❌ Some tests failed:")
            print(result.stdout)
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Could not run tests: {e}")
        return False

def main():
    """Main installation function"""
    print("WhatsApp Bulk Sender - Installation")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Check Chrome
    chrome_ok = check_chrome()
    
    # Create sample files
    create_sample_files()
    
    # Run tests
    tests_ok = run_tests()
    
    print("\n" + "=" * 40)
    print("Installation Summary:")
    print("=" * 40)
    print(f"Python Version: {'✅' if check_python_version() else '❌'}")
    print(f"Dependencies: {'✅' if install_dependencies() else '❌'}")
    print(f"Google Chrome: {'✅' if chrome_ok else '⚠️'}")
    print(f"Tests: {'✅' if tests_ok else '❌'}")
    
    if tests_ok:
        print("\n🎉 Installation completed successfully!")
        print("\nNext steps:")
        print("1. Run: python whatsapp_bulk_sender.py sample_contacts.xlsx 'Your message'")
        print("2. Scan the QR code when prompted")
        print("3. Watch the automation work!")
        
        print("\nExample usage:")
        print("python whatsapp_bulk_sender.py sample_contacts.xlsx 'Hello World!'")
        print("python whatsapp_bulk_sender.py contacts.xlsx 'Check this out!' --image photo.jpg")
        print("python whatsapp_bulk_sender.py contacts.xlsx 'Video message' --video video.mp4 --headless")
        
    else:
        print("\n❌ Installation completed with issues.")
        print("Please check the errors above and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()