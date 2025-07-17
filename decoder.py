import glob
import os
import logging
from logging import getLogger, DEBUG, StreamHandler
import sys
import cv2
import numpy as np
from pylibdmtx import pylibdmtx

class DataMatrixDecoder:
    def __init__(self, image_path: str):
        self.image_path = image_path
        self.compatible_image_formats = ['.png', '.jpg', '.jpeg']
        self.logger = self._setup_logger()
        self.images = self._get_images()
        self.crop_size = (400, 740, 650, 1000)  # (top, bottom, left, right)
        self.enable_cv_show = False
        self.morphology_kernel_size = (3, 3)

    def _get_images(self):
        image_files = []
        for ext in self.compatible_image_formats:
            image_files.extend(glob.glob(os.path.join(self.image_path, ext)))

        if not image_files:
            self.logger.warning(f"No images found in the specified folder path: {self.image_path}.")
            self.logger.warning("Please check the folder path and ensure it contains images in supported formats.")
            return None

        images = {}
        for img_path in image_files:
            img_name = os.path.basename(img_path)
            images[img_name] = img_path

        self.logger.info(f"Found {len(images)} images.")
        return images

    def _setup_logger(self):
        logger = getLogger("DecoderLogger")
        logger.setLevel(DEBUG)
        formatter = logging.Formatter(
                    '%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
        stream_handler = StreamHandler(sys.stdout)
        stream_handler.setLevel(DEBUG)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        logger.debug("Decoder started")
        return logger
    
    def _crop_image(self, image: np.ndarray):
        top, bottom, left, right = self.crop_size
        return image[top:bottom, left:right]
    
    def morphological_operations(self, image: np.ndarray):
        kernel = np.ones(self.morphology_kernel_size, np.uint8)
        morphology = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
        return morphology

    def show_images(images:dict):
        for name, img in images.items():
            cv2.namedWindow(name, cv2.WINDOW_NORMAL)
            cv2.setWindowProperty(name, cv2.WND_PROP_TOPMOST, 1)
            cv2.imshow(name, img)
        cv2.waitKey(5000)
        cv2.destroyAllWindows()

    def _get_datamatrix_data(self, image_path):
        input_image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        if input_image is None:
            self.logger.error("Image not found!")
            exit()

        gray = cv2.cvtColor(self._crop_image(input_image), cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        morph = self.morphological_operations(thresh)
        
        decoded_objects = pylibdmtx.decode(morph)
        if not decoded_objects:
            self.logger.warning(f"No DataMatrix found in {image_path}.")
            return None
        
        return decoded_objects[0].data.decode("utf-8")