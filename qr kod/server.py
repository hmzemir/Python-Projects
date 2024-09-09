from flask import Flask, render_template, request, send_file
import qrcode
from io import BytesIO

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Kullanıcıdan gelen linki al
        url = request.form.get('url')

        # QR kodu oluştur
        img = qrcode.make(url)
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        return send_file(buffer, as_attachment=True, download_name='qrcode.png', mimetype='image/png')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)

