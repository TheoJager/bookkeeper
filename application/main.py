import locale
import datetime
import sqlite3

import customtkinter

from application.message.message import Message
from application.ui.elements import Elements
from application.csv.csv_upload import csv_get_filename, csv_to_records
from application.database.database_mutations import Database_Mutations
from application.database.database_categories import Database_Categories

# PACKAGES
#######################################
# pyinstaller
# customtkinter

# COMPILE
#######################################
# pyinstaller --onefile --noconsole --icon=favicon.ico main.py

# CONSTANTS
#######################################

W20 = (20, 0)
CATEGORY_INCOME = 8

# CATEGORIE
# initialize categories
#######################################

Database_Categories.create_table_if_not_exists()

cat_records = [
  { 'ctr_income': 0, 'ctr_sequence': 1, 'ctr_name': 'Incidenteel' },
  { 'ctr_income': 0, 'ctr_sequence': 2, 'ctr_name': 'Eten' },
  { 'ctr_income': 0, 'ctr_sequence': 3, 'ctr_name': 'Boodschappen' },
  { 'ctr_income': 0, 'ctr_sequence': 4, 'ctr_name': 'Abonnementen' },
  { 'ctr_income': 0, 'ctr_sequence': 5, 'ctr_name': 'Kosten' },
  { 'ctr_income': 0, 'ctr_sequence': 6, 'ctr_name': 'Sparen' },
  { 'ctr_income': 0, 'ctr_sequence': 7, 'ctr_name': 'Beleggingen' },
  { 'ctr_income': 1, 'ctr_sequence': 8, 'ctr_name': 'Salaris' },
]
for cat_record in cat_records:
  try:
    Database_Categories.insert( cat_record )
  except sqlite3.IntegrityError:
    break

# IMPORT EXCEL
# create database
# add mutations to database
# add initial amount
#######################################

Database_Mutations.create_table_if_not_exists()


def insert_base_value( record: list ):
  if len( Database_Mutations.select() ) == 0:
    Database_Mutations.insert( {
      'mts_date'       : "19700101",
      'mts_amount'     : record[ 'mts_start' ],
      'mts_start'      : 0,
      'mts_description': 'start',
      'mts_category'   : 8,
    } )


def csv_to_database():
  filename = csv_get_filename()
  if (len( filename )):
    records = csv_to_records( filename )
    insert_base_value( records[ 0 ] )
    for record in records:
      try:
        Database_Mutations.insert( record )
      except sqlite3.IntegrityError:
        continue
    Message.ok( 'result', 'import successful' )


# MUTATIONS
# add categories (ai) to mutations
#######################################
def add_categories():
  pass


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

# BOOKKEEPER
# current selected month
# total amount on account
#######################################

customtkinter.set_appearance_mode( "System" )  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme( "green" )  # Themes: "blue" (standard), "green", "dark-blue"


