import pytesseract
from PIL import Image
import sys
import re
import psycopg

#use member_number as starting point for costco receipt
f = open("member_number", "r")
MEMBER_NUMBER = f.read()
f.close()

f = open("db_password", "r")
DB_PASSWORD = f.read()
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

    # each item is spread over 2 lines
    items = [""] * (len(string_list)//2)

    with psycopg.connect("dbname=costco user=postgres password={}".format(DB_PASSWORD)) as conn:

        # Open a cursor to perform database operations
        with conn.cursor() as cur:

            # Query the database and obtain data as Python objects.
            cur.execute("SELECT * FROM product")
            cur.fetchone()
            # will return (1, 100, "abc'def")

            # You can use `cur.fetchmany()`, `cur.fetchall()` to return a list
            # of several records, or even iterate on the cursor
            for record in cur:
                print(record)

            # a bit larger than needed as we ignore first and last few lines
            curr = 0
            i = 0
            print(len(string_list))
            while i < len(string_list):

                #stop reading items as there are none after this
                if "COMMONWEALTH" in string_list[i] or "COMMONWEALTH" in string_list[i-1]:
                    reading_items = False
                if reading_items:
                    name = string_list[i]
                    product_id, quantity, price = string_list[i+1].replace(" ", ",").split(",")[:3]

                    try:
                        price = float(price)
                    except ValueError:
                        price = 1.99
                    cur.execute("""
                        INSERT INTO Product 
                        (product_id, product_name, price)
                        SELECT %s, %s, %s
                        WHERE NOT EXISTS (SELECT product_id FROM Product WHERE product_id = %s);
                        
                        """, (int(product_id), name, price, int(product_id))
                    )
                    items[curr] = string_list[i] + ", " + string_list[i+1].replace(" ", ",")
                    print(items[curr])
                    curr += 1
                    i += 1

                #start reading items as they appear after the member number
                if str(member_number) in string_list[i]:
                    reading_items = True

                i += 1
            

            # Make the changes to the database persistent
            conn.commit()
    
    
    
    with open("items/" + filename + ".csv", "w") as f:
        f.write("name, id, count, cost\n")
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
            # to pdf
            if sys.argv[1] == '-p':
                
                pdf = pytesseract.image_to_pdf_or_hocr(sys.argv[2], extension='pdf')
                with open('test.pdf', 'w+b') as f:
                    f.write(pdf) # pdf type is bytes by default

            # to csv
            elif sys.argv[1] == '-t':
                out = pytesseract.image_to_string(Image.open(sys.argv[2]), lang='eng')
                print(out)

                with open("logs/" + re.split('[./]',sys.argv[2])[-2], "w") as f:
                    f.write(out)
        except Exception as e:
            print(e)
    
        
    