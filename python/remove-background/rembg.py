from PIL import Image
from rembg import remove

def remove_background(input_path, output_path):
    # Open the input image
    with open(input_path, 'rb') as i:
        input_data = i.read()
        
    # Remove the background using rembg
    output_data = remove(input_data)
    
    # Save the result as a PNG (required for transparency)
    with open(output_path, 'wb') as o:
        o.write(output_data)

# Example usage
remove_background("input.jpg", "output.png")

