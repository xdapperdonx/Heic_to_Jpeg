import os
import pyheif
from PIL import Image
from io import BytesIO
from flask import Flask, render_template, request, send_file

app = Flask(__name__)

def heic_to_jpeg(heic_file):
    try:
        #reads in heic file
        heif_file = pyheif.read(heic_file)

        #create image object from heic file
        image = Image.frombytes(
            heif_file.mode, 
            heif_file.size, 
            heif_file.data,
            "raw",
            heif_file.mode,
            heif_file.stride,
        )

        return image

    except Exception as e:
        print(f"{e} file: {heic_file}")

@app.route('/', methods=["GET","POST"])
def upload_file():
    if request.method == "POST":
        if 'file' not in request.files:
            return 'No file uploaded', 400
        
        file = request.files['file']
        if file.filename == '':
            return 'No file selected', 400
        
        if file:
            output_file = heic_to_jpeg(file)
           
            img_io = BytesIO()
            output_file.save(img_io, 'JPEG')
            img_io.seek(0)

            filename_without_extension = os.path.splitext(os.path.basename(file.filename))[0]

            return send_file(img_io, mimetype = "image/jpeg", as_attachment = True, download_name = f"{filename_without_extension}.jpeg")
        
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True, port = 5100)