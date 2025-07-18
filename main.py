import os
from decoder import DataMatrixDecoder

def main():
    image_path = os.path.join("dpm_images", "machine_1")
    print(f"Decoding images from: {image_path}")
    decoder = DataMatrixDecoder(machine_type="machine_1")
    decoder.decode_images(image_path)

if __name__ == "__main__":
    main()
