import pytesseract
from PIL import Image
import sys

f = open("member_number", "r")

MEMBER_NUMBER = f.read()
f.close()

print(MEMBER_NUMBER)


# def read_image(string, member_number):
#     read = False
#     for line in string.split("\n\n"):
        
        
#         if read:
#             print(line)
#         if str(member_number) in line:
#             read = True
#         if "COMMONWEALTH" in line:
#             read = False

# if __name__ == "__main__":
#     pytesseract.pytesseract.tesseract_cmd = r"D:\\tesseract\\tesseract"

#     if len(sys.argv) == 2:

#         f = open("r1", "r")
#         read_image(f.read(), MEMBER_NUMBER)
#     elif len(sys.argv) == 3:
#         print(sys.argv)
#     else:
        
#     # out = pytesseract.image_to_string(Image.open('r1.jpg'), lang='eng')
#     # f = open("r1", "x")
#     # f.write(out)
#     # print(out)
#     # f.close()