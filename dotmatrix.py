# Q.1 "Sea Marks: Dotmatrix"
# Import "Image" module from "Python Image Library"
from PIL import Image
import sys
 
def newCircle(img,p,q):
    # Run a loop which traverses on a square of a side which is equal to diameter of the circle
    for i in range(p-25,p+26):
        for j in range(q-25,q+26):
            # This statement applies the constraint of the circle [(x-p)^2 + (y-q)^2 <= R^2]
            if (i-p)**2+(j-q)**2 <=625 : img.putpixel((j,i),(255,255,255))
    # Return "img" back to the add_digit function        
    return img
 
 
def add_digit(img,digit,k):
    # Run a loop which adds all the circles of the digit on the image
    for t in digit:
        # This function takes "img" and pixel position of center of a circle
        img=newCircle(img,25+10+57*t[0],k+25+50+57*t[1])
    # Return "img" back to the create_Img function
    return img
 
 
def create_Img(data,dsn):
    # Create a new image of size = 500X300 and type = "RGB", color is black by default
    img = Image.new('RGB', (500, 300))
 
    # Run a loop for each digit of dsn
    for i in range(len(dsn)):
        # Add a digit via calling add_digit on image "img"
        # First element is "img" itself
        # Second element passes the data for ith digit(0 to 9)
        # Third element is to maintain the space between two digits of the dsn
        img = add_digit(img,data[int(dsn[i])],i*225)
 
    # Save the image in the directory
    return img
 
######################################## Program starts here ##############################################
 
# First of all, Create database
# Each tuple of tuple has the information that where should be a circle in the 5X3 grid for a digit (0 to 9)
d0 = ((0,0),(0,1),(0,2),(1,0),(1,2),(2,0),(2,2),(3,0),(3,2),(4,0),(4,1),(4,2))
d1 = ((0,2),(1,2),(2,2),(3,2),(4,2))
d2 = ((0,0),(0,1),(0,2),(1,2),(2,0),(2,1),(2,2),(3,0),(4,0),(4,1),(4,2))
d3 = ((0,0),(0,1),(0,2),(1,2),(2,0),(2,1),(2,2),(3,2),(4,0),(4,1),(4,2))
d4 = ((0,0),(0,2),(1,0),(1,2),(2,0),(2,1),(2,2),(3,2),(4,2))
d5 = ((0,0),(0,1),(0,2),(1,0),(2,0),(2,1),(2,2),(3,2),(4,0),(4,1),(4,2))
d6 = ((0,0),(0,1),(0,2),(1,0),(2,0),(2,1),(2,2),(3,0),(3,2),(4,0),(4,1),(4,2))
d7 = ((0,0),(0,1),(0,2),(1,2),(2,2),(3,2),(4,2))
d8 = ((0,0),(0,1),(0,2),(1,0),(1,2),(2,0),(2,1),(2,2),(3,0),(3,2),(4,0),(4,1),(4,2))
d9 = ((0,0),(0,1),(0,2),(1,0),(1,2),(2,0),(2,1),(2,2),(3,2),(4,0),(4,1),(4,2))
 
# Store all the tuples of digit in another tuble
data = (d0,d1,d2,d3,d4,d5,d6,d7,d8,d9)
 
# Taking "Docking Station Number" in "dsn" as an input
dsn = sys.argv[1]
 
# Call a function to create and save the image
display = create_Img(data,dsn)
display.save('dotmatrix.jpg')