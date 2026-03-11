import os
import requests
from PIL import Image, ImageDraw, ImageFont
import textwrap

# 1. Setup Environment Variables from GitHub Secrets
ACCESS_TOKEN = os.getenv("FB_ACCESS_TOKEN")
IG_USER_ID = os.getenv("IG_USER_ID")

def get_bible_verse():
    """Fetches a random verse."""
    try:
        response = requests.get("https://bible-api.com/?random=verse")
        data = response.json()
        return data['text'].strip().replace("\n", " "), data['reference']
    except Exception as e:
        print(f"Error fetching verse: {e}")
        return "Be joyful in hope, patient in affliction, faithful in prayer.", "Romans 12:12"

def create_image(verse_text, reference):
    """Creates a 1080x1080 square image."""
    img = Image.new('RGB', (1080, 1080), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)
    
    # Use default font if custom isn't found
    try:
        font_main = ImageFont.load_default(size=50)
        font_ref = ImageFont.load_default(size=35)
    except:
        font_main = ImageFont.load_default()
        font_ref = ImageFont.load_default()

    # Wrap text
    lines = textwrap.wrap(verse_text, width=35)
    
    # Draw logic
    y_text = 400
    for line in lines:
        draw.text((540, y_text), line, fill="white", font=font_main, anchor="mm")
        y_text += 70
    
    draw.text((540, y_text + 50), f"— {reference}", fill="#aaaaaa", font=font_ref, anchor="mm")
    img.save("post.jpg")

def post_to_instagram():
    """Directly posts to Instagram Graph API."""
    # The image must be publicly accessible. 
    # By pushing it to GitHub, we can use the 'raw' link.
    repo = os.getenv("GITHUB_REPOSITORY")
    image_url = f"https://raw.githubusercontent.com/{repo}/main/post.jpg"
    
    # Step 1: Create Container
    url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media"
    payload = {'image_url': image_url, 'access_token': ACCESS_TOKEN}
    res = requests.post(url, data=payload).json()
    
    if 'id' in res:
        creation_id = res['id']
        # Step 2: Publish
        publish_url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media_publish"
        requests.post(publish_url, data={'creation_id': creation_id, 'access_token': ACCESS_TOKEN})
        print("Success: Posted to Instagram!")
    else:
        print(f"Error: {res}")

if __name__ == "__main__":
    import sys
    
    # Check if we are in "Create" mode or "Post" mode
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"

    if mode == "create":
        v_text, v_ref = get_bible_verse()
        create_image(v_text, v_ref)
        print("Image created for GitHub to upload.")
        
    elif mode == "post":
        post_to_instagram()
