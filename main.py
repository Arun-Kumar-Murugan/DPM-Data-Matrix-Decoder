from decoder import DataMatrixDecoder

def main():
    decoder = DataMatrixDecoder(machine_name="machine_1")
    decoder.decode_images(image_path="dpm_images/machine_1")

if __name__ == "__main__":
    main()
