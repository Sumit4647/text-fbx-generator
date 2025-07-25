from PIL import Image, ImageDraw, ImageFont
import os

font_dir = "Font"
output_dir = "public/previews"
os.makedirs(output_dir, exist_ok=True)

sample_text = "Text Style"
img_size = (512, 128)
bg_color = "white"
text_color = "black"

for font_file in os.listdir(font_dir):
    if font_file.lower().endswith((".ttf", ".otf")):
        font_path = os.path.join(font_dir, font_file)
        font_name = os.path.splitext(font_file)[0]
        try:
            font = ImageFont.truetype(font_path, 64)
            img = Image.new("RGB", img_size, bg_color)
            draw = ImageDraw.Draw(img)
            bbox = draw.textbbox((0, 0), sample_text, font=font)
            text_size = (bbox[2] - bbox[0], bbox[3] - bbox[1])
            position = ((img_size[0] - text_size[0]) // 2, (img_size[1] - text_size[1]) // 2)
            draw.text(position, sample_text, fill=text_color, font=font)
            img.save(os.path.join(output_dir, f"{font_name}.png"))
        except Exception as e:
            print(f"Error with {font_file}: {e}")
