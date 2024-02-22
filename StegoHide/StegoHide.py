from PIL import Image
import os
from colorama import Fore


print(Fore.RED + '''

⠤⣤⣤⣤⣄⣀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣠⣤⠤⠤⠴⠶⠶⠶⠶
⢠⣤⣤⡄⣤⣤⣤⠄⣀⠉⣉⣙⠒⠤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠴⠘⣉⢡⣤⡤⠐⣶⡆⢶⠀⣶⣶⡦
⣄⢻⣿⣧⠻⠇⠋⠀⠋⠀⢘⣿⢳⣦⣌⠳⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠞⣡⣴⣧⠻⣄⢸⣿⣿⡟⢁⡻⣸⣿⡿⠁
⠈⠃⠙⢿⣧⣙⠶⣿⣿⡷⢘⣡⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⣿⣿⣷⣝⡳⠶⠶⠾⣛⣵⡿⠋⠀⠀
⠀⠀⠀⠀⠉⠻⣿⣶⠂⠘⠛⠛⠛⢛⡛⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠛⠀⠉⠒⠛⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⢸⠃
⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⣾
⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⣿
⠀⠀⠀⠀⠀⠀⢻⡁⠀⠀⠀⠀⠀⢸
⠀⠀⠀⠀⠀⠀⠘⡇
⠀⠀⠀⠀⠀⠀⠀⡇
⠀⠀⠀⠀⠀⠀⠀⠿
Instagram: f8le
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀''')
def hide_data_in_image(data_bytes, cover_image_path, output_image_path):
    # Open the cover image
    cover_image = Image.open(cover_image_path)
    
    # Get the width and height of the cover image
    width, height = cover_image.size
    
    # Check if the cover image is large enough to hide the data
    if len(data_bytes) > width * height * 3 // 8:
        print (Fore.YELLOW + 'Cover image is too small to hide the data.' + Fore.WHITE)
        return
    
    # Hide the data in the cover image
    data_index = 0
    for y in range(height):
        for x in range(width):
            pixel = list(cover_image.getpixel((x, y)))
            for i in range(3):
                if data_index < len(data_bytes) * 8:
                    # Get the least significant bit of the pixel value
                    lsb = data_bytes[data_index // 8] >> (7 - data_index % 8) & 1
                    # Replace the least significant bit of the pixel value with the data bit
                    pixel[i] = (pixel[i] & ~1) | lsb
                    data_index += 1
            cover_image.putpixel((x, y), tuple(pixel))
    
    # Save the modified image with the hidden data
    cover_image.save(output_image_path)
    print (Fore.YELLOW + 'Data hidden successfully in the image.' + Fore.WHITE)

def extract_data_from_image(image_path, output_file_path):
    # Open the image containing hidden data
    image = Image.open(image_path)
    
    # Extract data from the image
    data_bytes = bytearray()
    width, height = image.size
    data_index = 0
    for y in range(height):
        for x in range(width):
            pixel = list(image.getpixel((x, y)))
            for i in range(3):
                # Extract the least significant bit of the pixel value
                lsb = pixel[i] & 1
                # Add the extracted bit to the data bytes
                data_bytes.append(lsb)
                data_index += 1
    
    # Write the extracted data to a file
    with open(output_file_path, 'wb') as f:
        f.write(bytes(data_bytes))
    print(Fore.YELLOW + 'Data extracted successfully.' + Fore.WHITE)

def get_file_bytes(file_path):
    with open(file_path, 'rb') as file:
        return bytearray(file.read())

if __name__ == "__main__":
    # Paths to the data file, cover image, and output image
    data_file_path = input(Fore.GREEN + 'Enter the path to the file you want to hide: ' + Fore.WHITE)
    cover_image_path = input(Fore.GREEN + 'Enter the path to the cover image: ' + Fore.WHITE)
    output_image_path = input(Fore.GREEN + 'Enter the path for the output image with hidden data: ' + Fore.WHITE)
    
    # Convert file to bytes
    data_bytes = get_file_bytes(data_file_path)
    
    # Hide data in the cover image
    hide_data_in_image(data_bytes, cover_image_path, output_image_path)
    
    # Extract data from the image with hidden data
    extracted_data_file_path = input(Fore.GREEN + 'Enter the path for the extracted data file: ' + Fore.WHITE)
    extract_data_from_image(output_image_path, extracted_data_file_path)
