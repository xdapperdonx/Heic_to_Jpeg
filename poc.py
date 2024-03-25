from PIL import Image
import pyheif
import requests
import os

def heic_to_jpeg(heic_file, jpeg_output):
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

        #save image in JPEG format
        image.save(jpeg_output, "JPEG")

    except Exception as e:
        print(f"{e} file: {heic_file}")

if __name__ == "__main__":
    heic_file_path = "./HEIC/IMG_0101.HEIC"

    heic_to_jpeg(heic_file_path, "./JPEG/IMG_0101.jpeg")