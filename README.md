# sight-speak


This application leverages Google Cloud Vision API to perform various image analysis tasks, including object detection, image labeling, and Optical Character Recognition (OCR). It provides a user-friendly interface built with Tkinter and incorporates text-to-speech functionality for reading OCR results.

## Features

- Object Detection: Identifies and localizes multiple objects in an image.
- Image Labeling: Generates relevant labels for the content of an image.
- Optical Character Recognition (OCR): Extracts and displays text from images.
- Text-to-Speech: Reads aloud the OCR results.
- Visualization: Displays the results of object detection and OCR on the image.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7 or higher
- pip (Python package manager)
- A Google Cloud Platform account with the Vision API enabled
- Google Cloud credentials (JSON key file)

## Installation

1. Clone the repository or download the source code.

2. Install the required Python packages:

   ```
   pip install opencv-python-headless numpy google-cloud-vision pyttsx3
   ```

3. Set up Google Cloud credentials:
   - Place your Google Cloud JSON key file in a secure location on your computer.
   - Update the `GOOGLE_APPLICATION_CREDENTIALS` path in the script to point to your JSON key file:

     ```python
     os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'path/to/your/credentials.json'
     ```

## Usage

1. Run the script:

   ```
   python image_analysis_app.py
   ```

2. The application window will open. Click the "Select Image" button to choose an image file for analysis.

3. The application will perform object detection, image labeling, and OCR on the selected image.

4. Results will be displayed in the application window.

5. Click the "Play" button to hear the OCR results read aloud.

6. Use the "Exit" button to close the application.

## Notes

- The application resizes large images for better visualization. The original image is still used for analysis.
- Speech duration is estimated based on the length of the OCR text. Actual duration may vary.
- Ensure your system's audio is working correctly for the text-to-speech feature.

## Troubleshooting

- If you encounter any issues with Google Cloud authentication, verify that your credentials file is correctly set up and the path is properly specified in the script.
- For any other issues, check the console for error messages which may provide more information about the problem.

## Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request with your changes.


