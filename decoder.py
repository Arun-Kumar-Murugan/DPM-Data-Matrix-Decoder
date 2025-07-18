import glob
import os
import logging
from logging import getLogger, DEBUG, StreamHandler
import sys
import cv2
import numpy as np
from pylibdmtx import pylibdmtx

class DataMatrixDecoder:
    def __init__(self, machine_type: str, enable_cv_show: bool = False, morphology_kernel_size: tuple = (3, 3),
                 gaussian_blur_kernel_size: tuple = (7, 7), gaussian_blur_sigma: int = 5,
                 threshold_value: int = 0, threshold_max_value: int = 255,
                 cv_show_wait_time: int = 5000):

        self.compatible_image_formats = ['.png', '.jpg', '.jpeg']
        self.logger = self._setup_logger()
        self.enable_cv_show = enable_cv_show
        self.morphology_kernel_size = morphology_kernel_size
        self.crop_size = {
                        "machine_1": {
                                        "top": 200,
                                        "bottom": 800,
                                        "left": 300,
                                        "right": 1000
                                    },
                        "machine_2": {
                                        "top": 200,
                                        "bottom": 800,
                                        "left": 300,
                                        "right": 1000
                                    },
                        "machine_3": {
                                        "top": 200,
                                        "bottom": 1500,
                                        "left": 100,
                                        "right": 800
                                    }
                        }
        self.machine_type = machine_type.lower()

        self.gaussian_blur_kernel_size = gaussian_blur_kernel_size
        self.gaussian_blur_sigma = gaussian_blur_sigma

        self.threshold_value = threshold_value
        self.threshold_max_value = threshold_max_value

        self.cv_show_wait_time = cv_show_wait_time
        if self.machine_type not in self.crop_size:
            raise ValueError(f"Unsupported machine type: {self.machine_type}. Supported types are: {list(self.crop_size.keys())}.")

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
    
    def _morphological_operations(self, image: np.ndarray):
        kernel = np.ones(self.morphology_kernel_size, np.uint8)
        morphology = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
        return morphology

    def _show_images(self, images: dict):
        for name, img in images.items():
            cv2.namedWindow(name, cv2.WINDOW_NORMAL)
            cv2.setWindowProperty(name, cv2.WND_PROP_TOPMOST, 1)
            cv2.imshow(name, img)

        cv2.waitKey(self.cv_show_wait_time)
        cv2.destroyAllWindows()

    def _focus_on_datamatrix(self, image: np.ndarray):
        resized = cv2.resize(image, (1224, 1024))
        crop = self.crop_size[self.machine_type]
        return resized[crop["top"]:crop["bottom"], 
                            crop["left"]:crop["right"]]

    def _preprocess_image(self, image_path: str):
        input_image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

        if input_image is None:
            self.logger.error(f"Image not found in the specified path: {image_path}."
                              " Check the file path and ensure the image exists.")
            exit()

        focus_image = self._focus_on_datamatrix(input_image)
        gauss_blur = cv2.GaussianBlur(focus_image, 
                        self.gaussian_blur_kernel_size, self.gaussian_blur_sigma)

        gray = cv2.cvtColor(gauss_blur, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, self.threshold_value, 
                        self.threshold_max_value, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        morph = self._morphological_operations(thresh)
        
        if self.enable_cv_show:
            image_show = {
                "Original": input_image,
                "Focused": focus_image,
                "Grayscale ": gray,
                "Thresholded": thresh,
                "Morphology": morph
            }
            self._show_images(image_show)
        
        return morph

    def _get_datamatrix_data(self, image_path: str, image_name: str):
        preprocessed_image = self._preprocess_image(image_path)

        if preprocessed_image is None:
            self.logger.error(f"Failed to preprocess image: {image_name}.")
            return
        
        decoded_objects = pylibdmtx.decode(preprocessed_image)
        if not decoded_objects:
            self.logger.warning(f"DataMatrix out of focus or not found in {image_name}.")
            return

        return decoded_objects[0].data.decode("utf-8")
    
    def _fetch_images(self, image_path: str):
        image_files = []
        for ext in self.compatible_image_formats:
            image_files.extend(glob.glob(os.path.join(image_path, ext)))

        if not image_files:
            self.logger.warning(f"No images found in the specified folder path: {image_path}."
                                " Please check the folder path and ensure it contains images in supported formats.")
            return None

        images = {}
        for img_path in image_files:
            img_name = os.path.basename(img_path)
            images[img_name] = img_path

        self.logger.info(f"Found {len(images)} images.")
        return images
