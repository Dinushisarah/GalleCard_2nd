from PIL import Image, ImageDraw, ImageFont
import os

# ===== IMAGE POSITIONING CONFIGURATION =====
# Choose how the beach image should be positioned:
# "cover" - Fill entire area, crop if needed (no gaps, recommended)
# "contain" - Fit entire image, may have gaps (centered by default)
IMAGE_MODE = "cover"  # Change to "contain" if you prefer

# For "contain" mode, choose position:
# "center", "top", "bottom", "left", "right", "top-left", "top-right", "bottom-left", "bottom-right"
IMAGE_POSITION = "center"

# For "cover" mode, choose crop alignment:
# "center" - Crop from center (balanced view)
# "top" - Crop from top (show top of image)
# "bottom" - Crop from bottom (show bottom of image)
CROP_ALIGNMENT = "center"  # Only used in "cover" mode
# ===========================================

# Create a white card with rounded corners
card_width = 800
card_height = 1000
card_bg = Image.new('RGB', (card_width, card_height), color='white')
draw = ImageDraw.Draw(card_bg)

# Beach image area (top section with rounded corners)
beach_area_width = card_width - 80  # 40px margin on each side
beach_area_height = 400
beach_area_x = 40
beach_area_y = 40
corner_radius = 30

# Create a mask for rounded corners
def create_rounded_rectangle_mask(width, height, radius):
    mask = Image.new('L', (width, height), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([(0, 0), (width, height)], radius, fill=255)
    return mask

# Load the actual beach image from assets
beach_image_path = './assets/beach_pic_1.png'

if os.path.exists(beach_image_path):
    beach_img = Image.open(beach_image_path)
    
    if IMAGE_MODE == "cover":
        # COVER mode - Fill the entire area, crop if needed (no gaps)
        beach_img_ratio = beach_img.width / beach_img.height
        area_ratio = beach_area_width / beach_area_height
        
        if beach_img_ratio > area_ratio:
            # Image is wider - fit to height, crop width
            new_height = beach_area_height
            new_width = int(beach_img.width * (beach_area_height / beach_img.height))
            beach_img = beach_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            # Crop based on alignment
            if CROP_ALIGNMENT == "center":
                left = (new_width - beach_area_width) // 2
            elif CROP_ALIGNMENT == "left":
                left = 0
            else:  # right
                left = new_width - beach_area_width
            beach_img = beach_img.crop((left, 0, left + beach_area_width, beach_area_height))
        else:
            # Image is taller - fit to width, crop height
            new_width = beach_area_width
            new_height = int(beach_img.height * (beach_area_width / beach_img.width))
            beach_img = beach_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            # Crop based on alignment
            if CROP_ALIGNMENT == "center":
                top_offset = (new_height - beach_area_height) // 2
            elif CROP_ALIGNMENT == "top":
                top_offset = 0
            else:  # bottom
                top_offset = new_height - beach_area_height
            beach_img = beach_img.crop((0, top_offset, beach_area_width, top_offset + beach_area_height))
        
        # Create final image with exact dimensions
        beach_final = Image.new('RGB', (beach_area_width, beach_area_height))
        beach_final.paste(beach_img, (0, 0))
        beach_img = beach_final
        
    else:  # CONTAIN mode
        # Fit entire image, may have gaps
        beach_img.thumbnail((beach_area_width, beach_area_height), Image.Resampling.LANCZOS)
        beach_final = Image.new('RGB', (beach_area_width, beach_area_height), color=(135, 206, 250))
        
        # Calculate position based on IMAGE_POSITION setting
        if IMAGE_POSITION == "center":
            paste_x = (beach_area_width - beach_img.width) // 2
            paste_y = (beach_area_height - beach_img.height) // 2
        elif IMAGE_POSITION == "top":
            paste_x = (beach_area_width - beach_img.width) // 2
            paste_y = 0
        elif IMAGE_POSITION == "bottom":
            paste_x = (beach_area_width - beach_img.width) // 2
            paste_y = beach_area_height - beach_img.height
        elif IMAGE_POSITION == "left":
            paste_x = 0
            paste_y = (beach_area_height - beach_img.height) // 2
        elif IMAGE_POSITION == "right":
            paste_x = beach_area_width - beach_img.width
            paste_y = (beach_area_height - beach_img.height) // 2
        elif IMAGE_POSITION == "top-left":
            paste_x = 0
            paste_y = 0
        elif IMAGE_POSITION == "top-right":
            paste_x = beach_area_width - beach_img.width
            paste_y = 0
        elif IMAGE_POSITION == "bottom-left":
            paste_x = 0
            paste_y = beach_area_height - beach_img.height
        elif IMAGE_POSITION == "bottom-right":
            paste_x = beach_area_width - beach_img.width
            paste_y = beach_area_height - beach_img.height
        else:  # default to center
            paste_x = (beach_area_width - beach_img.width) // 2
            paste_y = (beach_area_height - beach_img.height) // 2
        
        beach_final.paste(beach_img, (paste_x, paste_y))
        beach_img = beach_final
else:
    # Fallback: create a simple gradient if image not found
    print(f"Warning: {beach_image_path} not found. Using gradient instead.")
    beach_img = Image.new('RGB', (beach_area_width, beach_area_height))
    beach_draw = ImageDraw.Draw(beach_img)
    for y in range(0, beach_area_height):
        blue_intensity = int(135 + (64 - 135) * y / beach_area_height)
        beach_draw.rectangle([(0, y), (beach_area_width, y + 1)], fill=(135, 206, blue_intensity))

# Apply rounded corners to beach image
beach_mask = create_rounded_rectangle_mask(beach_area_width, beach_area_height, corner_radius)
beach_img.putalpha(beach_mask)

# Paste beach image onto card
card_bg.paste(beach_img, (beach_area_x, beach_area_y), beach_img)

# GALLE text (black, centered, large)
try:
    # Try to use a system font, fallback to default if not available
    galle_font_size = 60
    try:
        galle_font = ImageFont.truetype("arial.ttf", galle_font_size)
    except:
        try:
            galle_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", galle_font_size)
        except:
            galle_font = ImageFont.load_default()
except:
    galle_font = ImageFont.load_default()

galle_text = "GALLE"
# Get text bounding box
bbox = draw.textbbox((0, 0), galle_text, font=galle_font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]

# Center the text horizontally
galle_x = (card_width - text_width) // 2
galle_y = beach_area_y + beach_area_height + 40
draw.text((galle_x, galle_y), galle_text, fill='black', font=galle_font)

# Description text (yellow/gold, centered, smaller)
description_text = """The top sightseeing places in Galle are Old Dutch Market, Flag Rock, Dutch Reformed Church, Amangalla, Old Gate, Galle Fort Lighthouse."""

try:
    desc_font_size = 24
    try:
        desc_font = ImageFont.truetype("arial.ttf", desc_font_size)
    except:
        try:
            desc_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", desc_font_size)
        except:
            desc_font = ImageFont.load_default()
except:
    desc_font = ImageFont.load_default()

# Wrap text to fit card width
max_width = card_width - 100
words = description_text.split()
lines = []
current_line = ""

for word in words:
    test_line = current_line + (" " if current_line else "") + word
    bbox = draw.textbbox((0, 0), test_line, font=desc_font)
    test_width = bbox[2] - bbox[0]
    
    if test_width <= max_width:
        current_line = test_line
    else:
        if current_line:
            lines.append(current_line)
        current_line = word

if current_line:
    lines.append(current_line)

# Draw each line centered
desc_y = galle_y + text_height + 30
line_height = text_height + 10
gold_color = (255, 204, 0)  # #FFCC00

for line in lines:
    bbox = draw.textbbox((0, 0), line, font=desc_font)
    line_width = bbox[2] - bbox[0]
    line_x = (card_width - line_width) // 2
    draw.text((line_x, desc_y), line, fill=gold_color, font=desc_font)
    desc_y += line_height

# Save the image
output_path = 'galle_card.png'
card_bg.save(output_path)
print(f"Card image saved to {output_path}")

# Display the image (optional)
card_bg.show()

