from flask import Flask, request, send_file
from flask_cors import CORS
import subprocess
import uuid
import os

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

@app.route('/generate', methods=['POST'])
def generate():
    text = request.form.get('text')
    if not text:
        return "Missing text", 400

    # Generate unique filename
    output_file = f"{uuid.uuid4()}.fbx"
    blender_cmd = [
        "blender", "--background", "--python", "generate_text.py", "--", text, output_file
    ]

    try:
        subprocess.run(blender_cmd, check=True)
    except subprocess.CalledProcessError as e:
        return f"Blender failed: {e}", 500

    if not os.path.exists(output_file):
        return "FBX not created", 500

    return send_file(output_file, as_attachment=True, download_name="3dtext.fbx")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
