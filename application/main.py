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


# RECALCULATE
#############################

def recalculate():
  Navigation.update()
  View_Bank.update()
  View_Year.update()
  View_Month.update()
  View_Graph.update()


class Bookkeeper( customtkinter.CTk ):
  def __init__( self ):
    super().__init__()

    # configure window
    #######################################

    self.title( "Bookkeeper" )
    # self.attributes('-fullscreen', True)

    w = 1600  # width for the Tk root
    h = 800  # height for the Tk root

    # get screen width and height
    ws = self.winfo_screenwidth()  # width of the screen
    hs = self.winfo_screenheight()  # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws - w) / 2
    y = (hs - h) / 4

    # set the dimensions of the screen
    # and where it is placed
    self.geometry( '%dx%d+%d+%d' % (w, h, x, y) )

    # configure grid layout (4x4)
    #######################################

    self.grid_columnconfigure( 0, weight = 1, minsize = 225 )  # sidebar
    self.grid_columnconfigure( 1, weight = 2, minsize = 575 )  # amount year
    self.grid_columnconfigure( 2, weight = 1, minsize = 400 )  # amount month
    self.grid_columnconfigure( 3, weight = 1, minsize = 400 )  # table
    self.grid_rowconfigure( (0, 1), weight = 1 )

    # FRAMES
    #############################

    frame_sidebar = Elements.frame( self, 0, 0, 1, 4, W20, 20 )

    frame_total = Elements.frame( self, 1, 0, 1, 1, W20, W20 )
    frame_month = Elements.frame( self, 2, 0, 1, 1, W20, W20 )
    frame_table = Elements.frame( self, 3, 0, 1, 2, 20, 20 )
    frame_graph = Elements.frame( self, 1, 1, 2, 1, W20, 20 )

    # ELEMENTS
    #######################################

    # sidebar
    #############################

    # title
    ###################

    Elements.title( frame_sidebar, "Bookkeeper", 0, 0, W20, W20 )

    # upload mutations
    #############################

    Elements.button( frame_sidebar, "Upload CSV", csv_to_database, 0, 1, 20, W20 )
    Elements.button( frame_sidebar, "Refresh", recalculate, 0, 2, 20, W20 )

    # current month
    # month navigation
    #############################

    Navigation.create_element_date( frame_sidebar, 0, 3 )
    Navigation.create_navigation( frame_sidebar, 0, 4 )

    # current bank total
    #############################

    View_Bank.create( frame_sidebar, 0, 5 )

    # amounts
    #######################################

    # totals
    #############################

    View_Year.create( frame_total )

    # this month
    #############################

    View_Month.create( frame_month )

    # create table
    #######################################

    View_Table.create_headers( frame_table )

    # graphs
    #######################################

    View_Graph.create( frame_graph )

    # recalculate
    #######################################

    recalculate()


if __name__ == '__main__':
  Bookkeeper().mainloop()
