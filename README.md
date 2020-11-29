# InvelonChallenge

### Project Structure:
* Crawler. Crawls thingiverse and downloads the .tls files and their categories
* Preprocessing
    * Read .stl file (numpy-stl).
    * Generate one or more rotations and translations of the 3D model (numpy-stl).
    * Save result into rgb image
    * Convert rgb image into grayscale image (Pillow)
* Datasets
    * Small: 2 categories
    * Medium: 5 categories
    * Large: 11 categories
* Models
    * Xception
    * DenseNet
    * MobileNetV2