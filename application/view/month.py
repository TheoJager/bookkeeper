from customtkinter import CTkFrame
from application.ui.elements import Elements
from application.constants import W20, CATEGORY_INCOME
from application.categories.categories import add_categories
from application.database.database_mutations import Database_Mutations
from application.database.database_categories import Database_Categories

# GLOBALS
#######################################

ELEMENT_MONTH = {}


# FUNCTIONS
#######################################

def create_month(append: CTkFrame):
  row = 0
  for category in Database_Categories.select():
    s = Elements.button_inverse(append, "€ 0.00", add_categories, 1, row, W20, W20)
    p = Elements.button_inverse(append, "0.00 %", add_categories, 2, row, (20, 20), W20)

    s.configure(anchor="w")
    p.configure(width=100)

    ELEMENT_MONTH[category["ctr_name"]] = [s, p]
    row += 1


def calculate_month():
  sum_income_month = Database_Mutations.sum_category_month(CATEGORY_INCOME)

  for category in Database_Categories.select():
    sum_category_month = Database_Mutations.sum_category_month(category["ctr_id"])
    percent_category = "0.00" if sum_income_month == 0 else str(round((sum_category_month / sum_income_month) * 100, 1))

    s, p = ELEMENT_MONTH[category["ctr_name"]]
    s.configure(text="€ " + str(sum_category_month))
    p.configure(text=str(percent_category) + " %")
