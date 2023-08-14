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
from selenium.common.exceptions import TimeoutException


# load the excel file
excel_file_path = r'C:\Users\ankur.chadha\Desktop\GrizzlyProject\excel\SalesMaster2024.xlsx'
sheet_to_read = "ScriptLinks"
rates_df = pd.read_excel(excel_file_path, sheet_name=sheet_to_read, skiprows=55)

# set up selenium with edge
edgedriver_path = r'C:\Users\ankur.chadha\desktop\msedgedriver'
os.environ["PATH"] += os.pathsep + edgedriver_path
edge_options = webdriver.EdgeOptions()
driver = webdriver.Edge(options=edge_options)
driver.maximize_window()

# get the column index of the 'Vendor' header
link_col_index = rates_df.columns.get_loc('Link1')
link_col_index_2 = rates_df.columns.get_loc('Link2')
link_col_index_3 = rates_df.columns.get_loc('Link3')

# get the column index of the 'Item Number' and 'Description' header
item_col_index = rates_df.columns.get_loc('Item#')
desc_col_index = rates_df.columns.get_loc('Description')

def determine_folder(item_number):
    item_str = str(item_number)
    # Check the prefix of the item number
    if item_str.startswith(('M', 'D', 'H', 'BAT')) or item_str[0].isdigit():
        return 'Consumables'
    elif item_str.startswith('S'):
        return 'Saftey'
    elif item_str.startswith('A'):
        return 'Apparel'
    elif item_str.startswith('G'):
        return 'Signs'
    elif item_str.startswith('COMP'):
        return 'COMP'
    else:
        # Default folder if none of the conditions match. 
        # Can be adjusted 
        return 'Other'


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
for index, row in rates_df.iterrows():
    link_1 = row[link_col_index]
    link_2 = row[link_col_index_2]
    link_3 = row[link_col_index_3]

    item_number = row[item_col_index]
    description = str(row[desc_col_index])
    if pd.isnull(item_number):
        break

    vendors = [link_1, link_2, link_3,]
    vendor_names = ["Vendor1", "Vendor2", "Vendor3"]

    # create a folder with the date to store screenshots
    date_str = datetime.datetime.now().strftime("%m.%d.%Y")
    folder_name = determine_folder(item_number)

    if not os.path.exists(folder_name):
        try:
            os.mkdir(folder_name)
            print(f"Directory '{folder_name}' created.")
        except Exception as e:
            print(f"Could not create directory. Error: {str(e)}")

    for vendor_url in vendors:
        # check if vendor is not null before opening link
        if pd.isna(vendor_url) or not str(vendor_url).strip():
            continue

        parsed_url = urlparse(vendor_url)
        vendor_netloc = parsed_url.netloc 

        parts = vendor_netloc.split('.')
        vendor_name = parts[1]
        
        print(f"Processing URL: {vendor_url}, Vendor: {vendor_name}")
        
        try:
            driver.set_page_load_timeout(30)   
            driver.get(vendor_url)
        except TimeoutException:
            print(f"Timed out waiting for the page to load: {vendor_url}")
            continue

        # adds wait condition to solve captcha 
        wait_time = 10
        time.sleep(wait_time)

        description = str(row[desc_col_index]).replace('\'', '_').replace('\"', '_').replace('-', ' ').replace('/', '_').replace('&','').replace('#','')

        #Take a screenshot
        screenshot_filename = f'{folder_name}/{row["Item#"]}_{description}_{vendor_name}_{index}.png'
        driver.save_screenshot(screenshot_filename)
        add_watermark(screenshot_filename, item_number, description)
        driver.delete_all_cookies()
        screenshot_filenames.append(screenshot_filename)


# Close the web driver
driver.quit()