import locale
import datetime
import sqlite3
import customtkinter

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

# CATEGORIE
# initialize categories
#######################################

Database_Categories.create_table_if_not_exists()

cat_records = [
  {'ctr_income': 0, 'ctr_sequence': 1, 'ctr_name': 'Incidenteel'},
  {'ctr_income': 0, 'ctr_sequence': 2, 'ctr_name': 'Eten'},
  {'ctr_income': 0, 'ctr_sequence': 3, 'ctr_name': 'Boodschappen'},
  {'ctr_income': 0, 'ctr_sequence': 4, 'ctr_name': 'Abonnementen'},
  {'ctr_income': 0, 'ctr_sequence': 5, 'ctr_name': 'Kosten'},
  {'ctr_income': 0, 'ctr_sequence': 6, 'ctr_name': 'Sparen'},
  {'ctr_income': 0, 'ctr_sequence': 7, 'ctr_name': 'Beleggingen'},
  {'ctr_income': 1, 'ctr_sequence': 8, 'ctr_name': 'Salaris'},
]
for cat_record in cat_records:
  try:
    Database_Categories.insert(cat_record)
  except sqlite3.IntegrityError:
    break

# IMPORT EXCEL
# create database
# add mutations to database
# add initial amount
#######################################

Database_Mutations.create_table_if_not_exists()


def insert_base_value(record: list):
  if len(Database_Mutations.select()) == 0:
    Database_Mutations.insert({
      'mts_date': "19700101",
      'mts_amount': record['mts_start'],
      'mts_description': 'start',
      'mts_category': 8,
    })


def csv_to_database():
  records = csv_to_records(csv_get_filename())
  insert_base_value(records[0])
  for record in records:
    try:
      Database_Mutations.insert(record)
    except sqlite3.IntegrityError:
      continue


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

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
  def __init__(self):
    super().__init__()

    # configure window
    #######################################
    self.title("Bookkeeper")
    self.geometry(f"{1200}x{580}")

    # configure grid layout (4x4)
    #######################################
    self.grid_columnconfigure(1, weight=1)
    self.grid_columnconfigure((2, 3), weight=0)
    self.grid_rowconfigure((0, 1, 2), weight=1)

    # create left sidebar
    #######################################
    sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
    sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
    sidebar_frame.grid_rowconfigure(4, weight=1)

    # title
    #############################
    font = customtkinter.CTkFont(size=20, weight="bold")
    title_label = customtkinter.CTkLabel(sidebar_frame, text="Bookkeeper", font=font)
    title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

    # upload mutations
    #############################
    sidebar_button_1 = customtkinter.CTkButton(sidebar_frame, text="Upload CSV File", command=csv_to_database)
    sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

    # add categories to mutations
    #############################
    sidebar_button_2 = customtkinter.CTkButton(sidebar_frame, text="add categories", command=add_categories)
    sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

    # current month
    #############################
    x = datetime.datetime.now()

    locale.setlocale(locale.LC_TIME, "nl_NL")

    font = customtkinter.CTkFont(size=16, weight="bold")
    month_label = customtkinter.CTkLabel(sidebar_frame, text=x.strftime("%B %Y"), font=font)
    month_label.grid(row=6, column=0, padx=20, pady=(20, 10))

    # current saldo
    #############################
    content = "€ " + str(Database_Mutations.sum())

    font = customtkinter.CTkFont(size=16, weight="bold")
    month_label = customtkinter.CTkLabel(sidebar_frame, text=content, font=font)
    month_label.grid(row=5, column=0, padx=20, pady=(20, 10))

    # create categorie data
    #######################################
    categorie_frame = customtkinter.CTkFrame(self, fg_color="transparent")
    categorie_frame.grid( row = 0, column = 1, padx = (20, 20), pady = (5, 5), sticky = "nsew" )

    main_button_1 = customtkinter.CTkButton( categorie_frame, text="incidenteel", fg_color = "transparent",
      border_width = 1, text_color = ("gray10", "#DCE4EE"), command=add_categories )
    main_button_1.grid( row = 1, column = 1, padx = (5, 5), pady = (20, 20),
      sticky = "nsew" )

    main_button_1 = customtkinter.CTkButton( categorie_frame, text="€-1562.75", fg_color = "transparent",
      border_width = 1, text_color = ("gray10", "#DCE4EE"), command=add_categories )
    main_button_1.grid( row = 1, column = 2, padx = (5, 5), pady = (20, 20),
      sticky = "nsew" )

    main_button_1 = customtkinter.CTkButton( categorie_frame, text="-10.8%", fg_color = "transparent",
      border_width = 1, text_color = ("gray10", "#DCE4EE"), command=add_categories )
    main_button_1.grid( row = 1, column = 3, padx = (5, 5), pady = (20, 20),      sticky = "nsew" )

    main_button_1 = customtkinter.CTkButton( categorie_frame, text="€-65.25", fg_color = "transparent",
      border_width = 1, text_color = ("gray10", "#DCE4EE"), command=add_categories )
    main_button_1.grid( row = 1, column = 5, padx = (5, 5), pady = (20, 20),
      sticky = "nsew" )

    main_button_1 = customtkinter.CTkButton( categorie_frame, text="-5.4%", fg_color = "transparent",
      border_width = 1, text_color = ("gray10", "#DCE4EE"), command=add_categories )
    main_button_1.grid( row = 1, column = 6, padx = (5, 5), pady = (20, 20), sticky = "nsew" )


    # create table
    #######################################
    categorie_table = customtkinter.CTkFrame(self, fg_color="transparent")
    categorie_table.grid( row = 0, column = 2, padx = (20, 20), pady = (20, 0), sticky = "nsew" )


if __name__ == '__main__':
  app = App()
  app.mainloop()
