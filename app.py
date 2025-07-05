from flask import Flask, request, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # <-- Enable frontend access

@app.route('/generate', methods=['POST'])
def generate():
    # run Blender script here to create an FBX file, e.g. "out.fbx"
    return send_file('out.fbx', as_attachment=True, download_name='3dtext.fbx')
