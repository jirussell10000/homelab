import sys

from PIL import Image
from rembg import remove

import tkinter as tk
from tkinter import filedialog

def main():
    root = tk.Tk()
    root.withdraw() # Hide the root window
    infile = filedialog.askopenfilename(title="Select an image file", 
                                        filetypes=[("PNG", "*.png"),
                                                   ("JPEG", "*.jpg *.jpeg")])
    if not infile:
        sys.exit("info: No file selected.")
    
    filename, extension = get_extension(infile)

    output = filename + "-rembg." + extension
    
    remove_background(infile, output)


def remove_background(input_path, output_path):
    # Open the input image
    with open(input_path, 'rb') as i:
        input_data = i.read()
        
    # Remove the background using rembg
    output_data = remove(input_data)
    
    # Save the result as a PNG (required for transparency)
    with open(output_path, 'wb') as o:
        o.write(output_data)


def get_extension(file):
    file = file.casefold()
    file = file.replace(' ','')
    file = file.split('.')

    return file[0], file[1]


if __name__ == "__main__":
    main()
