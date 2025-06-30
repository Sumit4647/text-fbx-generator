from flask import Flask, request, send_file
from flask_cors import CORS  # ← Add this

app = Flask(__name__)
CORS(app)  # ← Enable CORS globally
