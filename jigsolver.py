#Importing "Image" Module from "PIL"
from PIL import Image
import sys
#Assign the jigsaw.jpg to img
img = Image.open(str(sys.argv[1]))
# img = Image.open('jigsaw.jpg')

# Dimensions of Image
width = img.width
height = img.height
# print(width,height)

#Below commented code snippet is for finding the corner of image segments
#It creates a red square of side 5px
#Oberserving this, one can guess and use hit and trial method to reach a corner

# for i in range(5):
#     for j in range(5):
#         img.putpixel((i+190,200+j),(255))

#Crop a segment which is displaced and place it in correctly
seg1 = img.crop((515,150,700,330))
seg1 = seg1.transpose(method=Image.Transpose.FLIP_LEFT_RIGHT)
img.paste(seg1, box=(515,150,700,330), mask=None)

#Crop another segment which is displaced and place it in correctly
seg2 = img.crop((370,370,797,421))
seg2 = seg2.transpose(method=Image.Transpose.FLIP_TOP_BOTTOM)
img.paste(seg2, box=(370,370,797,421), mask=None)

#Crop pink baby bird to place it at right place
seg3 = img.crop((0,0,190,200))

#Load data of "seg3" in "seg3_data" to proferm some operation to remove its pink color
#It observed manually that 'g' and 'b' value for this segment interchanged. So lets put them their right place
seg3_data = seg3.load()
for i in range(190):
    for j in range(200):
        r,g,b = seg3_data[i,j]
        seg3_data[i,j]=r,b,g

#Crop seg4 before placing seg3 on top it because doing so will overwrite seg4 data
seg4 = img.crop((0,200,190,410))
seg4 = seg4.transpose(method=Image.Transpose.FLIP_TOP_BOTTOM)

#Attach both seg3 and seg4 on their right place
img.paste(seg3, box=(0,200,190,400), mask=None)
img.paste(seg4, box=(0,0,190,210), mask=None)

#Now the only problem remaining is the blue strip at bottem left corner
#Lets solve it by doing mirror padding
#So first load the data of img in a variable
img_data = img.load()

#Width of strip is 10px, It's better to do 5px wide mirror padding from both side
#Mirror padding from upside 
for i in range(0,190):
    for j in range(5):
        img_data[i,400+j] = img_data[i,400-1-j]

#Mirror padding from downside
for i in range(0,190):
    for j in range(5):
        img_data[i,410-1-j] = img_data[i,410+j]
                
#Bingo! Problem solved.Save it in current directory.
img.save('jigsolved.jpg')