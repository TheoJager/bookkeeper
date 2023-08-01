import customtkinter

from application.constants import W20
from application.ui.elements import Elements
from application.view.view_search import View_Search

customtkinter.set_appearance_mode( "System" )  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme( "green" )  # Themes: "blue" (standard), "green", "dark-blue"

class Uncategorized( customtkinter.CTk ):
  def __init__( self ):
    super().__init__()

    # configure window
    #######################################

    self.title( "Categorize" )

    w = 1200
    h = 700

    ws = self.winfo_screenwidth()
    hs = self.winfo_screenheight()

    x = (ws - w) / 2
    y = (hs - h) / 4

    self.geometry( '%dx%d+%d+%d' % (w, h, x, y) )

    # configure grid layout (4x4)
    #######################################

    self.grid_columnconfigure( 1, weight = 1, minsize = 1100 )  # headers
    self.grid_rowconfigure( 1, weight = 1 )

    # FRAMES
    #############################

    frame_edit = Elements.frame( self, 1, 0, 1, 1, 20, W20 )
    frame_edit.configure( width = 1000, height = 75 )

    frame_uncategorized_records = Elements.frame( self, 1, 1, 1, 1, 20, 20 )
    frame_uncategorized_records.configure( width = 1000 )

    # ELEMENTS
    #######################################

    View_Search.ELEMENT_PARENT = frame_uncategorized_records
    View_Search.create_form( frame_edit )
    View_Search.create_headers()
    View_Search.create_records()


if __name__ == '__main__':
  Uncategorized().mainloop()
