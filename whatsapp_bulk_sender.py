#!/usr/bin/env python3
"""
WhatsApp Bulk Message Sender
Automates sending bulk WhatsApp messages from Excel contacts with text, images, and videos.
"""

import os
import sys
import time
import random
import pandas as pd
from pathlib import Path
from typing import List, Optional, Tuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('whatsapp_sender.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class WhatsAppBulkSender:
    def __init__(self, headless: bool = False):
        """
        Initialize WhatsApp Bulk Sender
        
        Args:
            headless (bool): Run browser in headless mode
        """
        self.driver = None
        self.headless = headless
        self.wait = None
        
    def setup_driver(self):
        """Setup Chrome WebDriver with appropriate options"""
        try:
            chrome_options = Options()
            
            if self.headless:
                chrome_options.add_argument("--headless")
            
            # Additional options for better automation
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            # Disable automation detection
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Execute script to remove webdriver property
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            self.wait = WebDriverWait(self.driver, 30)
            logger.info("Chrome WebDriver setup completed successfully")
            
        except Exception as e:
            logger.error(f"Failed to setup WebDriver: {e}")
            raise
    
    def open_whatsapp_web(self):
        """Open WhatsApp Web and wait for QR code scan"""
        try:
            self.driver.get("https://web.whatsapp.com")
            logger.info("Opened WhatsApp Web")
            
            # Wait for user to scan QR code and load WhatsApp
            logger.info("Please scan the QR code to login to WhatsApp Web...")
            
            # Wait for the main chat list to appear (indicates successful login)
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="chat-list"]'))
            )
            logger.info("Successfully logged into WhatsApp Web")
            
        except Exception as e:
            logger.error(f"Failed to open WhatsApp Web: {e}")
            raise
    
    def extract_contacts_from_excel(self, excel_path: str) -> List[str]:
        """
        Extract phone numbers from Excel file
        
        Args:
            excel_path (str): Path to Excel file
            
        Returns:
            List[str]: List of phone numbers
        """
        try:
            # Read Excel file
            df = pd.read_excel(excel_path)
            logger.info(f"Loaded Excel file: {excel_path}")
            
            # Find phone number column (common column names)
            phone_columns = ['phone', 'phone_number', 'mobile', 'mobile_number', 'contact', 'number']
            phone_col = None
            
            for col in phone_columns:
                if col in df.columns:
                    phone_col = col
                    break
            
            if phone_col is None:
                # If no matching column found, use the first column
                phone_col = df.columns[0]
                logger.warning(f"No standard phone column found. Using first column: {phone_col}")
            
            # Extract phone numbers and clean them
            phone_numbers = []
            for number in df[phone_col].dropna():
                # Clean phone number (remove spaces, dashes, etc.)
                cleaned_number = str(number).replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
                
                # Ensure number starts with country code (add + if missing)
                if not cleaned_number.startswith('+'):
                    cleaned_number = '+' + cleaned_number
                
                phone_numbers.append(cleaned_number)
            
            logger.info(f"Extracted {len(phone_numbers)} phone numbers from Excel")
            return phone_numbers
            
        except Exception as e:
            logger.error(f"Failed to extract contacts from Excel: {e}")
            raise
    
    def search_contact(self, phone_number: str) -> bool:
        """
        Search for a contact by phone number
        
        Args:
            phone_number (str): Phone number to search for
            
        Returns:
            bool: True if contact found and selected, False otherwise
        """
        try:
            # Click on search box
            search_box = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="chat-list-search"]'))
            )
            search_box.click()
            search_box.clear()
            
            # Type phone number
            search_box.send_keys(phone_number)
            time.sleep(2)  # Wait for search results
            
            # Try to find and click on the contact
            try:
                # Look for contact in search results
                contact_element = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="cell-phone-number"]'))
                )
                contact_element.click()
                logger.info(f"Found and selected contact: {phone_number}")
                return True
                
            except:
                # If contact not found, try to start a new chat
                logger.info(f"Contact not found, starting new chat with: {phone_number}")
                search_box.send_keys(Keys.ENTER)
                time.sleep(2)
                return True
                
        except Exception as e:
            logger.error(f"Failed to search contact {phone_number}: {e}")
            return False
    
    def send_text_message(self, message: str):
        """
        Send text message to current contact
        
        Args:
            message (str): Text message to send
        """
        try:
            # Find message input box
            message_box = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="conversation-compose-box-input"]'))
            )
            message_box.click()
            
            # Clear any existing text
            message_box.clear()
            
            # Type message with human-like delays
            for char in message:
                message_box.send_keys(char)
                time.sleep(random.uniform(0.01, 0.05))  # Random delay between characters
            
            # Send message
            message_box.send_keys(Keys.ENTER)
            logger.info("Text message sent successfully")
            
        except Exception as e:
            logger.error(f"Failed to send text message: {e}")
            raise
    
    def send_media_message(self, file_path: str, is_video: bool = False):
        """
        Send media file (image or video) to current contact
        
        Args:
            file_path (str): Path to media file
            is_video (bool): True if file is video, False if image
        """
        try:
            # Click attachment button
            attachment_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="attach-button"]'))
            )
            attachment_button.click()
            time.sleep(1)
            
            # Click on image/video option
            if is_video:
                media_option = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="attach-video"]'))
                )
            else:
                media_option = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="attach-image"]'))
                )
            media_option.click()
            time.sleep(1)
            
            # Find file input and upload file
            file_input = self.driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
            file_input.send_keys(file_path)
            time.sleep(3)  # Wait for file to upload
            
            # Add caption if needed (optional)
            try:
                caption_box = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="media-caption"]')
                if caption_box:
                    caption_box.send_keys("Sent via WhatsApp Bulk Sender")
            except:
                pass
            
            # Send media
            send_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="send"]'))
            )
            send_button.click()
            
            media_type = "video" if is_video else "image"
            logger.info(f"{media_type.capitalize()} sent successfully")
            
        except Exception as e:
            logger.error(f"Failed to send media: {e}")
            raise
    
    def human_like_delay(self):
        """Add random human-like delays between actions"""
        # Random delay between 2-5 seconds
        delay = random.uniform(2, 5)
        time.sleep(delay)
    
    def send_bulk_messages(self, excel_path: str, message: str, 
                          image_path: Optional[str] = None, 
                          video_path: Optional[str] = None):
        """
        Send bulk messages to all contacts in Excel file
        
        Args:
            excel_path (str): Path to Excel file with contacts
            message (str): Text message to send
            image_path (Optional[str]): Path to image file
            video_path (Optional[str]): Path to video file
        """
        try:
            # Extract contacts from Excel
            contacts = self.extract_contacts_from_excel(excel_path)
            
            if not contacts:
                logger.error("No contacts found in Excel file")
                return
            
            logger.info(f"Starting bulk message sending to {len(contacts)} contacts")
            
            success_count = 0
            failed_count = 0
            
            for i, phone_number in enumerate(contacts, 1):
                try:
                    logger.info(f"Processing contact {i}/{len(contacts)}: {phone_number}")
                    
                    # Search and select contact
                    if not self.search_contact(phone_number):
                        logger.warning(f"Failed to find contact: {phone_number}")
                        failed_count += 1
                        continue
                    
                    # Human-like delay before sending
                    self.human_like_delay()
                    
                    # Send text message if provided
                    if message.strip():
                        self.send_text_message(message)
                        self.human_like_delay()
                    
                    # Send image if provided
                    if image_path and os.path.exists(image_path):
                        self.send_media_message(image_path, is_video=False)
                        self.human_like_delay()
                    
                    # Send video if provided
                    if video_path and os.path.exists(video_path):
                        self.send_media_message(video_path, is_video=True)
                        self.human_like_delay()
                    
                    success_count += 1
                    logger.info(f"Successfully sent message to {phone_number}")
                    
                    # Additional random delay between contacts
                    time.sleep(random.uniform(3, 8))
                    
                except Exception as e:
                    logger.error(f"Failed to send message to {phone_number}: {e}")
                    failed_count += 1
                    continue
            
            logger.info(f"Bulk messaging completed!")
            logger.info(f"Successfully sent: {success_count}")
            logger.info(f"Failed: {failed_count}")
            
        except Exception as e:
            logger.error(f"Bulk messaging failed: {e}")
            raise
    
    def close(self):
        """Close the browser and cleanup"""
        if self.driver:
            self.driver.quit()
            logger.info("Browser closed")

def main():
    """Main function to run the WhatsApp bulk sender"""
    import argparse
    
    parser = argparse.ArgumentParser(description="WhatsApp Bulk Message Sender")
    parser.add_argument("excel_path", help="Path to Excel file with contacts")
    parser.add_argument("message", help="Text message to send")
    parser.add_argument("--image", help="Path to image file (optional)")
    parser.add_argument("--video", help="Path to video file (optional)")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode")
    
    args = parser.parse_args()
    
    # Validate file paths
    if not os.path.exists(args.excel_path):
        logger.error(f"Excel file not found: {args.excel_path}")
        sys.exit(1)
    
    if args.image and not os.path.exists(args.image):
        logger.error(f"Image file not found: {args.image}")
        sys.exit(1)
    
    if args.video and not os.path.exists(args.video):
        logger.error(f"Video file not found: {args.video}")
        sys.exit(1)
    
    # Create and run WhatsApp sender
    sender = WhatsAppBulkSender(headless=args.headless)
    
    try:
        sender.setup_driver()
        sender.open_whatsapp_web()
        sender.send_bulk_messages(
            excel_path=args.excel_path,
            message=args.message,
            image_path=args.image,
            video_path=args.video
        )
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        sender.close()

if __name__ == "__main__":
    main()