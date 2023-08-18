# GrizzlyClone is a mirror image of the original #GrizzlyProject 

Battery.py is a script meant for the rental rates that handles items with battery numbers
you can run this script in place of "rentalrates.py" because it knows to group items that have battery add ons. This script has all of the 
functionality of rental rates but is more organized. Yet to be tested but code looks good. 

Lumberca.py is a script that iterrates through the california lumber links and posts the screenshots onto a pdf

Lumberco.py is a scrip that iterrates through the colorado lumber links and posts the screenshots onto a pdf

Lumberwa.py is a script that iterrates through the washington lumber links and posts the screenshots to a pdf

Rentalpdf.py is the script that takes all screenshots stored in the item number folders and posts them to a pdf. This will later be improved to handle the battery items

Rentalrates.py this is the script that has ran through and taken the rental screenshots. This has a wait time of 10 seconds and stores the screenshots
in a folder in the range its item number. For example, screenshots of '1182' will be stored in the '1100s' folder. The filename for each screenshot
is based on the description and item number, it also includes the vendor from where the screenshot was taken. This also adds a watermark that can 
be customized. The watermark displays the time/date of screenshot and the item description. 

Salespdf.py is the script that pastes the sales screenshots to a pdf. There will be pdf files for each of the categories of sales items. The pdf will be stored in that folder along 
with the screenshots. 

Salesrates.py is the script that mirrors the rentalrates.py script but changes the categories of folders that the screenshots are stored into to mirror the different
categories of sales items. Has the funcitonality of the rental rates script with the watermark and border around the screenshot. 

#IMPORTANT - do not have the script take screenshots and pdfs and then push those up to github. They will be uploaded but it will prevent you from pushing
new changes to github. 
