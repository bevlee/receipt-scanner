import pytesseract
from PIL import Image
import sys
import re
import products


#use member_number as starting point for costco receipt
f = open("member_number", "r")
MEMBER_NUMBER = f.read()
f.close()

START_STRING = MEMBER_NUMBER
# PATH to tesseract executable
TESSERACT_PATH = r"D:\\tesseract\\tesseract"
WHITELIST_LETTERS = "01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,-_/"

# designed for costco receipts
def read_image(string, member_number, filename):
    reading_items = False
    string = string.replace("\n\n", "\n")
    string_list = string.split('\n')
    
    items = [""] * (len(string_list)//2)
    # a bit larger than needed as we ignore first and last few lines
    curr = 0
    i = 0
    print(len(string_list))
    while i < len(string_list):
        
        if "COMMONWEALTH" in string_list[i] or "COMMONWEALTH" in string_list[i-1]:
            reading_items = False
        if reading_items:
            name = string_list[i] 
            product_id, quantity, price = string_list[i+1].split(:3)
                
            items[curr] = string_list[i] + ", " + string_list[i+1].replace(" ", ",")
            #print(items[curr])
            curr += 1
            i += 1

        if str(member_number) in string_list[i]:
            reading_items = True
        i += 1
    with open("items/" + filename + ".csv", "w") as f:
        for item in items:
            f.write(item+"\n")

if __name__ == "__main__":
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

    # Format receipt output to csv
    if len(sys.argv) == 2:

        f = open("logs/" + sys.argv[1], "r")
        read_image(f.read(), START_STRING, sys.argv[1])
        f.close()

    # Perform OCR on receipt image
    elif len(sys.argv) == 3:
        try:
            if sys.argv[1] == '-p':
                
                pdf = pytesseract.image_to_pdf_or_hocr(sys.argv[2], extension='pdf')
                with open('test.pdf', 'w+b') as f:
                    f.write(pdf) # pdf type is bytes by default

            elif sys.argv[1] == '-t':
                out = pytesseract.image_to_string(Image.open(sys.argv[2]), lang='eng')
                print(out)

                with open("logs/" + re.split('[./]',sys.argv[2])[-2], "w") as f:
                    f.write(out)
        except:
            print("exception")
    
        
    