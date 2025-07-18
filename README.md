# DPM Data Matrix Decoder

A robust Python-based solution for decoding DPM (Direct Part Marking) Data Matrix codes from industrial images. This tool is specifically designed to handle challenging industrial environments with optimized preprocessing techniques for different machine configurations.

## 🔧 Features

- **Multi-Machine Support**: Pre-configured settings for different industrial machines (machine_1, machine_2, machine_3)
- **Advanced Image Preprocessing**: Gaussian blur, morphological operations, and adaptive thresholding
- **ROI-Based Processing**: Machine-specific region of interest cropping for optimal decoding
- **Batch Processing**: Decode multiple images from a directory simultaneously
- **Visual Debugging**: Optional image display for preprocessing step visualization
- **Comprehensive Logging**: Detailed logging with timestamps and processing status
- **Flexible Configuration**: Customizable preprocessing parameters
- **Industrial Grade**: Optimized for low-contrast and challenging lighting conditions

## 📋 Requirements

- Python 3.7+
- OpenCV 4.11.0.86
- NumPy 1.26.1
- pylibdmtx 0.1.10
- python-dotenv (for environment variables)
- tabulate (for result formatting)

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Arun-Kumar-Murugan/DPM-Data-Matrix-Decoder.git
   cd DPM-Data-Matrix-Decoder
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install libdmtx (required for pylibdmtx):**
   
   **On Windows:**
   - Download and install libdmtx from the official source
   - Or use conda: `conda install -c conda-forge libdmtx`
   
   **On Ubuntu/Debian:**
   ```bash
   sudo apt-get install libdmtx0a libdmtx-dev
   ```
   
   **On macOS:**
   ```bash
   brew install libdmtx
   ```

## 📁 Project Structure

```
DPM-Data-Matrix-Decoder/
├── decoder.py              # Main decoder class with preprocessing logic
├── main.py                 # Entry point with environment variable support
├── requirements.txt        # Python dependencies
├── testing.ipynb          # Jupyter notebook for testing and experimentation
├── README.md              # This documentation
├── LICENSE                # License file
└── dpm_images/            # Sample images organized by machine
    ├── machine_1/         # Images from machine 1
    ├── machine_2/         # Images from machine 2
    └── machine_3/         # Images from machine 3
```

## 🎯 Usage

### Method 1: Using Environment Variables (Recommended)

1. **Create a `.env` file** in the project root:
   ```env
   IMAGE_PATH=./dpm_images/machine_1
   MACHINE_NAME=machine_1
   ```

2. **Run the decoder:**
   ```bash
   python main.py
   ```

### Method 2: Direct Import

```python
from decoder import DataMatrixDecoder

# Initialize decoder for specific machine
decoder = DataMatrixDecoder(machine_name="machine_1")

# Decode all images in a directory
decoder.decode_images("./dpm_images/machine_1")
```

### Method 3: Custom Configuration

```python
from decoder import DataMatrixDecoder

# Initialize with custom parameters
decoder = DataMatrixDecoder(
    machine_name="machine_1",
    enable_cv_show=True,                    # Show preprocessing steps
    morphology_kernel_size=(5, 5),         # Morphological operations kernel
    gaussian_blur_kernel_size=(9, 9),      # Gaussian blur kernel
    gaussian_blur_sigma=7,                  # Gaussian blur sigma
    threshold_value=0,                      # Threshold value (0 for OTSU)
    threshold_max_value=255,                # Maximum threshold value
    cv_show_wait_time=1000                  # Display time for each image (ms)
)

decoder.decode_images("path/to/your/images")
```

## 🔧 Configuration

### Machine-Specific Settings

The decoder comes pre-configured with optimal settings for three machine types:

| Machine | ROI Coordinates | Optimized For |
|---------|----------------|---------------|
| machine_1 | top: 200, bottom: 800, left: 300, right: 1000 | Standard industrial setup |
| machine_2 | top: 200, bottom: 800, left: 300, right: 1000 | Standard industrial setup |
| machine_3 | top: 200, bottom: 1500, left: 100, right: 800 | Wide format imaging |

### Preprocessing Pipeline

1. **Image Resizing**: Standardized to 1224x1024 pixels
2. **ROI Extraction**: Machine-specific region cropping
3. **Gaussian Blur**: Noise reduction with configurable kernel
4. **Grayscale Conversion**: Color to grayscale transformation
5. **Adaptive Thresholding**: OTSU method for optimal binarization
6. **Morphological Operations**: Closing operations for structure enhancement

### Supported Image Formats

- PNG (.png)
- JPEG (.jpg, .jpeg)

## 📊 Output Format

The decoder provides comprehensive results in a tabulated format:

```
********************************************* RESULTS *********************************************

┌─────────────────────────────────────────────────┬─────────────────────────────────────────┐
│ Filename                                        │ Decoded Data                            │
├─────────────────────────────────────────────────┼─────────────────────────────────────────┤
│ S00001_F1_C1_N001_P165_B1_20250717103204536.jpg│ [Decoded DataMatrix Content]            │
│ S00003_F1_C3_N001_P165_B1_20250717103204552.jpg│ [Decoded DataMatrix Content]            │
│ S00004_F1_C4_N001_P165_B1_20250717103204536.jpg│ DataMatrix out of focus or not found    │
└─────────────────────────────────────────────────┴─────────────────────────────────────────┘

********************************************* END *********************************************
```

## 🔍 Troubleshooting

### Common Issues

1. **"DataMatrix out of focus or not found"**
   - Check image quality and focus
   - Verify correct machine configuration
   - Adjust ROI coordinates if needed
   - Try different preprocessing parameters

2. **"Image not found in the specified path"**
   - Verify the image path exists
   - Check file permissions
   - Ensure image format is supported

3. **Import errors for pylibdmtx**
   - Install libdmtx system library
   - Verify pylibdmtx installation
   - Check system compatibility

### Performance Tips

- Use appropriate image resolution (recommended: 1224x1024 after resizing)
- Ensure good lighting conditions during image capture
- Clean the DataMatrix surface before imaging
- Use machine-specific configurations for best results

## 🧪 Testing

Use the provided Jupyter notebook for interactive testing:

```bash
jupyter notebook testing.ipynb
```

The notebook provides:
- Step-by-step preprocessing visualization
- Parameter tuning capabilities
- Performance analysis tools

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Arun Kumar Murugan**
- GitHub: [@Arun-Kumar-Murugan](https://github.com/Arun-Kumar-Murugan)

## 🙏 Acknowledgments

- OpenCV community for computer vision tools
- pylibdmtx developers for DataMatrix decoding capabilities
- Industrial automation community for real-world testing scenarios

---

For more detailed documentation and advanced usage examples, please refer to the code comments and the testing notebook.
