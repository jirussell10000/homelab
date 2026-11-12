import sys
import os

from PIL import Image, ImageOps

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
    output = filename + "-inverted." + extension
    invert_image(infile, output)


def invert_image(input_path, output_path):
    # Open the input image
    try:
        with Image.open(input_path) as img:
            if img.mode == 'RGBA':
                r,g,b,a = img.split()

                # Bring RGB together and remove the alpha channel
                rgb_image = Image.merge('RGB',(r,g,b))
                inverted_rgb = ImageOps.invert(rgb_image)
                r2,g2,b2 = inverted_rgb.split()
                inverted_img = Image.merge('RGBA',(r2,g2,b2,a))
            else:
                # Convert image to RGB before inverting
                if img.mode not in ('L','RGB'):
                    img = img.convert('RGB')

                inverted_img = ImageOps.invert(img)

            inverted_img.save(output_path)
            print(f"Successfully inverted image saved to: {output_path}")
    
    except Exception as e:
        print(f"An error occured: {e}")


def get_extension(file):
    file = file.casefold()
    file = file.replace(' ','')
    file = file.split('.')

    return file[0], file[1]


if __name__ == "__main__":
    main()
