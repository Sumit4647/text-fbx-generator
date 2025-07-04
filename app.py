from flask import Flask, request, send_file
import subprocess
import os

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate():
    text = request.form.get('text', '')
    if not text:
        return "No text provided", 400

    # Write text to a temp file or pass as arg
    subprocess.run(['blender', '--background', '--python', 'generate_text.py', '--', text])

    # Return FBX file
    return send_file('output.fbx', as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
