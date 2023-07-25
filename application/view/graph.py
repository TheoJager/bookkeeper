from customtkinter import CTkFrame
from application.constants import W20
from application.ui.elements import Elements
from application.database.database_categories import Database_Categories

# GLOBALS
#######################################

ELEMENT_GRAPH = {}

# FUNCTIONS
#######################################

def create_graph_header(append: CTkFrame, column: int, name: str):
  header = Elements.header(append, name, column, 0, (2, 0), W20)
  header.grid(columnspan=12)


def create_graph_bars(append: CTkFrame, column: int, i: int):
  progressbar = Elements.progressbar(append, column, 1, (1, 0), 20)
  progressbar.set(i / 12)


def create_graph(append: CTkFrame):
  column = 0

  spacer = Elements.label(append, " ", column, 1, W20, W20)
  spacer.grid(rowspan=2)

  column += 1

  for category in Database_Categories.select():
    create_graph_header(append, column, category["ctr_name"])
    column += 1
    for i in range(12):
      create_graph_bars(append, column, i)
      column += 1
