import glob
from tkinter import *
from tkinter import filedialog

from PIL import ImageTk, Image

root = Tk()

images = glob.glob("images/*.jpg")


def open_image(path):
    height = 300
    img = Image.open(path)
    image_width, image_height = img.size
    scaler = image_height / height
    width = int(image_width / scaler)

    img = img.resize((width, height), Image.ANTIALIAS)

    return ImageTk.PhotoImage(img)


def open():
    global label
    root.filename = filedialog.askopenfilename(
        initialdir='images', title='images',
        filetypes=(('jpg files', '*.jpg'), ('all files', '*.*')))

    img = open_image(root.filename)
    label.configure(image=img)
    label.image = img
    return


image = open_image(images[0])
label = Label(image=image)
label.pack()

Button(root, text='open file', command=open).pack()

root.mainloop()
