import glob
import os
import logging
from logging import getLogger, DEBUG, StreamHandler
import sys

class DataMatrixDecoder:
    def __init__(self, image_path: str):
        self.image_path = image_path
        self.compatible_image_formats = ['.png', '.jpg', '.jpeg']
        self.logger = self._setup_logger()
        self.images = self._get_images()

    def _get_images(self):
        image_files = []
        for ext in self.compatible_image_formats:
            image_files.extend(glob.glob(os.path.join(self.image_path, ext)))

        if not image_files:
            self.logger.warning("No images found in the specified folder.")
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