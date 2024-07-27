from flask import Flask, render_template, request, send_file, url_for
import qrcode
import io
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Create an 'uploads' directory within the project directory
uploads_dir = os.path.join(os.getcwd(), 'uploads')
if not os.path.exists(uploads_dir):
    os.makedirs(uploads_dir)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.form.get('data')
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')

    # Save the image to a file in the uploads directory
    filename = secure_filename(f"qr_{data}.png")
    filepath = os.path.join(uploads_dir, filename)
    img.save(filepath)

    # Return the path for the image file for download
    return render_template('index.html', filepath=url_for('download_file', filename=filename))

@app.route('/download/<filename>')
def download_file(filename):
    # Return the file for download
    return send_file(os.path.join(uploads_dir, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
