import uuid, os, subprocess
from flask import Flask, request, send_file
from flask_cors import CORS
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return "OK", 200

@app.route("/generate", methods=["POST"])
def generate():
    text = request.form.get("text")
    if not text:
        return "Missing text", 400

    # generate FBX logic


@app.route("/", methods=["GET"])
def home():
    return "OK", 200



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
    text = request.form.get('text', '').strip()
    is_custom = request.form.get('is_custom') == 'true'

    if not text:
        return "Bad request: missing text", 400

    custom_font_filepath = None
    if is_custom:
        custom_file = request.files.get('font_file')
        if not custom_file:
            return "Bad request: missing font_file", 400
        custom_font_filepath = f"{uuid.uuid4()}_{custom_file.filename}"
        custom_file.save(custom_font_filepath)
        font_arg = "CUSTOM"
    else:
        font_key = request.form.get('font', 'BurbankBigCondensed-Black')
        if font_key not in FONT_MAP:
            return "Bad request: invalid font_key", 400
        font_arg = font_key

    filename = f"{uuid.uuid4()}.fbx"
    cmd = [
      "blender","--background","--python","generate_text.py","--",
      text, font_arg, filename
    ]
    if custom_font_filepath:
        cmd.append(custom_font_filepath)

    try:
        subprocess.run(cmd, check=True)
        return send_file(filename, as_attachment=True, download_name="3dtext.fbx")
    finally:
        if custom_font_filepath and os.path.exists(custom_font_filepath):
            os.remove(custom_font_filepath)
        if os.path.exists(filename):
            pass # Usually handled by background tasks in prod, sending file directly works for now

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)
