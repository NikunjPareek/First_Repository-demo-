#!/usr/bin/env python3
"""
Example usage script for WhatsApp Bulk Sender

This script demonstrates how to use the WhatsAppBulkSender class
to send bulk messages with text, images, and videos.
"""

from whatsapp_bulk_sender import WhatsAppBulkSender
import os

def main():
    # Initialize the WhatsApp bulk sender
    sender = WhatsAppBulkSender(headless=False)  # Set to True for headless mode
    
    # Configuration
    excel_file_path = "/path/to/your/contacts.xlsx"  # Update this path
    
    # Message content
    message = """Hello! 👋

This is a test message from our WhatsApp bulk sender.

Hope you're having a great day!

Best regards,
Your Company"""
    
    # Optional media files (update paths as needed)
    image_path = "/path/to/your/image.jpg"  # Set to None if no image
    video_path = None  # "/path/to/your/video.mp4"  # Set to None if no video
    
    # Example 1: Send messages with text only
    print("=== Example 1: Text-only messages ===")
    try:
        sender.send_bulk_messages(
            excel_path=excel_file_path,
            message=message,
            phone_column=None,  # Auto-detect column
            image_path=None,
            video_path=None,
            start_from=0,  # Start from first contact
            max_messages=5  # Limit to 5 messages for testing
        )
    except Exception as e:
        print(f"Error in Example 1: {e}")
    
    # Example 2: Send messages with image
    print("\n=== Example 2: Messages with image ===")
    if image_path and os.path.exists(image_path):
        try:
            sender_with_image = WhatsAppBulkSender(headless=False)
            sender_with_image.send_bulk_messages(
                excel_path=excel_file_path,
                message=message,
                phone_column="phone",  # Specify column name
                image_path=image_path,
                video_path=None,
                start_from=0,
                max_messages=3
            )
        except Exception as e:
            print(f"Error in Example 2: {e}")
    else:
        print("Image file not found, skipping example 2")
    
    # Example 3: Send messages with video
    print("\n=== Example 3: Messages with video ===")
    if video_path and os.path.exists(video_path):
        try:
            sender_with_video = WhatsAppBulkSender(headless=False)
            sender_with_video.send_bulk_messages(
                excel_path=excel_file_path,
                message=message,
                phone_column="mobile",  # Different column name
                image_path=None,
                video_path=video_path,
                start_from=0,
                max_messages=2
            )
        except Exception as e:
            print(f"Error in Example 3: {e}")
    else:
        print("Video file not found, skipping example 3")

def create_sample_excel():
    """Create a sample Excel file with contacts for testing"""
    import pandas as pd
    
    # Sample contact data
    contacts = {
        'name': ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Wilson'],
        'phone': ['1234567890', '9876543210', '5555555555', '1111111111'],
        'email': ['john@example.com', 'jane@example.com', 'bob@example.com', 'alice@example.com']
    }
    
    df = pd.DataFrame(contacts)
    df.to_excel('sample_contacts.xlsx', index=False)
    print("Sample Excel file 'sample_contacts.xlsx' created successfully!")
    print("Please update the phone numbers with real numbers before using.")

def test_single_message():
    """Test sending a single message"""
    print("=== Testing single message ===")
    
    sender = WhatsAppBulkSender(headless=False)
    sender.setup_driver()
    
    if sender.login_whatsapp():
        # Test with a single number (update with a real number)
        test_phone = "1234567890"  # Update this with a real phone number
        test_message = "Hello! This is a test message from WhatsApp bulk sender."
        
        success = sender.send_message_to_contact(
            phone_number=test_phone,
            message=test_message,
            image_path=None,
            video_path=None
        )
        
        if success:
            print("Test message sent successfully!")
        else:
            print("Failed to send test message")
    
    sender.close()

if __name__ == "__main__":
    print("WhatsApp Bulk Sender - Example Usage")
    print("=" * 40)
    
    choice = input("""
Choose an option:
1. Run full examples (requires Excel file)
2. Create sample Excel file
3. Test single message
4. Exit

Enter your choice (1-4): """)
    
    if choice == "1":
        main()
    elif choice == "2":
        create_sample_excel()
    elif choice == "3":
        test_single_message()
    elif choice == "4":
        print("Goodbye!")
    else:
        print("Invalid choice. Please run the script again.")