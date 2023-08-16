import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from PIL import Image
import datetime

# Define the parent directory where the folders are located
parent_dir = r'C:\Users\ankur.chadha\Desktop\GrizzlyProject\Sales2024'

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
            
            # Iterate through each file in the folder
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                
                # Make sure it's a png file
                if os.path.isfile(file_path) and file_path.lower().endswith(".png"):
                    try:
                        # Open the image file
                        with Image.open(file_path) as img:
                            # Resize image to fit on a letter page with a bit of margin
                            img_width, img_height = img.size
                            width = page_width - 2*50
                            height = width * img_height / img_width
                            if height > page_height - 3*50:  # 3*50 to account for filename space at the top
                                # Image is too tall; adjust size by height instead of width
                                height = page_height - 3*50
                                width = height * img_width / img_height

                            # Draw the file name on the canvas at the top
                            c.setFont("Helvetica", 10)
                            text_width = pdfmetrics.stringWidth(file_name, "Helvetica", 10)
                            c.drawString((page_width - text_width) / 2, page_height - 30, file_name)  # 30 is the margin for text at the top
                            
                            # Draw image on the canvas just below the text
                            c.drawImage(file_path, 50, page_height - 80 - height, width=width, height=height)  # 80 is the combined space for text and margin

                            c.showPage()

                    except Exception as e:
                        print(f"Could not process file {file_name}. Error: {str(e)}")
                        
            c.save()