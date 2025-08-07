import time
import random
import pandas as pd
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
from typing import Optional, List
from urllib.parse import quote

class WhatsAppBulkSender:
    def __init__(self, headless: bool = False):
        """
        Initialize WhatsApp Bulk Sender
        
        Args:
            headless: Whether to run browser in headless mode (not recommended for WhatsApp Web)
        """
        self.driver = None
        self.wait = None
        self.headless = headless
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('whatsapp_bulk_sender.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def setup_driver(self):
        """Setup Chrome WebDriver with necessary options"""
        try:
            chrome_options = Options()
            
            # Add necessary Chrome options
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            # Keep browser session for WhatsApp Web
            chrome_options.add_argument("--user-data-dir=./whatsapp_session")
            
            if self.headless:
                chrome_options.add_argument("--headless")
                
            # Initialize the driver
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.wait = WebDriverWait(self.driver, 20)
            
            self.logger.info("Chrome WebDriver initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to setup Chrome WebDriver: {str(e)}")
            raise
            
    def read_excel_contacts(self, excel_path: str, phone_column: str = None) -> List[str]:
        """
        Read contacts from Excel file
        
        Args:
            excel_path: Path to Excel file
            phone_column: Name of column containing phone numbers (auto-detects if None)
            
        Returns:
            List of phone numbers
        """
        try:
            if not os.path.exists(excel_path):
                raise FileNotFoundError(f"Excel file not found: {excel_path}")
                
            # Read Excel file
            df = pd.read_excel(excel_path)
            self.logger.info(f"Excel file loaded with {len(df)} rows")
            
            # Auto-detect phone column if not specified
            if phone_column is None:
                phone_columns = ['phone', 'mobile', 'number', 'contact', 'whatsapp']
                for col in df.columns:
                    if any(keyword in col.lower() for keyword in phone_columns):
                        phone_column = col
                        break
                        
                if phone_column is None:
                    # Use first column as default
                    phone_column = df.columns[0]
                    
            self.logger.info(f"Using column '{phone_column}' for phone numbers")
            
            # Extract and clean phone numbers
            contacts = []
            for index, row in df.iterrows():
                phone = str(row[phone_column]).strip()
                
                # Clean phone number
                phone = ''.join(filter(str.isdigit, phone))
                
                if len(phone) >= 10:  # Minimum valid phone length
                    # Add country code if not present
                    if not phone.startswith('91') and len(phone) == 10:
                        phone = '91' + phone  # Default to India, modify as needed
                    contacts.append(phone)
                else:
                    self.logger.warning(f"Invalid phone number at row {index + 1}: {row[phone_column]}")
                    
            self.logger.info(f"Extracted {len(contacts)} valid phone numbers")
            return contacts
            
        except Exception as e:
            self.logger.error(f"Error reading Excel file: {str(e)}")
            raise
            
    def login_whatsapp(self):
        """Open WhatsApp Web and wait for user to scan QR code"""
        try:
            self.logger.info("Opening WhatsApp Web...")
            self.driver.get("https://web.whatsapp.com")
            
            # Check if already logged in
            try:
                self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@data-testid='chat-list']")))
                self.logger.info("Already logged in to WhatsApp Web")
                return True
            except TimeoutException:
                pass
                
            # Wait for QR code scan
            self.logger.info("Please scan QR code in the browser to login...")
            
            # Wait for successful login (chat list appears)
            try:
                self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@data-testid='chat-list']")))
                self.logger.info("Successfully logged in to WhatsApp Web")
                time.sleep(3)  # Wait for full load
                return True
            except TimeoutException:
                self.logger.error("Login timeout. Please try again.")
                return False
                
        except Exception as e:
            self.logger.error(f"Error during WhatsApp login: {str(e)}")
            return False
            
    def send_message_to_contact(self, phone_number: str, message: str, 
                              image_path: Optional[str] = None, 
                              video_path: Optional[str] = None) -> bool:
        """
        Send message to a specific contact
        
        Args:
            phone_number: Phone number to send message to
            message: Text message to send
            image_path: Path to image file (optional)
            video_path: Path to video file (optional)
            
        Returns:
            True if message sent successfully, False otherwise
        """
        try:
            # Open chat using phone number
            url = f"https://web.whatsapp.com/send?phone={phone_number}"
            self.driver.get(url)
            
            # Wait for chat to load
            time.sleep(random.uniform(3, 5))
            
            # Check if chat loaded successfully
            try:
                # Wait for message input box
                message_box = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, "//div[@data-testid='conversation-compose-box-input']"))
                )
            except TimeoutException:
                # Try alternative selector
                try:
                    message_box = self.wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='conversation-compose-box-input']"))
                    )
                except TimeoutException:
                    self.logger.error(f"Could not find message box for {phone_number}")
                    return False
            
            # Send media files first if provided
            if image_path or video_path:
                if not self._send_media(image_path, video_path):
                    self.logger.warning(f"Failed to send media to {phone_number}, continuing with text...")
            
            # Send text message if provided
            if message.strip():
                if not self._send_text_message(message_box, message):
                    return False
                    
            self.logger.info(f"Message sent successfully to {phone_number}")
            
            # Random delay between messages (human-like behavior)
            delay = random.uniform(2, 5)
            self.logger.info(f"Waiting {delay:.1f} seconds before next message...")
            time.sleep(delay)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error sending message to {phone_number}: {str(e)}")
            return False
            
    def _send_media(self, image_path: Optional[str] = None, 
                   video_path: Optional[str] = None) -> bool:
        """Send media files (image or video)"""
        try:
            media_path = image_path or video_path
            if not media_path or not os.path.exists(media_path):
                self.logger.error(f"Media file not found: {media_path}")
                return False
                
            # Click attachment button
            attachment_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='clip']"))
            )
            attachment_btn.click()
            time.sleep(1)
            
            # Click on appropriate media option
            if image_path:
                media_btn = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//input[@accept='image/*,video/mp4,video/3gpp,video/quicktime']"))
                )
            else:
                media_btn = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//input[@accept='image/*,video/mp4,video/3gpp,video/quicktime']"))
                )
            
            # Upload file
            media_btn.send_keys(os.path.abspath(media_path))
            time.sleep(2)
            
            # Wait for media to load and click send
            send_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='compose-btn-send']"))
            )
            send_btn.click()
            
            # Wait for media to send
            time.sleep(3)
            return True
            
        except Exception as e:
            self.logger.error(f"Error sending media: {str(e)}")
            return False
            
    def _send_text_message(self, message_box, message: str) -> bool:
        """Send text message"""
        try:
            # Clear any existing text
            message_box.clear()
            
            # Handle multi-line messages
            lines = message.split('\n')
            for i, line in enumerate(lines):
                message_box.send_keys(line)
                if i < len(lines) - 1:  # Not the last line
                    message_box.send_keys(Keys.SHIFT + Keys.ENTER)
            
            # Send message
            message_box.send_keys(Keys.ENTER)
            time.sleep(2)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error sending text message: {str(e)}")
            return False
            
    def send_bulk_messages(self, excel_path: str, message: str, 
                          phone_column: str = None,
                          image_path: Optional[str] = None,
                          video_path: Optional[str] = None,
                          start_from: int = 0,
                          max_messages: Optional[int] = None):
        """
        Send bulk messages to contacts from Excel file
        
        Args:
            excel_path: Path to Excel file containing contacts
            message: Text message to send
            phone_column: Column name containing phone numbers
            image_path: Path to image file (optional)
            video_path: Path to video file (optional)
            start_from: Index to start from (for resuming)
            max_messages: Maximum number of messages to send
        """
        try:
            # Setup driver and login
            self.setup_driver()
            if not self.login_whatsapp():
                self.logger.error("Failed to login to WhatsApp")
                return
                
            # Read contacts
            contacts = self.read_excel_contacts(excel_path, phone_column)
            
            if not contacts:
                self.logger.error("No valid contacts found")
                return
                
            # Apply start_from and max_messages limits
            if start_from > 0:
                contacts = contacts[start_from:]
                self.logger.info(f"Starting from contact {start_from + 1}")
                
            if max_messages:
                contacts = contacts[:max_messages]
                self.logger.info(f"Limited to {max_messages} messages")
                
            self.logger.info(f"Starting bulk message sending to {len(contacts)} contacts...")
            
            successful = 0
            failed = 0
            
            for i, phone in enumerate(contacts, start=start_from + 1):
                self.logger.info(f"Sending message {i}/{len(contacts) + start_from} to {phone}")
                
                if self.send_message_to_contact(phone, message, image_path, video_path):
                    successful += 1
                else:
                    failed += 1
                    
                # Longer random delay every 10 messages
                if i % 10 == 0:
                    delay = random.uniform(10, 20)
                    self.logger.info(f"Taking a longer break: {delay:.1f} seconds...")
                    time.sleep(delay)
                    
            self.logger.info(f"Bulk messaging completed. Successful: {successful}, Failed: {failed}")
            
        except Exception as e:
            self.logger.error(f"Error in bulk messaging: {str(e)}")
        finally:
            if self.driver:
                input("Press Enter to close the browser...")
                self.driver.quit()
                
    def close(self):
        """Close the browser driver"""
        if self.driver:
            self.driver.quit()