from flask import Flask, render_template, request, send_file
import qrcode
import os
from PIL import Image
import uuid

app = Flask(__name__)
OUTPUT_FOLDER = "generated_qr"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    qr_filename = None

    if request.method == "POST":
        data = request.form["data"]
        fill = request.form["fill_color"]
        bg = request.form["bg_color"]
        border = int(request.form["border"])
        version = int(request.form["version"])

        qr = qrcode.QRCode(
            version=version,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=border
        )

        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color=fill, back_color=bg)

        filename = f"{uuid.uuid4().hex}.png"
        filepath = os.path.join(OUTPUT_FOLDER, filename)
        img.save(filepath)

        qr_filename = filename

    return render_template("index.html", qr_filename=qr_filename)

@app.route("/download/<filename>")
def download(filename):
    return send_file(os.path.join(OUTPUT_FOLDER, filename), as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
