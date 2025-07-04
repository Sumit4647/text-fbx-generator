from flask import Flask, request, send_file
import subprocess
import uuid

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate():
    text = request.form.get('text', '')
    if not text:
        return "No text provided", 400

    filename = f"{uuid.uuid4()}.fbx"
    subprocess.run([
        "blender", "-b", "-P", "generate_text.py", "--", text, filename
    ], check=True)

    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
