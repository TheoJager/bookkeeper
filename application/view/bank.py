from customtkinter import CTkFrame, CTkLabel
from application.constants import W20
from application.ui.elements import Elements
from application.database.database_mutations import Database_Mutations

# GLOBALS
#######################################

ELEMENT_BANK_TOTAL: CTkLabel


# FUNCTIONS
#######################################

def create_bank_total(append: CTkFrame, column: int = 0, row: int = 0):
  global ELEMENT_BANK_TOTAL

  ELEMENT_BANK_TOTAL = Elements.header(append, "€ 0.00", column, row, W20, W20)


def update_bank_total():
  global ELEMENT_BANK_TOTAL

  ELEMENT_BANK_TOTAL.configure(text=("€ " + '%.2f' % Database_Mutations.sum()))
