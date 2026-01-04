from flask import Flask, request, send_file
from flask_cors import CORS
import subprocess, uuid, os

app = Flask(__name__)
CORS(app)


# Map keys to font files in your Font/ folder
FONT_MAP = {
    "A4SPEED-Bold":           "Font/A4SPEED-Bold.ttf",
    "Arial":                  "Font/Arial.ttf",
    "BebasNeue-Regular":      "Font/BebasNeue-Regular.ttf",
    "Bold Drop":              "Font/Bold Drop.ttf",
    "Bubblegum":              "Font/Bubblegum.ttf",
    "BurbankBigCondensed-Black": "Font/BurbankBigCondensed-Black.otf",
    "Creamy Soup":            "Font/Creamy Soup.otf",
    "Designer":               "Font/Designer.otf",
    "Heavitas":               "Font/Heavitas.ttf",
    "Kind Daily":             "Font/Kind Daily.ttf",
    "LEMONMILK-Bold":         "Font/LEMONMILK-Bold.otf",
    "Minecrafter.Alt":        "Font/Minecrafter.Alt.ttf",
    "OpenSans-Bold":          "Font/OpenSans-Bold.ttf",
    "PackyGreat":             "Font/PackyGreat.ttf",
    "paladins":               "Font/paladins.ttf",
    "Pricedown Bl":           "Font/Pricedown Bl.otf",
    "Roboto-Regular":         "Font/Roboto-Regular.ttf",
    "Square Game":            "Font/Square Game.otf",
    "Super Greatly":          "Font/Super Greatly.ttf",
    "SuperMario256":          "Font/SuperMario256.ttf",
    "Supersonic Rocketship":  "Font/Supersonic Rocketship.ttf",
    "THEBOLDFONT":            "Font/THEBOLDFONT.ttf",
}


@app.route('/generate', methods=['POST'])
def generate():
    text     = request.form.get('text', '').strip()
    font_key = request.form.get('font', 'BurbankBigCondensed-Black')
    if not text or font_key not in FONT_MAP:
        return "Bad request", 400

    filename = f"{uuid.uuid4()}.fbx"
    font_arg = font_key  # pass the key to Blender script
    cmd = [
      "blender","--background","--python","generate_text.py","--",
      text, font_arg, filename
    ]
    subprocess.run(cmd, check=True)
    return send_file(filename, as_attachment=True, download_name="3dtext.fbx")

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)
