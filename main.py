import os
import requests
import textwrap
import time
from PIL import Image, ImageDraw, ImageFont

# 1. Setup Environment Variables
# These are pulled from GitHub Secrets (online) or your .env file (local)
ACCESS_TOKEN = os.getenv("FB_ACCESS_TOKEN")
IG_USER_ID = os.getenv("IG_USER_ID")

def get_bible_verse():
    """Fetches a random verse from the Bible API."""
    try:
        response = requests.get("https://bible-api.com/?random=verse", timeout=10)
        data = response.json()
        text = data['text'].strip().replace("\n", " ")
        ref = data['reference']
        return text, ref
    except Exception as e:
        print(f"Error fetching verse: {e}")
        # Reliable fallback verse
        return "Be joyful in hope, patient in affliction, faithful in prayer.", "Romans 12:12"

def create_image(verse_text, reference):
    """Creates a 1080x1080 square image and saves it as post.jpg."""
    # Create a dark gray background
    img = Image.new('RGB', (1080, 1080), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)
    
    # Font Setup with Fallbacks
    try:
        # Try to load default font with specific size (Pillow 10.1.0+)
        font_main = ImageFont.load_default(size=50)
        font_ref = ImageFont.load_default(size=35)
    except:
        # Older Pillow version fallback
        font_main = ImageFont.load_default()
        font_ref = ImageFont.load_default()

    # Wrap the verse text to fit the image
    lines = textwrap.wrap(verse_text, width=35)
    
    # Calculate vertical starting position
    y_text
