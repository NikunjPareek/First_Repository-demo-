#!/usr/bin/env python3
"""
Example usage of WhatsApp Bulk Sender
Demonstrates different ways to use the automation script
"""

import os
import sys
from whatsapp_bulk_sender import WhatsAppBulkSender

def example_basic_usage():
    """Example of basic text-only messaging"""
    print("=== Example 1: Basic Text Messaging ===")
    
    # Create sender instance
    sender = WhatsAppBulkSender(headless=False)
    
    try:
        # Setup and login
        sender.setup_driver()
        sender.open_whatsapp_web()
        
        # Send messages
        sender.send_bulk_messages(
            excel_path="sample_contacts.xlsx",
            message="Hello! This is a test message from the WhatsApp Bulk Sender."
        )
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sender.close()

def example_with_media():
    """Example with image and video"""
    print("=== Example 2: Messaging with Media ===")
    
    # Check if media files exist
    image_path = "sample_image.jpg"
    video_path = "sample_video.mp4"
    
    # Only use files that exist
    image_to_use = image_path if os.path.exists(image_path) else None
    video_to_use = video_path if os.path.exists(video_path) else None
    
    sender = WhatsAppBulkSender(headless=False)
    
    try:
        sender.setup_driver()
        sender.open_whatsapp_web()
        
        sender.send_bulk_messages(
            excel_path="sample_contacts.xlsx",
            message="Check out this amazing content!",
            image_path=image_to_use,
            video_path=video_to_use
        )
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sender.close()

def example_headless_mode():
    """Example using headless mode for faster execution"""
    print("=== Example 3: Headless Mode ===")
    
    sender = WhatsAppBulkSender(headless=True)
    
    try:
        sender.setup_driver()
        sender.open_whatsapp_web()
        
        sender.send_bulk_messages(
            excel_path="sample_contacts.xlsx",
            message="Automated message sent in headless mode."
        )
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sender.close()

def example_custom_message():
    """Example with multi-line custom message"""
    print("=== Example 4: Multi-line Message ===")
    
    custom_message = """
Hello there! 👋

This is a multi-line message sent via WhatsApp Bulk Sender.

Features:
✅ Text messaging
✅ Image support  
✅ Video support
✅ Human-like behavior
✅ No restrictions

Best regards,
Your Automation Team
    """.strip()
    
    sender = WhatsAppBulkSender(headless=False)
    
    try:
        sender.setup_driver()
        sender.open_whatsapp_web()
        
        sender.send_bulk_messages(
            excel_path="sample_contacts.xlsx",
            message=custom_message
        )
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sender.close()

def create_sample_files():
    """Create sample files for testing"""
    print("Creating sample files...")
    
    # Create sample Excel file if it doesn't exist
    if not os.path.exists("sample_contacts.xlsx"):
        import pandas as pd
        
        sample_data = {
            'phone_number': ['+1234567890', '+1987654321', '+1122334455'],
            'name': ['John Doe', 'Jane Smith', 'Bob Johnson']
        }
        
        df = pd.DataFrame(sample_data)
        df.to_excel("sample_contacts.xlsx", index=False)
        print("✅ Created sample_contacts.xlsx")
    
    # Create sample image file (1x1 pixel PNG)
    if not os.path.exists("sample_image.jpg"):
        from PIL import Image
        
        # Create a simple 100x100 red image
        img = Image.new('RGB', (100, 100), color='red')
        img.save("sample_image.jpg")
        print("✅ Created sample_image.jpg")
    
    # Create sample video file (empty file for testing)
    if not os.path.exists("sample_video.mp4"):
        with open("sample_video.mp4", "w") as f:
            f.write("This is a placeholder video file")
        print("✅ Created sample_video.mp4 (placeholder)")

def main():
    """Run examples based on command line arguments"""
    
    if len(sys.argv) < 2:
        print("WhatsApp Bulk Sender - Example Usage")
        print("=" * 40)
        print("Usage: python example_usage.py <example_number>")
        print("\nAvailable examples:")
        print("1 - Basic text messaging")
        print("2 - Messaging with media")
        print("3 - Headless mode")
        print("4 - Multi-line custom message")
        print("setup - Create sample files")
        print("\nExample: python example_usage.py 1")
        return
    
    example = sys.argv[1]
    
    # Create sample files if requested
    if example == "setup":
        create_sample_files()
        return
    
    # Create sample files for testing
    create_sample_files()
    
    # Run selected example
    examples = {
        "1": example_basic_usage,
        "2": example_with_media,
        "3": example_headless_mode,
        "4": example_custom_message
    }
    
    if example in examples:
        try:
            examples[example]()
        except KeyboardInterrupt:
            print("\n⚠️  Process interrupted by user")
        except Exception as e:
            print(f"\n❌ Error running example {example}: {e}")
    else:
        print(f"❌ Unknown example: {example}")
        print("Available examples: 1, 2, 3, 4, setup")

if __name__ == "__main__":
    main()