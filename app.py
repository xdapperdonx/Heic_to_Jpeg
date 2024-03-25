import os
import pyheif
import zipfile
from PIL import Image
from io import BytesIO
from flask import Flask, render_template, request, send_file, jsonify

app = Flask(__name__)

def heic_to_jpeg(upload_files):
    converted_files_list = []
    for file in upload_files:
        try:
            new_filename = os.path.splitext(os.path.basename(file.filename))[0] + ".jpeg"

            try:
                #reads in heic file
                heif_file = pyheif.read(file)
            except ValueError:
                print(file.filename)


            #create image object from heic file
            image = Image.frombytes(
                heif_file.mode, 
                heif_file.size, 
                heif_file.data,
                "raw",
                heif_file.mode,
                heif_file.stride,
            )

            img_io = BytesIO()
            img_io.name = new_filename
            image.save(img_io, 'JPEG')
            img_io.seek(0)            

            converted_files_list.append(img_io)
    
        except Exception as e:
            print(f"{e} file: {heic_file}")

    return converted_files_list

@app.route('/', methods=["GET","POST"])
def upload():
    upload_files = request.files.getlist('files')

    if request.method == "POST":
        if len(upload_files) <= 0 or upload_files[0].filename == "":
            return 'No files uploaded', 400
        else:
            files_list = heic_to_jpeg(upload_files)
            zip_buffer = BytesIO()

            temp_dir = 'temp'
            os.makedirs(temp_dir, exist_ok=True)

            zip_file_path = os.path.join(temp_dir, "files.zip")
            with zipfile.ZipFile(zip_file_path, 'w') as zipf:
                for index, image in enumerate(files_list, start=0):
                    image_name = f'image{index}.jpg'
                    zipf.writestr(image_name, image.getvalue())

            zip_buffer.seek(0)

            return send_file(zip_file_path, as_attachment = True, download_name = "images.zip")
       
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host = "0.0.0.0", debug = True, port = 5100)