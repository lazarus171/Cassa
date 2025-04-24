# import Code128 from barcode module 
from barcode import Code128 

# import ImageWriter to generate an image file 
from barcode.writer import ImageWriter 

# Make sure to pass the number as string 
number = 'A1234'

# Now, let's create an object of Code128 class and 
# pass the number with the ImageWriter() as the 
# writer 
my_code = Code128(number, writer=ImageWriter()) 

# Our barcode is ready. Let's save it. 
my_code.save("new_code1")
