from decoder import DataMatrixDecoder
from dotenv import load_dotenv
import os

def main():
    load_dotenv()
    image_path = os.getenv("IMAGE_PATH")
    machine_name = os.getenv("MACHINE_NAME")

    decoder = DataMatrixDecoder(machine_name)
    decoder.decode_images(image_path)

if __name__ == "__main__":
    main()
