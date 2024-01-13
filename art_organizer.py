import os
import shutil
from PIL import Image
# import tkinter as tk
# from tkinter import filedialog

def get_checkpoint_from_image(image_path):
    # Implement your logic to extract model/checkpoint information
    def get_model_from_metadata(image_path):
        with Image.open(image_path) as img:
            metadata = img.info

        # Extract the 'parameters' string from the metadata dictionary
        parameters_string = metadata.get('parameters', '')

        # Search for 'Model: ' in the parameters string
        model_start = parameters_string.find('Model: ')
        if model_start != -1:
            # If 'Model: ' is found, extract the substring after it until the next comma or the end of the string
            model_end = parameters_string.find(',', model_start)
            if model_end == -1:
                model_end = len(parameters_string)
            model = parameters_string[model_start + len('Model: '):model_end].strip()
            return model

        return None
    
    model = get_model_from_metadata(image_path)

    if model is not None:
        print("Model:", model)
        return model
    else:
        print("Model information not found in metadata.")

def move_image_to_folder(image_path, checkpoint, destination_folder):
    destination_folder = os.path.join(destination_folder, f"{checkpoint}_Folder")
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    destination_path = os.path.join(destination_folder, os.path.basename(image_path))
    
    shutil.copy(image_path, destination_path)
    print(f"Copied and moved {image_path} to {destination_path}")

def process_images_in_folder(source_folder, destination_folder):
    for root, _, files in os.walk(source_folder):
        for filename in files:
            if filename.endswith(".png"):
                image_path = os.path.join(root, filename)

                checkpoint = get_checkpoint_from_image(image_path)

                move_image_to_folder(image_path, checkpoint, destination_folder)

def main():
    source_folder = "YourPathHere"
    destination_folder = "YourPathHere"
    
    process_images_in_folder(source_folder, destination_folder)

if __name__ == "__main__":
    main()

#  # Future GUI setup
# root = tk.Tk()
# root.title("Image Processing App")

# source_folder_var = tk.StringVar()
# destination_folder_var = tk.StringVar()

# tk.Label(root, text="Source Folder:").pack()
# tk.Entry(root, textvariable=source_folder_var, width=50).pack()
# tk.Button(root, text="Select Source Folder", command=on_select_source_folder).pack()

# tk.Label(root, text="Destination Folder:").pack()
# tk.Entry(root, textvariable=destination_folder_var, width=50).pack()
# tk.Button(root, text="Select Destination Folder", command=on_select_destination_folder).pack()

# tk.Button(root, text="Process Images", command=on_process).pack()

# root.mainloop()