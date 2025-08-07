import streamlit as st
import pandas as pd
import time
import random
import os
from pathlib import Path
import tempfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import base64

# Page configuration
st.set_page_config(
    page_title="WhatsApp Bulk Messenger",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        color: #25D366;
        font-size: 2.5rem;
        font-weight: bold;
    }
    .section-header {
        color: #075E54;
        border-bottom: 2px solid #25D366;
        padding-bottom: 0.5rem;
        margin: 1rem 0;
    }
    .success-message {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 0.25rem;
        margin: 1rem 0;
    }
    .error-message {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.25rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #e7f3ff;
        border: 1px solid #b8daff;
        color: #004085;
        padding: 1rem;
        border-radius: 0.25rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class WhatsAppAutomation:
    def __init__(self):
        self.driver = None
        self.wait = None
    
    def setup_driver(self):
        """Set up Chrome driver with appropriate options"""
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Keep browser open for user interaction
        chrome_options.add_experimental_option("detach", True)
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.wait = WebDriverWait(self.driver, 30)
        
    def open_whatsapp_web(self):
        """Open WhatsApp Web and wait for QR code scan"""
        try:
            self.driver.get("https://web.whatsapp.com")
            st.info("🔄 WhatsApp Web opened. Please scan the QR code to login.")
            
            # Wait for the main chat interface to load (indicates successful login)
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='chat-list']")))
            st.success("✅ Successfully logged into WhatsApp Web!")
            return True
            
        except TimeoutException:
            st.error("❌ Timeout waiting for WhatsApp Web to load. Please try again.")
            return False
        except Exception as e:
            st.error(f"❌ Error opening WhatsApp Web: {str(e)}")
            return False
    
    def send_message_to_number(self, phone_number, message, media_path=None):
        """Send message to a specific phone number"""
        try:
            # Clean phone number (remove spaces, dashes, etc.)
            clean_number = ''.join(filter(str.isdigit, phone_number))
            
            # Create WhatsApp URL for the number
            url = f"https://web.whatsapp.com/send?phone={clean_number}"
            self.driver.get(url)
            
            # Wait for chat to load
            time.sleep(3)
            
            # Check if number is invalid
            try:
                invalid_element = self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Phone number shared via url is invalid')]")))
                if invalid_element:
                    return False, f"Invalid phone number: {phone_number}"
            except TimeoutException:
                pass  # Number is valid, continue
            
            # Wait for message input box
            message_box = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='conversation-compose-box-input']")))
            
            # Send media file if provided
            if media_path and os.path.exists(media_path):
                try:
                    # Click attachment button
                    attach_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='clip']")))
                    attach_btn.click()
                    
                    # Click on document/media option
                    media_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='attach-document']")))
                    media_btn.click()
                    
                    # Upload file
                    file_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='file']")
                    file_input.send_keys(media_path)
                    
                    # Wait for file to upload and send button to appear
                    time.sleep(2)
                    send_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='send']")))
                    send_btn.click()
                    
                    # Wait for media to send
                    time.sleep(3)
                    
                except Exception as e:
                    st.warning(f"⚠️ Could not send media to {phone_number}: {str(e)}")
            
            # Send text message if provided
            if message.strip():
                # Clear and type message
                message_box.clear()
                message_box.send_keys(message)
                
                # Send message
                message_box.send_keys(Keys.ENTER)
                
                # Wait for message to be sent
                time.sleep(2)
            
            return True, "Message sent successfully"
            
        except TimeoutException:
            return False, f"Timeout sending message to {phone_number}"
        except Exception as e:
            return False, f"Error sending message to {phone_number}: {str(e)}"
    
    def close_driver(self):
        """Close the browser driver"""
        if self.driver:
            self.driver.quit()

def process_excel_file(uploaded_file):
    """Process uploaded Excel file and extract phone numbers"""
    try:
        # Read Excel file
        df = pd.read_excel(uploaded_file)
        
        # Display columns to user for selection
        st.subheader("📊 Excel File Preview")
        st.dataframe(df.head())
        
        # Let user select the column containing phone numbers
        phone_column = st.selectbox(
            "Select the column containing phone numbers:",
            options=df.columns.tolist(),
            help="Choose the column that contains WhatsApp phone numbers"
        )
        
        if phone_column:
            # Extract phone numbers from selected column
            phone_numbers = df[phone_column].dropna().astype(str).tolist()
            
            # Clean phone numbers (remove NaN, empty strings, etc.)
            phone_numbers = [num.strip() for num in phone_numbers if num.strip() and num.strip().lower() != 'nan']
            
            st.success(f"✅ Found {len(phone_numbers)} phone numbers in the file")
            
            # Show preview of phone numbers
            with st.expander("📱 Preview Phone Numbers"):
                for i, num in enumerate(phone_numbers[:10], 1):
                    st.text(f"{i}. {num}")
                if len(phone_numbers) > 10:
                    st.text(f"... and {len(phone_numbers) - 10} more numbers")
            
            return phone_numbers
        else:
            return []
            
    except Exception as e:
        st.error(f"❌ Error processing Excel file: {str(e)}")
        return []

def save_uploaded_file(uploaded_file):
    """Save uploaded file to temporary directory"""
    try:
        temp_dir = tempfile.mkdtemp()
        file_path = os.path.join(temp_dir, uploaded_file.name)
        
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        return file_path
    except Exception as e:
        st.error(f"❌ Error saving file: {str(e)}")
        return None

