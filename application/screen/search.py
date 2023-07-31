import customtkinter

from application.constants import W20
from application.ui.elements import Elements

customtkinter.set_appearance_mode( "System" )  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme( "green" )  # Themes: "blue" (standard), "green", "dark-blue"

class Search( customtkinter.CTk ):
  def __init__( self ):
    super().__init__()

    # configure window
    #######################################

    self.title( "Search" )

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

    frame_headers = Elements.frame( self, 1, 0, 1, 1, 20, W20 )
    frame_records = Elements.scroll( self, 1, 1, 1, 1, 20, 20 )

    frame_headers.configure( width = 500, height = 50 )

    # ELEMENTS
    #######################################

    # headers
    #############################


    # records
    #############################



if __name__ == '__main__':
  Search().mainloop()
