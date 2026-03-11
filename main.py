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
    y_text = 450 - (len(lines) * 35) 
    
    # Draw Verse
    for line in lines:
        draw.text((540, y_text), line, fill="white", font=font_main, anchor="mm")
        y_text += 70
    
    # Draw Reference
    draw.text((540, y_text + 60), f"— {reference}", fill="#aaaaaa", font=font_ref, anchor="mm")
    
    # Save the file to the current directory
    img.save("post.jpg")
    print("✅ Image 'post.jpg' created successfully.")

def post_to_instagram():
    """Tells Instagram to fetch the image from your GitHub repository."""
    repo = os.getenv("GITHUB_REPOSITORY")
    if not repo:
        print("❌ Error: GITHUB_REPOSITORY env variable not found.")
        return

    # Use a timestamp (?t=...) so Instagram doesn't show an old cached image
    timestamp = int(time.time())
    image_url = f"https://raw.githubusercontent.com/{repo}/main/post.jpg?t={timestamp}"
    
    print(f"Attempting to post image from: {image_url}")

    # Step 1: Create Media Container
    post_url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media"
    payload = {
        'image_url': image_url,
        'caption': f'Daily Scripture: #Bible #Faith #Christian',
        'access_token': ACCESS_TOKEN
    }
    
    response = requests.post(post_url, data=payload).json()
    
    if 'id' in response:
        creation_id = response['id']
        # Step 2: Publish the Container
        publish_url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media_publish"
        publish_res = requests.post(publish_url, data={
            'creation_id': creation_id,
            'access_token': ACCESS_TOKEN
        }).json()
        
        print(f"🚀 Success! Posted to Instagram. ID: {publish_res.get('id')}")
    else:
        print(f"❌ Instagram API Error: {response}")

if __name__ == "__main__":
    # Check if secrets are present
    if not ACCESS_TOKEN or not IG_USER_ID:
        print("⚠️ Warning: FB_ACCESS_TOKEN or IG_USER_ID is missing.")
    
    # 1. Fetch and Create (Always run this when script is called)
    print("Starting BibleBot Process...")
    v_text, v_ref = get_bible_verse()
    create_image(v_text, v_ref)
