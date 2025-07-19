# DPM Data Matrix Decoder

A robust Python-based solution for decoding DPM (Direct Part Marking) Data Matrix codes from industrial images. This tool is specifically designed to handle challenging industrial environments with optimized preprocessing techniques for different machine configurations.

## 🔧 Features

- **Multi-Machine Support**: Pre-configured settings for different industrial machines (machine_1, machine_2, machine_3)
- **Advanced Image Preprocessing**: Gaussian blur, morphological operations, and adaptive thresholding
- **ROI-Based Processing**: Machine-specific region of interest cropping for optimal decoding
- **Batch Processing**: Decode multiple images from a directory simultaneously
- **Visual Debugging**: Optional image display for preprocessing step visualization
- **Comprehensive Logging**: Detailed logging with timestamps and processing status
- **CSV Export Functionality**: Automatic export of results to timestamped CSV files
- **Timestamp Tracking**: IST (Indian Standard Time) timestamps for each processed image
- **Report Generation**: Organized reports with serial numbers, timestamps, and results
- **Flexible Configuration**: Customizable preprocessing parameters
- **Industrial Grade**: Optimized for low-contrast and challenging lighting conditions

## 📋 Requirements

- Python 3.7+
- OpenCV 4.11.0.86
- NumPy 1.26.1
- pylibdmtx 0.1.10
- python-dotenv 1.0.1 (for environment variables)
- tabulate (for result formatting)

**Note**: The `csv` and `datetime` modules are part of Python's standard library.

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
├── reports/               # Auto-generated CSV reports (created at runtime)
│   └── YYYY-MM-DD HH-MM-SS AM/PM.csv  # Timestamped report files
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

## 📈 CSV Export & Reporting

### Automatic Report Generation
The decoder automatically generates detailed CSV reports for every batch processing session:

**Features:**
- **Timestamped Files**: Each report is saved with a unique timestamp (format: `YYYY-MM-DD HH-MM-SS AM/PM.csv`)
- **IST Timestamps**: Individual processing timestamps in Indian Standard Time format
- **Serial Numbering**: Sequential numbering for processed images
- **Status Tracking**: Clear indication of successful decodes vs. failed attempts

**Report Location:**
```
reports/
├── 2025-07-19 02-45-30 PM.csv
├── 2025-07-19 03-15-20 PM.csv
└── 2025-07-19 04-30-15 PM.csv
```

**Data Structure:**
| Column | Description | Example |
|--------|-------------|---------|
| S.No | Serial number of processed image | 1, 2, 3... |
| TimeStampIST | Processing timestamp in IST | 2025-07-19 02:45:30 PM |
| ImageFile | Original image filename | S00001_F1_C1_N001_P165_B1_20250717103204536.jpg |
| DecodedData | Decoded DataMatrix content or error message | Decoded content or "DataMatrix out of focus or not found" |

### Benefits of CSV Export
- **Audit Trail**: Complete processing history with timestamps
- **Data Analysis**: Easy import into Excel, databases, or analysis tools
- **Quality Monitoring**: Track success rates and identify problematic images
- **Compliance**: Structured data for regulatory or quality control requirements
- **Batch Comparison**: Compare results across different processing sessions

## 📊 Output Format

The decoder provides comprehensive results in both console and CSV formats:

### Console Output
The results are displayed in a tabulated format with timestamps:

```
********************************************* RESULTS *********************************************

┌──────┬─────────────────────┬─────────────────────────────────────────────────┬─────────────────────────────────────────┐
│ S.No │ TimeStampIST        │ ImageFile                                       │ DecodedData                             │
├──────┼─────────────────────┼─────────────────────────────────────────────────┼─────────────────────────────────────────┤
│ 1    │ 2025-07-19 02:45:30 PM │ S00001_F1_C1_N001_P165_B1_20250717103204536.jpg│ [Decoded DataMatrix Content]            │
│ 2    │ 2025-07-19 02:45:31 PM │ S00003_F1_C3_N001_P165_B1_20250717103204552.jpg│ [Decoded DataMatrix Content]            │
│ 3    │ 2025-07-19 02:45:32 PM │ S00004_F1_C4_N001_P165_B1_20250717103204536.jpg│ DataMatrix out of focus or not found    │
└──────┴─────────────────────┴─────────────────────────────────────────────────┴─────────────────────────────────────────┘

********************************************* END *********************************************
```

### CSV Export
Results are automatically exported to CSV files with the following features:
- **Automatic Timestamping**: Files named with processing timestamp (e.g., `2025-07-19 02-45-30 PM.csv`)
- **Structured Data**: Organized with S.No, TimeStampIST, ImageFile, and DecodedData columns
- **Reports Directory**: All CSV files saved in `reports/` directory (auto-created)
- **IST Timestamps**: Each processed image gets an Indian Standard Time timestamp

**CSV Format:**
```csv
S.No,TimeStampIST,ImageFile,DecodedData
1,2025-07-19 02:45:30 PM,S00001_F1_C1_N001_P165_B1_20250717103204536.jpg,[Decoded DataMatrix Content]
2,2025-07-19 02:45:31 PM,S00003_F1_C3_N001_P165_B1_20250717103204552.jpg,[Decoded DataMatrix Content]
3,2025-07-19 02:45:32 PM,S00004_F1_C4_N001_P165_B1_20250717103204536.jpg,DataMatrix out of focus or not found
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

4. **CSV export issues**
   - Ensure write permissions in the project directory
   - Check available disk space
   - Verify the `reports/` directory can be created

### Performance Tips

- Use appropriate image resolution (recommended: 1224x1024 after resizing)
- Ensure good lighting conditions during image capture
- Clean the DataMatrix surface before imaging
- Use machine-specific configurations for best results
- Monitor CSV reports for pattern analysis and quality improvements

## 🧪 Testing

Use the provided Jupyter notebook for interactive testing:

```bash
jupyter notebook testing.ipynb
```

The notebook provides:
- Step-by-step preprocessing visualization
- Parameter tuning capabilities
- Performance analysis tools
- CSV export validation and analysis

**Testing CSV Export:**
After running the decoder, check the `reports/` directory for generated CSV files. You can verify:
- Timestamp accuracy
- Data integrity
- Proper formatting
- Sequential numbering

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
