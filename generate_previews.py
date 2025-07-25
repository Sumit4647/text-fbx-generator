from PIL import Image, ImageDraw, ImageFont
import os

FONT_DIR = "Font"
OUTPUT_DIR = "font_previews"
SAMPLE_TEXT = "Text Style"

os.makedirs(OUTPUT_DIR, exist_ok=True)

for font_file in os.listdir(FONT_DIR):
    try:
        if font_file.endswith((".ttf", ".otf")):
            font_path = os.path.join(FONT_DIR, font_file)
            font = ImageFont.truetype(font_path, 100)
            # Temp canvas to measure text
            temp_img = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
            draw = ImageDraw.Draw(temp_img)
            bbox = draw.textbbox((0, 0), SAMPLE_TEXT, font=font)
            width = bbox[2] - bbox[0]
            height = bbox[3] - bbox[1]

            img = Image.new("RGBA", (width + 20, height + 40), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            draw.text((10, 10), SAMPLE_TEXT, font=font, fill=(255, 255, 255, 255))

            output_path = os.path.join(OUTPUT_DIR, f"{os.path.splitext(font_file)[0]}.png")
            img.save(output_path, "PNG")
            print(f"Saved: {output_path}")
    except Exception as e:
        print(f"Error with {font_file}: {e}")
