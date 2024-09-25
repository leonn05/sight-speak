import os
import io
import cv2
import numpy as np
from tkinter import Tk, Button, filedialog, Text, Scrollbar, messagebox, Label
from google.cloud import vision
import pyttsx3

# Set the path to your Google Cloud credentials JSON file
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'<file of API key>'

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def perform_all_operations():
    file_path = filedialog.askopenfilename()

    if not file_path:
        show_warning("Please select an image.")
        return

    try:
        # Object Detection
        img, objects_result = perform_object_detection(file_path)
        show_object_detection_visualization(img)

        # Image Labeling
        labels_result = perform_image_labeling(file_path)

        # OCR
        ocr_result = process_ocr(file_path)
        show_ocr_visualization(file_path)

        # Display results in Tkinter window
        display_results(objects_result, labels_result, ocr_result)
    except Exception as e:
        show_warning(f"Error processing the image: {str(e)}")

def convert_text_to_speech(text):
    if text:
        # Set the speech rate (you can experiment with different values)
        rate = 175
        engine.setProperty('rate', rate)

        # Get an estimation of the speech duration
        duration = get_speech_duration(text)

        engine.say(text)
        engine.runAndWait()

        # Display the duration in a label
        duration_label.config(text=f"Speech Duration: {duration:.2f} seconds")

def get_speech_duration(text):
    # A simple estimation of the speech duration based on the text length
    # Adjust this factor based on your observations
    duration_per_word = 0.15  # seconds
    words = len(text.split())
    return words * duration_per_word

def perform_object_detection(file_path):
    with io.open(file_path, 'rb') as image_file:
        content = image_file.read()

    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=content)
    response = client.object_localization(image=image)

    objects = response.localized_object_annotations

    img = cv2.imdecode(np.frombuffer(content, np.uint8), -1)

    for obj in objects:
        bounding_box = obj.bounding_poly.normalized_vertices
        x0, y0 = int(bounding_box[0].x * img.shape[1]), int(bounding_box[0].y * img.shape[0])
        x1, y1 = int(bounding_box[2].x * img.shape[1]), int(bounding_box[2].y * img.shape[0])

        cv2.rectangle(img, (x0, y0), (x1, y1), (0, 255, 0), 2)
        font_size = max(0.5, min(1.0, (x1 - x0) / 100.0))
        cv2.putText(img, obj.name, (x0, y0 - 5), cv2.FONT_HERSHEY_SIMPLEX, font_size, (255, 0, 0), 2)

    return img, objects

def perform_image_labeling(file_path):
    with io.open(file_path, 'rb') as image_file:
        content = image_file.read()

    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=content)
    response = client.label_detection(image=image)

    labels = response.label_annotations
    label_descriptions = "\n".join(label.description for label in labels)

    return label_descriptions

def process_ocr(file_path):
    with io.open(file_path, 'rb') as f:
        content = f.read() 

    vision_client = vision.ImageAnnotatorClient()
    image = vision.Image(content=content)

    response = vision_client.text_detection(image=image)

    img = cv2.imdecode(np.frombuffer(content, np.uint8), -1)

    for text in response.text_annotations[1:]:
        vertices = [(vertex.x, vertex.y) for vertex in text.bounding_poly.vertices]

        for i in range(len(vertices)):
            cv2.line(img, vertices[i], vertices[(i+1)%len(vertices)], (0, 255, 0), 2)

        cv2.putText(img, text.description, (vertices[0][0], vertices[0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    return img, response.text_annotations

def show_object_detection_visualization(img):
    # Resize the image for visualization
    resized_img = resize_image(img, 900, 700)
    
    cv2.imshow('Object Detection', resized_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def show_ocr_visualization(file_path):
    img, _ = process_ocr(file_path)
    
    # Resize the image for visualization
    resized_img = resize_image(img, 900, 700)
    
    cv2.imshow('OCR Visualization', resized_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def resize_image(image, max_width, max_height):
    height, width = image.shape[:2]
    aspect_ratio = width / height

    if width > max_width:
        new_width = max_width
        new_height = int(new_width / aspect_ratio)
    elif height > max_height:
        new_height = max_height
        new_width = int(new_height * aspect_ratio)
    else:
        return image

    return cv2.resize(image, (new_width, new_height))

def display_results(objects_result, labels_result, ocr_result):
    result_text.delete(1.0, "end")  # Clear previous content

    # Extract relevant information from objects_result
    objects_info = [obj.name for obj in objects_result]

    # Extract description from OCR result
    ocr_info = ocr_result[1][0].description if ocr_result else ""

    # Add content to the Text widget
    result_text.insert("1.0", f"Object Detection Result:\n{', '.join(objects_info)}\n\nImage Labeling Result:\n{labels_result}\n\nOCR Result:\n{ocr_info}")

    # Add Play button
    play_button = Button(root, text="Play", command=lambda: convert_text_to_speech(ocr_info), font=("Arial", 14), relief="flat", bg="#3498db", fg="white", padx=20, pady=10)
    play_button.pack(pady=5)

def show_warning(message):
    messagebox.showwarning("Warning", message)

root = Tk()
root.title("Google Cloud Vision API Operations")

window_width = 900
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width / 2) - (window_width / 2)
y_coordinate = (screen_height / 2) - (window_height / 2)
root.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))

select_button = Button(root, text="Select Image", command=perform_all_operations, font=("Arial", 14), relief="flat", bg="#4CAF50", fg="white", padx=20, pady=10)
select_button.pack(pady=20)

result_text = Text(root, wrap="word", font=("Arial", 12), height=10)
result_text.pack(expand=True, fill="both", padx=10, pady=10)

scrollbar = Scrollbar(root, command=result_text.yview)
scrollbar.pack(side="right", fill="y")
result_text.config(yscrollcommand=scrollbar.set)

duration_label = Label(root, text="", font=("Arial", 12))
duration_label.pack(pady=5)

exit_button = Button(root, text="Exit", command=root.quit, font=("Arial", 14), relief="flat", bg="#FF5733", fg="white", padx=22, pady=12)
exit_button.pack(pady=17)

root.mainloop()