import os
import shutil
from PIL import Image
import tkinter as tk
from tkinter import filedialog

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

def on_select_source_folder():
    source_folder_var.set(filedialog.askdirectory())

def on_select_destination_folder():
    destination_folder_var.set(filedialog.askdirectory())

def on_process():
    source_folder = source_folder_var.get()
    destination_folder = destination_folder_var.get()

    process_images_in_folder(source_folder, destination_folder)

# GUI setup
root = tk.Tk()
root.title("AI Image Organization App")

root.configure(bg="#323232")

source_folder_var = tk.StringVar()
destination_folder_var = tk.StringVar()

frame_title = tk.Frame(root, width=10, height=75, bg='#323232')
frame_title.pack(fill=tk.X)

title_label = tk.Label(frame_title, text="AI Image Organization App", font=("Arial", 18), bg='#323232', fg='#b6b6b6')
title_label.pack(side=tk.LEFT, padx=5)

title_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Frame for Source Folder
frame_source = tk.Frame(root, padx=10, pady=10, bg='#323232')
frame_source.pack(fill=tk.X)

tk.Label(frame_source, text="Source Folder:", font=("Arial", 12), bg='#323232', fg='#b6b6b6').pack(side=tk.LEFT, padx=5)
entry_source = tk.Entry(frame_source, textvariable=source_folder_var, width=40, font=("Arial", 12), bg='#b6b6b6', fg='#1b1a1b', border=0)
entry_source.pack(side=tk.LEFT, padx=35)
tk.Button(frame_source, text="Select", command=on_select_source_folder, font=("Arial", 12), bg='#b6b6b6', fg='#1b1b1b').pack(side=tk.LEFT, padx=0)

# Frame for Destination Folder
frame_destination = tk.Frame(root, padx=10, pady=10, bg='#323232')
frame_destination.pack(fill=tk.X)

tk.Label(frame_destination, text="Destination Folder:", font=("Arial", 12), bg='#323232', fg='#b6b6b6').pack(side=tk.LEFT, padx=5)
entry_destination = tk.Entry(frame_destination, textvariable=destination_folder_var, width=40, font=("Arial", 12), bg='#b6b6b6', fg='#1b1a1b', border=0)
entry_destination.pack(side=tk.LEFT, padx=5)
tk.Button(frame_destination, text="Select", command=on_select_destination_folder, font=("Arial", 12), bg='#b6b6b6', fg='#1b1b1b').pack(side=tk.LEFT, padx=30)

# Process Button
tk.Button(root, text="Process Images", command=on_process, font=("Arial", 14), bg="#48889c", fg="white", relief=tk.GROOVE, width=15, height=2).pack(pady=20)

root.mainloop()

# def main():
#     source_folder = "test-source-directory"
#     destination_folder = "test-destination-directory"
    
#     process_images_in_folder(source_folder, destination_folder)

# if __name__ == "__main__":
#     main()
