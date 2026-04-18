import uuid, os, subprocess
from flask import Flask, request, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
    "Starjedi":               "Font/Starjedi.ttf",
    "Starjhol":               "Font/Starjhol.ttf",
    "Starjout":               "Font/Starjout.ttf",
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
        cmd.extend(["--custom_font_path", custom_font_filepath])
    advanced = request.form.get('advanced_settings')
    if advanced:
        cmd.extend(["--advanced_settings", advanced])

    try:
        subprocess.run(cmd, check=True)
        return send_file(filename, as_attachment=True, download_name="3dtext.fbx")
    finally:
        if custom_font_filepath and os.path.exists(custom_font_filepath):
            os.remove(custom_font_filepath)
        if os.path.exists(filename):
            pass # Usually handled by background tasks in prod, sending file directly works for now


@app.route('/preview', methods=['POST'])
def preview():
    """Returns the actual FBX for 3D display in the browser — same pipeline as /generate,
    but stored in /tmp and no download tracking."""
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

    fbx_path = f"/tmp/{uuid.uuid4()}_preview.fbx"
    cmd = [
        "blender", "--background", "--python", "generate_text.py", "--",
        text, font_arg, fbx_path
    ]
    if custom_font_filepath:
        cmd.extend(["--custom_font_path", custom_font_filepath])
    advanced = request.form.get('advanced_settings')
    if advanced:
        cmd.extend(["--advanced_settings", advanced])

    try:
        subprocess.run(cmd, check=True, timeout=90)
        return send_file(fbx_path, mimetype='application/octet-stream',
                         as_attachment=False, download_name='preview.fbx')
    except subprocess.TimeoutExpired:
        return "Preview timed out", 504
    finally:
        if custom_font_filepath and os.path.exists(custom_font_filepath):
            os.remove(custom_font_filepath)
        if os.path.exists(fbx_path):
            os.remove(fbx_path)

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)