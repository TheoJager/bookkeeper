import locale
import customtkinter
import application.globals as glb

from application.constants import W20
from application.database.database_search import Database_Search
from application.date.today import Today
from application.screen.categorize import Categorize
from application.ui.elements import Elements
from application.csv.csv_upload import csv_to_database
from application.view.view import View
from application.view.view_bank import View_Bank
from application.view.view_date import View_Date
from application.view.view_year import View_Year
from application.view.view_graph import View_Graph
from application.view.view_month import View_Month
from application.view.view_table import View_Table
from application.view.view_navigation import Navigation
from application.database.database_mutations import Database_Mutations
from application.database.database_categories import Database_Categories

# PACKAGES
#######################################
# pyinstaller
# customtkinter

# COMPILE
#######################################
# pyinstaller --onefile --noconsole --icon=favicon.ico main.py

# DATABASE SETUP
#######################################

Database_Categories.create_table_if_not_exists()
Database_Categories.create_default_records()

Database_Mutations.create_table_if_not_exists()

Database_Search.create_table_if_not_exists()

# SETTINGS
#######################################

locale.setlocale( locale.LC_TIME, "nl_NL" )

customtkinter.set_appearance_mode( "System" )  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme( "green" )  # Themes: "blue" (standard), "green", "dark-blue"

glb.SELECTED_MONTH = Today.month()

class Bookkeeper( customtkinter.CTk ):
  def __init__( self ):
    super().__init__()

    # configure window
    #######################################

    self.title( "Bookkeeper" )
    # self.attributes('-fullscreen', True)

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
    self.grid_columnconfigure( 1, weight = 1, minsize = 500 )  # amount year
    self.grid_columnconfigure( 2, weight = 1, minsize = 350 )  # amount month
    self.grid_columnconfigure( 3, weight = 1, minsize = 450 )  # table
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

    Elements.title( frame_sidebar, "Bookkeeper", 0, 0, (10, 0), W20 )

    Elements.button( frame_sidebar, "Upload CSV", csv_to_database, 0, 1, 20 )

    View_Date.create( frame_sidebar, 0, 3 )

    Navigation.create( frame_sidebar, 0, 4 )

    View_Bank.create( frame_sidebar, 0, 5 )

    def open_categorize():
      Categorize().mainloop()

    Elements.button( frame_sidebar, "Categorize", open_categorize, 0, 6, 20 )

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

    View.initiate()
    View.update( glb.SELECTED_MONTH )


if __name__ == '__main__':
  Bookkeeper().mainloop()
