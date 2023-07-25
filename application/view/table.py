from customtkinter import CTkFrame
from application.constants import W20
from application.ui.elements import Elements

# GLOBALS
#######################################

ELEMENT_TABLES = {}


# FUNCTIONS
#######################################

def create_table_headers(append: CTkFrame):
  Elements.header(append, "date", 0, 0, W20, W20)
  Elements.header(append, "product", 1, 0, W20, W20)
  Elements.header(append, "category", 2, 0, W20, W20)
  Elements.header(append, "amount", 3, 0, (20, 20), W20)


def create_table_rows(append: CTkFrame):
  Elements.label(append, "20221124", 0, 1, W20, W20)
  Elements.label(append, "triplepro", 1, 1, W20, W20)
  Elements.label(append, "salaris", 2, 1, W20, W20)
  Elements.label(append, "2028.93", 3, 1, W20, W20)
