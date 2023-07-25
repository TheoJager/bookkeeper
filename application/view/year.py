from customtkinter import CTkFrame

from application.ui.elements import Elements
from application.constants import W20, CATEGORY_INCOME
from application.categories.categories import add_categories
from application.database.database_mutations import Database_Mutations
from application.database.database_categories import Database_Categories

# GLOBALS
#######################################
ELEMENT_TOTAL = {}

def create_total(append: CTkFrame):
  row = 0
  for category in Database_Categories.select():
    Elements.button_inverse(append, category["ctr_name"], add_categories, 0, row, W20, W20).configure(
      anchor="w")
    s = Elements.button_inverse(append, "€ 0.00", add_categories, 1, row, W20, W20)
    p = Elements.button_inverse(append, "0.00 %", add_categories, 2, row, W20, W20)

    s.configure(anchor="w")
    p.configure(width=100)

    ELEMENT_TOTAL[category["ctr_name"]] = [s, p]
    row += 1

  Elements.label(append, "", 0, row + 1, W20, W20)


def calculate_total():
  sum_income_year = Database_Mutations.sum_category_year(CATEGORY_INCOME)

  for category in Database_Categories.select():
    sum_category = Database_Mutations.sum_category_year(category["ctr_id"])
    percent_category = "0.00" if sum_income_year == 0 else str(round((sum_category / sum_income_year) * 100, 1))

    s, p = ELEMENT_TOTAL[category["ctr_name"]]
    s.configure(text="€ " + str(sum_category))
    p.configure(text=str(percent_category) + " %")
