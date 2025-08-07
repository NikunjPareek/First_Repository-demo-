"""
Configuration settings for WhatsApp Bulk Sender
"""

# Timing and Delays (in seconds)
DELAYS = {
    'typing_min': 0.01,      # Minimum delay between characters
    'typing_max': 0.05,      # Maximum delay between characters
    'action_min': 2,          # Minimum delay between actions
    'action_max': 5,          # Maximum delay between actions
    'contact_min': 3,         # Minimum delay between contacts
    'contact_max': 8,         # Maximum delay between contacts
    'search_wait': 2,         # Wait time for search results
    'media_upload': 3,        # Wait time for media upload
}

# WhatsApp Web Selectors
SELECTORS = {
    'chat_list': '[data-testid="chat-list"]',
    'search_box': '[data-testid="chat-list-search"]',
    'contact_phone': '[data-testid="cell-phone-number"]',
    'message_input': '[data-testid="conversation-compose-box-input"]',
    'attach_button': '[data-testid="attach-button"]',
    'attach_image': '[data-testid="attach-image"]',
    'attach_video': '[data-testid="attach-video"]',
    'file_input': 'input[type="file"]',
    'media_caption': '[data-testid="media-caption"]',
    'send_button': '[data-testid="send"]',
}

# Browser Configuration
BROWSER_CONFIG = {
    'window_size': '1920,1080',
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'timeout': 30,
    'headless': False,
}

# Excel Configuration
EXCEL_CONFIG = {
    'phone_columns': [
        'phone',
        'phone_number', 
        'mobile',
        'mobile_number',
        'contact',
        'number'
    ],
    'default_sheet': 0,  # First sheet
}

# Logging Configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(levelname)s - %(message)s',
    'file': 'whatsapp_sender.log',
    'max_file_size': 10 * 1024 * 1024,  # 10MB
    'backup_count': 5,
}

# WhatsApp Web URLs
URLS = {
    'whatsapp_web': 'https://web.whatsapp.com',
}

# Media Configuration
MEDIA_CONFIG = {
    'supported_images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'],
    'supported_videos': ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv'],
    'max_file_size': None,  # No limit
}

# Error Handling
ERROR_CONFIG = {
    'max_retries': 3,
    'retry_delay': 5,
    'continue_on_error': True,
}

# Anti-Detection Settings
ANTI_DETECTION = {
    'randomize_delays': True,
    'human_typing': True,
    'disable_automation_flags': True,
    'custom_user_agent': True,
}