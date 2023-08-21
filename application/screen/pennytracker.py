import locale
import customtkinter
import globals as glb

from constants import W20
from date.today import Today
from ui.elements import Elements
from screen.search import Search
from csvfile.csvfile import CSVFile
from view.view_update import View
from view.view_bank import View_Bank
from view.view_date import View_Date
from view.view_year import View_Year
from view.view_graph import View_Graph
from view.view_month import View_Month
from view.view_table import View_Table
from view.view_navigation import Navigation

# SETTINGS
#######################################

customtkinter.set_appearance_mode( "System" )  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme( "green" )  # Themes: "blue" (standard), "green", "dark-blue"

locale.setlocale( locale.LC_TIME, "nl_NL" )

glb.SELECTED_MONTH = Today.month()


class PennyTracker( customtkinter.CTk ):
  def __init__( self ):
    super().__init__()

    # configure window
    #######################################

    self.title( "PennyTracker" )

    w = 1600
    h = 800

    ws = self.winfo_screenwidth()
    hs = self.winfo_screenheight()

    x = (ws - w) / 2
    y = (hs - h) / 4

    self.geometry( '%dx%d+%d+%d' % (w, h, x, y) )

    # configure grid layout (4x4)
    #######################################

    self.grid_columnconfigure( 0, weight = 1, minsize = 200 )  # sidebar
    self.grid_columnconfigure( 1, weight = 1, minsize = 425 )  # amount year
    self.grid_columnconfigure( 2, weight = 1, minsize = 275 )  # amount month
    self.grid_columnconfigure( 3, weight = 1, minsize = 600 )  # table
    self.grid_rowconfigure( (0, 1), weight = 1 )

    # FRAMES
    #############################

    frame_sidebar = Elements.frame( self, 0, 0, 1, 4, W20, 20 )

    frame_total = Elements.frame( self, 1, 0, 1, 1, W20, W20 )
    frame_month = Elements.frame( self, 2, 0, 1, 1, W20, W20 )
    frame_table = Elements.frame( self, 3, 0, 1, 1, 20, W20 )
    frame_graph = Elements.frame( self, 1, 1, 3, 1, 20, 20 )

    # ELEMENTS
    #######################################

    # sidebar
    #############################

    Elements.title( frame_sidebar, "PennyTracker", 0, 0, (10, 0), W20 )

    Elements.button( frame_sidebar, "Upload CSV", CSVFile.to_database, 0, 1, 20 )

    View_Date.create( frame_sidebar, 0, 3 )

    Navigation.create( frame_sidebar, 0, 4 )

    View_Bank.create( frame_sidebar, 0, 5 )

    def open_searches():
      Search().mainloop()

    Elements.button( frame_sidebar, "Searches", open_searches, 0, 6, 20 )

    # amounts
    #############################

    View_Year.create( frame_total )

    View_Month.create( frame_month )

    # table
    #######################################

    View_Table.create( frame_table )

    # graphs
    #######################################

    View_Graph.create( frame_graph )

    # update
    #######################################

    View.update( glb.SELECTED_MONTH )

    # EXIT
    #######################################

    def on_closing():
      glb.SELECTED_MONTH = Today.month()

      View_Date.reset()
      View_Bank.reset()
      View_Year.reset()
      View_Month.reset()
      View_Table.reset()
      View_Graph.reset()
      self.destroy()

    self.protocol( "WM_DELETE_WINDOW", on_closing )


if __name__ == '__main__':
  PennyTracker().mainloop()
