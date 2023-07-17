import glob
from tkinter import *

root = Tk()
root.title( 'bookkeeper' )
root.iconbitmap( 'D:/python/bookkeeper/favicon.ico' )
root.geometry( '1000x600' )

# pyinstaller --onefile --noconsole --icon=favicon.ico main.py


def get( dictionary, key, default = None ):
    return dictionary[ key ] if key in dictionary.keys() else default


# IMPORT EXCEL
# basis bedrag
# toevoegen records
# check dubbel
# toevoegen aan categorie (ai)
#######################################

# LABEL
# deze maand
# bedrag op rekening
#######################################

# CATEGORIE
# bedragen deze maand
#######################################

# CATEGORIE
# bedragen alle maanden
# aanklikbare staven
#######################################

# MAANDEN
# navigatie nu, vorige, volgende
#######################################

# OVERZICHT
# deze maand
# per categorie deze maand
#######################################



if __name__ == '__main__':
    root.mainloop()
