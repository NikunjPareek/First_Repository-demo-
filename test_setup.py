#!/usr/bin/env python3
"""
Test script to verify WhatsApp Bulk Sender setup
"""

import sys
import importlib

def test_imports():
    """Test if all required modules can be imported"""
    required_modules = [
        'selenium',
        'pandas', 
        'openpyxl',
        'webdriver_manager',
        'PIL',
        'logging'
    ]
    
    print("Testing module imports...")
    failed_imports = []
    
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n❌ Failed to import: {', '.join(failed_imports)}")
        print("Please install missing dependencies:")
        print("pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All modules imported successfully!")
        return True

def test_chrome_driver():
    """Test Chrome WebDriver setup"""
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.chrome import ChromeDriverManager
        
        print("\nTesting Chrome WebDriver setup...")
        
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Install and setup ChromeDriver
        service = Service(ChromeDriverManager().install())
        
        # Create driver
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Test basic functionality
        driver.get("https://www.google.com")
        title = driver.title
        driver.quit()
        
        print(f"✅ Chrome WebDriver working! Tested with: {title}")
        return True
        
    except Exception as e:
        print(f"❌ Chrome WebDriver test failed: {e}")
        print("Please ensure Google Chrome is installed on your system")
        return False

def test_excel_processing():
    """Test Excel file processing"""
    try:
        import pandas as pd
        
        print("\nTesting Excel processing...")
        
        # Create a simple test DataFrame
        test_data = {
            'phone_number': ['+1234567890', '+1987654321'],
            'name': ['Test User 1', 'Test User 2']
        }
        df = pd.DataFrame(test_data)
        
        # Test saving and reading
        test_file = 'test_contacts.xlsx'
        df.to_excel(test_file, index=False)
        
        # Read back
        df_read = pd.read_excel(test_file)
        
        # Clean up
        import os
        os.remove(test_file)
        
        print("✅ Excel processing working!")
        return True
        
    except Exception as e:
        print(f"❌ Excel processing test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("WhatsApp Bulk Sender - Setup Test")
    print("=" * 40)
    
    tests = [
        ("Module Imports", test_imports),
        ("Chrome WebDriver", test_chrome_driver),
        ("Excel Processing", test_excel_processing)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 40)
    print("Test Results:")
    print("=" * 40)
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 All tests passed! Your setup is ready.")
        print("You can now run the WhatsApp Bulk Sender:")
        print("python whatsapp_bulk_sender.py contacts.xlsx 'Your message'")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        print("Common solutions:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Install Google Chrome browser")
        print("3. Check your internet connection")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)