class App( customtkinter.CTk ):
  def __init__( self ):
    super().__init__()

    # configure window
    #######################################
    self.title( "Bookkeeper" )
    # self.geometry( f"{1800}x{800}" )
    # self.attributes('-fullscreen', True)

    # configure grid layout (4x4)
    #######################################
    self.grid_columnconfigure( (1, 4), weight = 3, minsize = 400 )
    self.grid_columnconfigure( (2, 3), weight = 1 )
    self.grid_rowconfigure( (0, 1), weight = 1 )

    # FRAMES
    #############################
    frame_sidebar = Elements.frame( self, 0, 0, 1, 4, 20, 20 )
    frame_sidebar.configure( corner_radius = 0 )

    frame_total = Elements.frame( self, 1, 0, 1, 1, (0, 20), 20 )
    frame_month = Elements.frame( self, 2, 0, 1, 1, (0, 20), 20 )

    frame_space = Elements.frame( self, 3, 0, 1, 1, (0, 20), 20 )
    frame_space.configure( fg_color = "transparent" )

    frame_table = Elements.frame( self, 4, 0, 1, 2, (0, 20), 20 )
    frame_table_data = Elements.scroll( frame_table, 0, 1, 5, 4, 0, 0 )

    frame_graph = Elements.frame( self, 1, 1, 3, 1, (0, 20), (0, 20) )

    # ELEMENTS
    #######################################

    # sidebar
    #############################

    # title
    ###################
    Elements.title( frame_sidebar, "Bookkeeper", 0, 0, 20, (20, 10) )

    # upload mutations
    #############################
    Elements.button( frame_sidebar, "Upload CSV", csv_to_database, 0, 1, 20, (20, 10) )

    # recalculate
    #############################
    def recalculate():
      calculate_bank_total()
      calculate_total()
      calculate_month()
      pass

    Elements.button( frame_sidebar, "refresh", recalculate, 0, 2, 20, (20, 10) )

    # add categories to mutations
    #############################
    # sidebar_button_2 = customtkinter.CTkButton( frame_sidebar, text = "add categories",
    #   command = add_categories )
    # sidebar_button_2.grid( row = 2, column = 0, padx = 20, pady = 10 )

    # current saldo
    #############################
    content = "€ " + str( Database_Mutations.sum() )
    self.element_bank_total = Elements.header( frame_sidebar, content, 0, 3, 20, (20, 10) )

    def calculate_bank_total():
      self.element_bank_total.configure( text = ("€ " + str( Database_Mutations.sum() )) )

    # current month
    #############################
    locale.setlocale( locale.LC_TIME, "nl_NL" )

    x = datetime.datetime.now()
    content = x.strftime( "%B %Y" )
    Elements.header( frame_sidebar, content, 0, 4, 20, (20, 10) )

    # amounts
    #######################################

    # totals
    #############################
    self.element_total = { }

    row = 0
    categories = Database_Categories.select()
    for category in categories:
      Elements.button_inverse( frame_total, category[ "ctr_name" ], add_categories, 0, row, W20, W20 ).configure( anchor = "w" )
      s = Elements.button_inverse( frame_total, "€ 0.00", add_categories, 1, row, W20, W20 )
      p = Elements.button_inverse( frame_total, "0.00 %", add_categories, 2, row, W20, W20 )

      s.configure( anchor = "w" )
      p.configure( width = 100 )

      self.element_total[ category[ "ctr_name" ] ] = [ s, p ]
      row += 1

    Elements.label( frame_total, "", 0, row + 1, W20, W20 )

    def calculate_total():
      sum_income_year = Database_Mutations.sum_category_year( CATEGORY_INCOME )

      categories = Database_Categories.select()
      for category in categories:
        sum_category = Database_Mutations.sum_category_year( category[ "ctr_id" ] )
        percent_category = "0.00" if sum_income_year == 0 else str( round( (sum_category / sum_income_year) * 100, 1 ) )

        s, p = self.element_total[ category[ "ctr_name" ] ]
        s.configure( text = "€ " + str( sum_category ) )
        p.configure( text = str( percent_category ) + " %" )


    # this month
    #############################
    self.element_month = { }

    row = 0
    for category in categories:
      s = Elements.button_inverse( frame_month, "€ 0.00", add_categories, 1, row, W20, W20 )
      p = Elements.button_inverse( frame_month, "0.00 %", add_categories, 2, row, (20, 20), W20 )

      s.configure( anchor = "w" )
      p.configure( width = 100 )

      self.element_month[ category[ "ctr_name" ] ] = [ s, p ]
      row += 1

    def calculate_month():
      sum_income_month = Database_Mutations.sum_category_month( CATEGORY_INCOME )

      for category in categories:
        sum_category_month = Database_Mutations.sum_category_month( category[ "ctr_id" ] )
        percent_category = "0.00" if sum_income_month == 0 else str( round( (sum_category_month / sum_income_month) * 100, 1 ) )

        s, p = self.element_month[ category[ "ctr_name" ] ]
        s.configure( text = "€ " + str( sum_category_month ) )
        p.configure( text = str( percent_category ) + " %" )

    # create table
    #######################################
    Elements.header( frame_table, "date", 0, 0, W20, W20 )
    Elements.header( frame_table, "product", 1, 0, W20, W20 )
    Elements.header( frame_table, "category", 2, 0, W20, W20 )
    Elements.header( frame_table, "amount", 3, 0, (20, 20), W20 )

    Elements.label( frame_table_data, "20221124", 0, 1, W20, W20 )
    Elements.label( frame_table_data, "triplepro", 1, 1, W20, W20 )
    Elements.label( frame_table_data, "salaris", 2, 1, W20, W20 )
    Elements.label( frame_table_data, "2028.93", 3, 1, W20, W20 )

    # graphs
    #######################################

    column = 0
    for j in range( 8 ):
      spacer = Elements.label( frame_graph, " ", column, 1, W20, W20 )
      spacer.grid( rowspan = 2 )

      header = Elements.header( frame_graph, "incidenteel", column + 1, 0, (2, 0), W20 )
      header.grid( columnspan = 12 )

      column += 1
      for i in range( 12 ):
        progressbar = customtkinter.CTkProgressBar( frame_graph, orientation = "vertical" )
        progressbar.grid( column = column, row = 1, padx = (1, 0), pady = 20, sticky = "ns" )
        progressbar.set( i / 12 )
        column += 1

    # recalculate
    #######################################
    recalculate()


if __name__ == '__main__':
  app = App()
  app.mainloop()
