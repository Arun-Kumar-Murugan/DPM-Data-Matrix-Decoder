import os
from decoder import DataMatrixDecoder

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(base_dir, "dpm_images", "machine_1")
    print(f"Decoding images from: {image_path}")
    decoder = DataMatrixDecoder(machine_type="machine_1", enable_cv_show=True)
    decoder.decode_images(image_path)

if __name__ == "__main__":
    main()
