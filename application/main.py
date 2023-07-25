import customtkinter

from application.ui.elements import Elements
from application.csv.csv_upload import csv_to_database
from application.view.year import calculate_total, create_total
from application.view.graph import create_graph
from application.view.month import create_month, calculate_month
from application.view.table import create_table_headers, create_table_rows
from application.view.navigation import create_element_date, CURRENT_MONTH, create_navigation
from application.database.database_mutations import Database_Mutations
from application.database.database_categories import Database_Categories

# PACKAGES
#######################################
# pyinstaller
# customtkinter

# COMPILE
#######################################
# pyinstaller --onefile --noconsole --icon=favicon.ico main.py

# CATEGORIE
# initialize categories
#######################################

Database_Categories.create_table_if_not_exists()
Database_Categories.create_default_records()

# IMPORT EXCEL
# create database
# add mutations to database
# add initial amount
#######################################

Database_Mutations.create_table_if_not_exists()

# @TODO bedragen deze maand
# @TODO aanklikbare staven
# @TODO navigatie nu, vorige, volgende
# @TODO current selected month
# @TODO overzicht deze maand
# @TODO overzicht categorie deze maand
# @TODO overzicht categorie dit jaar
#######################################

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
  def __init__(self):
    super().__init__()

    # configure window
    #######################################
    self.title("Bookkeeper")
    # self.geometry( f"{1800}x{800}" )
    # self.attributes('-fullscreen', True)

    # configure grid layout (4x4)
    #######################################
    self.grid_columnconfigure((1, 4), weight=3, minsize=400)
    self.grid_columnconfigure((2, 3), weight=1)
    self.grid_rowconfigure((0, 1), weight=1)

    # FRAMES
    #############################
    frame_sidebar = Elements.frame(self, 0, 0, 1, 4, 20, 20)
    frame_sidebar.configure(corner_radius=0)

    frame_total = Elements.frame(self, 1, 0, 1, 1, (0, 20), 20)
    frame_month = Elements.frame(self, 2, 0, 1, 1, (0, 20), 20)

    frame_space = Elements.frame(self, 3, 0, 1, 1, (0, 20), 20)
    frame_space.configure(fg_color="transparent")

    frame_table = Elements.frame(self, 4, 0, 1, 2, (0, 20), 20)
    frame_table_data = Elements.scroll(frame_table, 0, 1, 5, 4, 0, 0)

    frame_graph = Elements.frame(self, 1, 1, 3, 1, (0, 20), (0, 20))

    # ELEMENTS
    #######################################

    # sidebar
    #############################

    # title
    ###################
    Elements.title(frame_sidebar, "Bookkeeper", 0, 0, 20, (20, 10))

    # upload mutations
    #############################
    Elements.button(frame_sidebar, "Upload CSV", csv_to_database, 0, 1, 20, (20, 10))

    # recalculate
    #############################
    def recalculate():
      calculate_bank_total()
      calculate_total()
      calculate_month()
      pass

    Elements.button(frame_sidebar, "refresh", recalculate, 0, 2, 20, (20, 10))

    # add categories to mutations
    #############################
    # sidebar_button_2 = customtkinter.CTkButton( frame_sidebar, text = "add categories",
    #   command = add_categories )
    # sidebar_button_2.grid( row = 2, column = 0, padx = 20, pady = 10 )

    # current saldo
    #############################
    content = "€ " + str(Database_Mutations.sum())
    self.element_bank_total = Elements.header(frame_sidebar, content, 0, 3, 20, (20, 10))

    def calculate_bank_total():
      self.element_bank_total.configure(text=("€ " + str(Database_Mutations.sum())))

    # current month
    #############################
    create_element_date(frame_sidebar)
    create_navigation(frame_sidebar)

    # amounts
    #######################################

    # totals
    #############################
    create_total(frame_total)

    # this month
    #############################
    create_month(frame_month)

    # create table
    #######################################
    create_table_headers(frame_table)
    create_table_rows(frame_table_data)

    # graphs
    #######################################

    create_graph(frame_graph)

    # recalculate
    #######################################
    recalculate()


if __name__ == '__main__':
  app = App()
  app.mainloop()
