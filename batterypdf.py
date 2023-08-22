import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from PIL import Image
import datetime

def get_item_number_from_filename(filename):
    """Extract the item number from the filename."""
    parts = filename.split('_')
    if "addon" in filename.lower():
        return parts[1]  # The structure is expected to be like "battery_ITEMNUMBER_description_vendor_index.png"
    return parts[0]  # The structure is expected to be like "ITEMNUMBER_description_vendor_index.png"

# Define the parent directory where the folders are located
parent_dir = r'C:\Users\ankur.chadha\Desktop\GrizzlyProject\AddOns'

# Iterate through each folder in the parent directory
for folder_name in os.listdir(parent_dir):
    # Check if folder name starts with a number
    if folder_name[0].isdigit():
        folder_path = os.path.join(parent_dir, folder_name)
        
        # Make sure it's actually a folder (not a file or a symlink)
        if os.path.isdir(folder_path):
            pdf_filename = f"{folder_path}/{folder_name} Screenshots {datetime.datetime.now().strftime('%m.%d.%Y')}.pdf"
            c = canvas.Canvas(pdf_filename, pagesize=letter)
            page_width, page_height = letter
            
            grouped_files = {}  # This will store filenames grouped by item numbers.
            
            # Group the files by their item numbers.
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                if os.path.isfile(file_path) and file_path.lower().endswith(".png"):
                    item_number = get_item_number_from_filename(file_name)
                    if item_number not in grouped_files:
                        grouped_files[item_number] = []
                    grouped_files[item_number].append(file_path)

            for item_number, files in grouped_files.items():
                if len(files) > 1:  # This ensures that there is at least a battery and a part screenshot.
                    part_file = [f for f in files if "Addon" not in f.lower()][0]  # Take the first non-battery/addon screenshot as the part screenshot.
                    addon_file = [f for f in files if "Addon" in f.lower()][0]  # Take the first addon screenshot.

                    # Draw the part image.
                    with Image.open(part_file) as img:
                        img_width, img_height = img.size
                        width = page_width - 2*50
                        height = (page_height / 2 - 3*50) * img_height / img_width  # Adjust for half page height.
                        if height > page_height / 2 - 3*50:  # 3*50 to account for filename space at the top
                            height = page_height / 2 - 3*50
                            width = height * img_width / img_height
                        c.drawImage(part_file, 50, page_height - 80 - height, width=width, height=height)  # 80 is the space for text at the top

                    # Draw the addon image.
                    with Image.open(addon_file) as img:
                        img_width, img_height = img.size
                        width = page_width - 2*50
                        height = (page_height / 2 - 3*50) * img_height / img_width  # Adjust for half page height.
                        if height > page_height / 2 - 3*50:
                            height = page_height / 2 - 3*50
                            width = height * img_width / img_height
                        c.drawImage(addon_file, 50, page_height / 2 - 30 - height, width=width, height=height)  # Adjusted position for half page.

                    c.showPage()
                        
            c.save()
