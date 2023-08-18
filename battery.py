# 1. Imports and Global Constants
import pandas as pd
from selenium import webdriver
from PIL import Image, ImageDraw, ImageFont
import os
import time
import datetime
from urllib.parse import urlparse
from selenium import webdriver
from selenium.common.exceptions import TimeoutException

EXCEL_FILE_PATH = r'C:\Users\ankur.chadha\Desktop\GrizzlyProject\excel\RatesMaster2024.xlsx'
SHEET_NAME = "New Links"
EDGE_DRIVER_PATH = r'C:\Users\ankur.chadha\desktop\msedgedriver'
BATTERY_ITEMS_DIR = "Battery Items"


# 2. Configuration Setup
def setup_selenium():
    os.environ["PATH"] += os.pathsep + EDGE_DRIVER_PATH
    edge_options = webdriver.EdgeOptions()
    driver = webdriver.Edge(options=edge_options)
    driver.maximize_window()
    return driver


# 3. Directory Handling Functions
def create_directory(path):
    if not os.path.exists(path):
        try:
            os.mkdir(path)
            print(f"Directory '{path}' created.")
        except Exception as e:
            print(f"Could not create directory. Error: {str(e)}")


# 4. Watermarking Function
def add_watermark(screenshot_filename, item_number, description):
    img = Image.open(screenshot_filename)
    border_width = 10
    new_img = Image.new("RGB", (img.width + 2 * border_width, img.height + 2 * border_width), "black")
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

    img_width, img_height = img.size
    text_width, text_height = draw.textsize(watermark_text, font=font)

    position = (new_img.width - text_width - 10, new_img.height - text_height - 10)
    padding = 10

    draw.rectangle([position[0]-padding, position[1]-padding, position[0]+text_width+padding, position[1]+text_height+padding], fill=background_color)
    draw.text(position, watermark_text, font=font, fill=color, stroke_width=stroke_width, stroke_fill=stroke_color)
    new_img.save(screenshot_filename)


# 5. Screenshot Handling Function
def handle_screenshot(driver, folder_name, item_number, description, vendor_url, index, is_battery_item):
    parsed_url = urlparse(vendor_url)
    vendor_netloc = parsed_url.netloc
    parts = vendor_netloc.split('.')
    vendor_name = parts[1]
    
    # Add 'Battery' prefix in filename for Battery items
    filename_prefix = "Battery_" if is_battery_item else ""
    
    print(f"Processing URL: {vendor_url}, Vendor: {vendor_name}")

    screenshot_filename = f'{folder_name}/{filename_prefix}{item_number}_{description}_{vendor_name}_{index}.png'
    driver.save_screenshot(screenshot_filename)
    add_watermark(screenshot_filename, item_number, description)
    
    return screenshot_filename


# 6. Main Process Function
def process_links(driver, rates_df):
    screenshot_filenames = []
    
    for index, row in rates_df.iterrows():
        link_1 = row['Link1']
        link_2 = row['Link2']
        link_3 = row['Link3']
        battery = row['Battery']
        item_number = row['Item#']
        description = str(row['Description'])
        
        if pd.isnull(item_number):
            break
        
        vendors = [link_1, link_2, link_3, battery]
        
        folder_name = str(int(item_number / 100) * 100)
        is_battery_item = not pd.isna(battery) and str(battery).strip()
        
        # Determine the appropriate directory for the screenshots
        if is_battery_item:
            battery_items_path = os.path.join(os.getcwd(), BATTERY_ITEMS_DIR)
            create_directory(battery_items_path)
            
            item_folder_path = os.path.join(battery_items_path, folder_name)
            create_directory(item_folder_path)
        else:
            create_directory(folder_name)
        
        for vendor_idx, vendor_url in enumerate(vendors):
            if pd.isna(vendor_url) or not str(vendor_url).strip():
                continue
            
            try:
                driver.set_page_load_timeout(30)
                driver.get(vendor_url)
            except TimeoutException:
                print(f"Timed out waiting for the page to load: {vendor_url}")
                continue
            
            time.sleep(10)
            
            # Use item_folder_path as folder_name for Battery items
            screenshot_folder = item_folder_path if is_battery_item and vendor_idx == 3 else folder_name
            screenshot_filename = handle_screenshot(driver, screenshot_folder, item_number, description, vendor_url, index, is_battery_item and vendor_idx == 3)
            screenshot_filenames.append(screenshot_filename)
            driver.delete_all_cookies()
            
    return screenshot_filenames


# 7. Script Execution Block
if __name__ == '__main__':
    rates_df = pd.read_excel(EXCEL_FILE_PATH, sheet_name=SHEET_NAME)
    driver = setup_selenium()
    
    screenshot_filenames = process_links(driver, rates_df)
    
    # Close the web driver
    driver.quit()
