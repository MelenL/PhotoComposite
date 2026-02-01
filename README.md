# PhotoComposite 10x15

**Author:** Melen Laclais  
**License:** [Creative Commons Zero v1.0 Universal (Public Domain)](https://creativecommons.org/publicdomain/zero/1.0/)  
**Live Demo:** [photocomposite.streamlit.app](https://photocomposite.streamlit.app/#photo-composite-10x15)

## Overview
PhotoComposite 10x15 is a functional utility designed for the algorithmic tiling of digital images onto a standard 10x15cm (4x6") print format. The primary objective of this tool is to optimize physical print space, allowing for cost-efficient photo development without the loss of image data or intentional cropping.

## Technical Specifications
The system utilizes the `Pillow` library to perform high-fidelity image manipulations. Key technical features include:

* **Dynamic Layout Engine**: Supports 2, 4, or 8 image divisions per composite sheet.
* **Aspect Ratio Preservation**: Implements a "fit-to-canvas" logic that preserves the original proportions of every uploaded file.
* **Automated Orientation Correction**: Evaluates EXIF metadata to correct image rotation and automatically orients portrait images to landscape to maximize pixel density within the grid cells.
* **High-Resolution Output**: Generates JPEG files at 300 DPI (1800x1200 px), ensuring professional print quality.

## Deployment & Usage
The application is hosted on **Streamlit Cloud**. You can access the interface directly here: [photocomposite.streamlit.app](https://photocomposite.streamlit.app/#photo-composite-10x15)

### Local Execution:
1. Install dependencies:  
   `pip install streamlit Pillow`
2. Launch the application:  
   `streamlit run app.py`

## Usage Instructions
1. Select the desired density (2, 4, or 8 photos per sheet) using the sidebar.
2. Upload image files (JPG, PNG, WebP).
3. Generate and download the processed composites as a consolidated ZIP archive.

---
**Public Domain Dedication:** This work has been marked as dedicated to the public domain. You can copy, modify, distribute and perform the work, even for commercial purposes, all without asking permission.