def main():
    # Header
    st.markdown('<h1 class="main-header">📱 WhatsApp Bulk Messenger</h1>', unsafe_allow_html=True)
    st.markdown("Send messages to multiple WhatsApp contacts with ease!")
    
    # Sidebar with instructions
    with st.sidebar:
        st.markdown("### 📋 Instructions")
        st.markdown("""
        1. **Upload Excel File**: Upload an Excel file containing phone numbers
        2. **Select Column**: Choose the column with phone numbers
        3. **Write Message**: Enter your message text
        4. **Upload Media** (Optional): Attach image/video
        5. **Click Done**: Start the automation
        6. **Scan QR Code**: Login to WhatsApp Web when prompted
        """)
        
        st.markdown("### ⚠️ Important Notes")
        st.markdown("""
        - Phone numbers should include country code (e.g., +1234567890)
        - Make sure you're logged into WhatsApp on your phone
        - Keep the browser window open during the process
        - The process includes random delays (1-5 seconds) between messages
        """)
    
    # Initialize session state
    if 'phone_numbers' not in st.session_state:
        st.session_state.phone_numbers = []
    if 'automation_started' not in st.session_state:
        st.session_state.automation_started = False
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<h2 class="section-header">📁 File Upload</h2>', unsafe_allow_html=True)
        
        # Excel file upload
        excel_file = st.file_uploader(
            "Upload Excel file with phone numbers",
            type=['xlsx', 'xls'],
            help="Upload an Excel file containing WhatsApp phone numbers"
        )
        
        if excel_file:
            phone_numbers = process_excel_file(excel_file)
            st.session_state.phone_numbers = phone_numbers
    
    with col2:
        st.markdown('<h2 class="section-header">📝 Message Content</h2>', unsafe_allow_html=True)
        
        # Message input
        message_text = st.text_area(
            "Enter your message:",
            height=150,
            placeholder="Type your message here...",
            help="Enter the text message you want to send to all contacts"
        )
        
        # Media file upload
        media_file = st.file_uploader(
            "Upload image/video (optional)",
            type=['jpg', 'jpeg', 'png', 'gif', 'mp4', 'avi', 'mov', 'pdf', 'doc', 'docx'],
            help="Upload an image, video, or document to send along with the message"
        )
    
    # Action section
    st.markdown('<h2 class="section-header">🚀 Start Automation</h2>', unsafe_allow_html=True)
    
    # Display summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📱 Phone Numbers", len(st.session_state.phone_numbers))
    with col2:
        st.metric("📝 Message Length", len(message_text))
    with col3:
        st.metric("📎 Media File", "Yes" if media_file else "No")
    
    # Validation and start button
    can_start = len(st.session_state.phone_numbers) > 0 and message_text.strip()
    
    if not can_start:
        if len(st.session_state.phone_numbers) == 0:
            st.warning("⚠️ Please upload an Excel file and select the phone number column")
        if not message_text.strip():
            st.warning("⚠️ Please enter a message to send")
    
    # Start automation button
    if st.button("🎯 Done - Start Automation", type="primary", disabled=not can_start):
        st.session_state.automation_started = True
    
    # Run automation
    if st.session_state.automation_started and can_start:
        st.markdown('<div class="info-box">🚀 <strong>Automation Started!</strong> Please follow the instructions below.</div>', unsafe_allow_html=True)
        
        # Save media file if uploaded
        media_path = None
        if media_file:
            media_path = save_uploaded_file(media_file)
            if media_path:
                st.success(f"✅ Media file saved: {media_file.name}")
        
        # Initialize automation
        automation = WhatsAppAutomation()
        
        try:
            # Setup driver and open WhatsApp Web
            with st.spinner("🔄 Setting up browser..."):
                automation.setup_driver()
            
            if automation.open_whatsapp_web():
                # Wait for user confirmation that they've logged in
                st.markdown("### 📱 Please scan the QR code in the browser window that opened")
                
                if st.button("✅ I've logged in, start sending messages"):
                    # Progress tracking
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    success_count = 0
                    failed_numbers = []
                    
                    total_numbers = len(st.session_state.phone_numbers)
                    
                    for i, phone_number in enumerate(st.session_state.phone_numbers):
                        status_text.text(f"📤 Sending message to: {phone_number} ({i+1}/{total_numbers})")
                        
                        # Send message
                        success, result_message = automation.send_message_to_number(
                            phone_number, message_text, media_path
                        )
                        
                        if success:
                            success_count += 1
                            st.success(f"✅ Sent to {phone_number}")
                        else:
                            failed_numbers.append(phone_number)
                            st.error(f"❌ Failed to send to {phone_number}: {result_message}")
                        
                        # Update progress
                        progress_bar.progress((i + 1) / total_numbers)
                        
                        # Random delay between messages (1-5 seconds)
                        delay = random.uniform(1, 5)
                        time.sleep(delay)
                    
                    # Final results
                    st.markdown("---")
                    st.markdown("### 📊 Automation Complete!")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("✅ Successful", success_count)
                    with col2:
                        st.metric("❌ Failed", len(failed_numbers))
                    with col3:
                        st.metric("📱 Total", total_numbers)
                    
                    if failed_numbers:
                        st.markdown("### ❌ Failed Numbers:")
                        for num in failed_numbers:
                            st.text(f"• {num}")
                    
                    st.balloons()
        
        except Exception as e:
            st.error(f"❌ Automation error: {str(e)}")
        
        finally:
            # Clean up
            automation.close_driver()
            st.session_state.automation_started = False

if __name__ == "__main__":
    main()