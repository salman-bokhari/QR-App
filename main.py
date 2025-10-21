import argparse
import os
from io import BytesIO
from flask import Flask, send_file, jsonify, request
import qrcode
from datetime import datetime

app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/generate", methods=["GET"])
def generate():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing 'url' query parameter"}), 400

    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    out_dir = os.environ.get("QR_OUT", "qr_codes")
    os.makedirs(out_dir, exist_ok=True)
    filename = f"qr_{ts}.png"
    path = os.path.join(out_dir, filename)

    # Create QR code
    img = qrcode.make(url)
    img.save(path)

    # Return the generated image
    return send_file(path, mimetype="image/png")

@app.route("/")
def home():
    # Check if a startup QR exists
    startup_qr = os.path.join(os.environ.get("QR_OUT", "qr_codes"), "startup_qr.png")
    if os.path.exists(startup_qr):
        return send_file(startup_qr, mimetype="image/png")
    return "QR Code Generator is running! Use /generate?url=YOUR_URL to create a QR code."

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="QR Code Generator")
    parser.add_argument("--url", default=None, help="URL to generate QR code for at startup")
    parser.add_argument("--port", default=8080, type=int)
    parser.add_argument("--out", default="qr_codes", help="Output folder for QR codes")
    args = parser.parse_args()

    # Ensure output dir exists
    os.makedirs(args.out, exist_ok=True)
    os.environ["QR_OUT"] = args.out

    # Generate one QR on startup if URL given
    if args.url:
        filename = os.path.join(args.out, "startup_qr.png")
        qrcode.make(args.url).save(filename)
        print(f"Startup QR saved at: {filename}")

    print(f"Running QR Code Generator on port {args.port} ...")
    app.run(host="0.0.0.0", port=args.port)
