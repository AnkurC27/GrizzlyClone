import pandas as pd
from selenium import webdriver
from docx import Document
from docx.shared import Inches
from PIL import Image
import os
import time
import datetime
from urllib.parse import urlparse
from PIL import Image, ImageDraw, ImageFont

# load the excel file
excel_file_path = r'C:\Users\ankur.chadha\Desktop\GrizzlyProject\excel\linksca.xlsx'
lumber_df = pd.read_excel(excel_file_path)

# set up selenium with edge
edgedriver_path = r'C:\Users\ankur.chadha\desktop\msedgedriver'
os.environ["PATH"] += os.pathsep + edgedriver_path
edge_options = webdriver.EdgeOptions()
driver = webdriver.Edge(options=edge_options)
driver.maximize_window()

# get the column index of the 'Vendor' header
vendor_col_index = lumber_df.columns.get_loc('HomeDepot')
vendor_col_index_2 = lumber_df.columns.get_loc('BuildClub')
vendor_col_index_3 = lumber_df.columns.get_loc('AshbyLumber')
vendor_col_index_4 = lumber_df.columns.get_loc('Best')
vendor_col_index_5 = lumber_df.columns.get_loc('CloseLumber')
vendor_col_index_6 = lumber_df.columns.get_loc('WhiteCap')

# get the column index of the 'Item Number' and 'Description' header
item_col_index = lumber_df.columns.get_loc('Item#')
desc_col_index = lumber_df.columns.get_loc('Description')


def add_watermark(screenshot_filename, item_number, description):
    img = Image.open(screenshot_filename)

    # width of the border in pixels
    border_width = 10

    #create a new image with size increased by twice the border width
    new_img = Image.new("RGB", (img.width +2 * border_width, img.height +2 * border_width), "black")

    # paste the original image at an offset of the border width
    new_img.paste(img, (border_width, border_width))

    draw = ImageDraw.Draw(new_img)
    date_time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    watermark_text = f"{item_number}, {description}, {date_time}"
    position = (10, 10)
    font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 30)
    color = "black" 
    stroke_color = "white"
    stroke_width = 2
    background_color = "yellow"

    # Get image and text dimensions
    img_width, img_height = img.size
    text_width, text_height = draw.textsize(watermark_text, font=font)

    position = (new_img.width - text_width - 10, new_img.height - text_height -10)
    padding = 10

    draw.rectangle([position[0]-padding, position[1]-padding, position[0]+text_width+padding, position[1]+text_height+padding], fill=background_color)

    draw.text(position, watermark_text, font=font, fill=color, stroke_width=stroke_width, stroke_fill=stroke_color)
    new_img.save(screenshot_filename)

screenshot_filenames = []

# Iterate over the rows of the excel file
for index, row in lumber_df.iterrows():
    vendor_1 = row[vendor_col_index]
    vendor_2 = row[vendor_col_index_2]
    vendor_3 = row[vendor_col_index_3]
    vendor_4 = row[vendor_col_index_4]
    vendor_5 = row[vendor_col_index_5]
    vendor_6 = row[vendor_col_index_6]

    item_number = str(row[item_col_index])
    description = str(row[desc_col_index])
    if pd.isnull(item_number):
        break

    vendors = [vendor_1, vendor_2, vendor_3, vendor_4, vendor_5, vendor_6]
    vendor_names = ['HomeDepot', 'BuildClub', 'AshbyLumber', 'Best', 'CloseLumber', 'WhiteCap']

    # create a folder with the date to store screenshots
    date_str = datetime.datetime.now().strftime("%m%d%Y")
    folder_name = 'lumberca_' + date_str

    if not os.path.exists(folder_name):
        try:
            os.mkdir(folder_name)
            print(f"Directory '{folder_name}' created.")
        except Exception as e:
            print(f"Could not create directory. Error: {str(e)}")

    for vendor_url, vendor_name in zip(vendors, vendor_names):
        # check if vendor is not null before opening link
        if pd.isna(vendor_url) or not str(vendor_url).strip():
            continue

        print(f"Processing URL: {vendor_url}")   
        driver.get(vendor_url)
        
        # adds condition to menards url to solve captcha
        wait_time = 3
        if "buildclub.com" in vendor_url:
            wait_time = 8
        
        time.sleep(wait_time)

        description = str(row[desc_col_index]).replace('\'', '_').replace('\"', '_').replace('-', ' ').replace('/', '_')

        #Take a screenshot
        screenshot_filename = f'{folder_name}/{description}_{vendor_name}.png'
        driver.save_screenshot(screenshot_filename)
        add_watermark(screenshot_filename, item_number, description)

        screenshot_filenames.append(screenshot_filename)

# Paste screenshot to pdf 
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

date_str = datetime.datetime.now().strftime("%m.%d.%Y")
c = canvas.Canvas(f"Lumber Rates CA {date_str}.pdf", pagesize=letter)

page_width, page_height = letter 

for screenshot_filename in screenshot_filenames:
    with Image.open(screenshot_filename) as img:
        img_width, img_height = img.size
    c.drawImage(screenshot_filename, 50, 500, width=500, height=300)
    c.showPage()

c.save()