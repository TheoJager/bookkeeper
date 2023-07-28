import customtkinter

from application.constants import W20
from application.ui.elements import Elements
from application.csv.csv_upload import csv_to_database
from application.view.bank import View_Bank
from application.view.year import View_Year
from application.view.graph import View_Graph
from application.view.month import View_Month
from application.view.table import View_Table
from application.view.navigation import Navigation
from application.view.functions import view_update
from application.database.database_mutations import Database_Mutations
from application.database.database_categories import Database_Categories

# PACKAGES
#######################################
# pyinstaller
# customtkinter

# COMPILE
#######################################
# pyinstaller --onefile --noconsole --icon=favicon.ico main.py

# @TODO bedragen deze maand
# @TODO aanklikbare staven
# @TODO overzicht deze maand
# @TODO overzicht categorie dit jaar
#######################################

# DATABASE SETUP
#######################################

Database_Categories.create_table_if_not_exists()
Database_Categories.create_default_records()

Database_Mutations.create_table_if_not_exists()

# SETTINGS
#######################################

customtkinter.set_appearance_mode( "System" )  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme( "green" )  # Themes: "blue" (standard), "green", "dark-blue"


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

    Navigation.create_element_date( frame_sidebar, 0, 3 )
    Navigation.create_navigation( frame_sidebar, 0, 4 )

    View_Bank.create( frame_sidebar, 0, 5 )

    # amounts
    #############################

    View_Year.create( frame_total )

    View_Month.create( frame_month )

    # table
    #######################################

    View_Table.create( frame_table, Navigation.MONTH )

    # graphs
    #######################################

    View_Graph.create( frame_graph )

    # update
    #######################################

    view_update()


if __name__ == '__main__':
  Bookkeeper().mainloop()
