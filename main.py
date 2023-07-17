import glob
from tkinter import *

from PIL import ImageTk, Image

root = Tk()
root.title( 'title of the application' )
root.iconbitmap( 'D:/python/bookkeeper/favicon.ico' )
root.geometry( '400x400' )

# root.overrideredirect(1)

images = glob.glob( "D:/python/bookkeeper/images/*.jpg" )

index = 0
max = len( images ) - 1


def get( dictionary, key, default = None ):
    return dictionary[ key ] if key in dictionary.keys() else default


def open_image( path ):
    height = 300
    img = Image.open( path )
    image_width, image_height = img.size
    scaler = image_height / height
    width = int( image_width / scaler )

    img = img.resize( (width, height) )

    return ImageTk.PhotoImage( img )


def image_previous():
    global index
    index = max if index == 0 else index - 1

    status.configure( text = 'image ' + str( index + 1 ) + ' of ' + str( max + 1 ) )

    img = open_image( images[ index ] )
    image_container.configure( image = img )
    image_container.image = img


def image_next():
    global index
    index = 0 if index == max else index + 1

    status.configure( text = 'image ' + str( index + 1 ) + ' of ' + str( max + 1 ) )

    img = open_image( images[ index ] )
    image_container.configure( image = img )
    image_container.image = img


image = open_image( images[ 0 ] )

image_container = Label( image = image )
image_container.grid( row = 0, column = 0, columnspan = 3, sticky = 'nsew' )

status = Label( text = 'image 1 of ' + str( max + 1 ), height = 2, anchor = E, padx = 15 )
status.grid( row = 2, column = 0, columnspan = 3,
    sticky = 'nsew' )

buttons = {
    '<<'  : { 'row': 1, 'column': 0, 'onclick': image_previous },
    '>>'  : { 'row': 1, 'column': 2, 'onclick': image_next },
    'exit': { 'row': 1, 'column': 1, 'onclick': root.quit },
}

for label, button in buttons.items():
    b = Button( root, text = label, font = ('Arial', 10),
        width = get( button, 'width', 10 ), height = 3,
        bg = '#565656', fg = '#CDCDCD', borderwidth = 1,
        command = get( button, 'onclick' ) )

    b.grid( row = button[ 'row' ],
        column = button[ 'column' ],
        columnspan = get( button, 'columnspan', 1 ),
        sticky = 'nsew' )

if __name__ == '__main__':
    root.mainloop()
