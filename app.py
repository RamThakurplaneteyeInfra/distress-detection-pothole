import os
import io
import torch
import requests
import folium
import sqlite3
import numpy as np
from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
from flask_socketio import SocketIO
from PIL import Image
from datetime import datetime
from segment_anything import sam_model_registry, SamPredictor
from fpdf import FPDF
from dotenv import load_dotenv
import psycopg2

# ---------------------------------------------------
# Load environment variables
# ---------------------------------------------------
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
CORS(app)
app.config["SECRET_KEY"] = SECRET_KEY
socketio = SocketIO(app, cors_allowed_origins="*")

# ---------------------------------------------------
# Database Connection
# ---------------------------------------------------
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

# ---------------------------------------------------
# Model Setup
# ---------------------------------------------------
MODEL_NAME = "vit_b"
MODEL_PATH = "sam_vit_b_01ec64.pth"
HF_MODEL_URL = "https://huggingface.co/AkhileshYR/sam-vit-b-model/resolve/main/sam_vit_b_01ec64.pth"

def ensure_model_file():
    """Ensure SAM model file exists, download if missing."""
    if not os.path.exists(MODEL_PATH) or os.path.getsize(MODEL_PATH) < 300_000_000:
        print("[INFO] SAM model not found locally. Downloading from Hugging Face...")
        try:
            r = requests.get(HF_MODEL_URL, stream=True)
            with open(MODEL_PATH, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print("[INFO] SAM model downloaded successfully.")
        except Exception as e:
            print(f"[ERROR] Failed to download SAM model: {e}")

print("[INFO] Checking SAM model file...")
ensure_model_file()

print("[INFO] Loading SAM model...")
sam = sam_model_registry[MODEL_NAME](checkpoint=MODEL_PATH)
predictor = SamPredictor(sam)
print("[INFO] SAM model loaded successfully.")

# ---------------------------------------------------
# Routes
# ---------------------------------------------------
@app.route("/")
def index():
    return render_template("index1.html")

@app.route("/health")
def health_check():
    return jsonify({"status": "ok", "message": "Backend running"}), 200

@app.route("/upload", methods=["POST"])
def upload_image():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file provided"}), 400

    img_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(img_path)

    image = Image.open(img_path).convert("RGB")
    image_np = np.array(image)

    predictor.set_image(image_np)
    input_points = np.array([[200, 200]])  # placeholder point
    input_labels = np.array([1])

    masks, scores, logits = predictor.predict(
        point_coords=input_points,
        point_labels=input_labels,
        multimask_output=True
    )

    area = np.sum(masks[0])  # simple area estimation

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO detections (filename, area, created_at) VALUES (%s, %s, %s)",
        (file.filename, float(area), datetime.utcnow())
    )
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        "filename": file.filename,
        "area": float(area),
        "message": "Detection complete"
    })

@app.route("/download_pdf/<filename>")
def download_pdf(filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Detection Report for {filename}", ln=True, align="C")
    pdf.output(f"{UPLOAD_FOLDER}/{filename}.pdf")

    return send_file(f"{UPLOAD_FOLDER}/{filename}.pdf", as_attachment=True)

# ---------------------------------------------------
# Run the App
# ---------------------------------------------------
if __name__ == "__main__":
    print("[INFO] Starting server...")
    socketio.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))

