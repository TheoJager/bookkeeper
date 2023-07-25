import locale
import datetime

from application.constants import W20
from application.ui.elements import Elements
from customtkinter import CTkFrame, CTkLabel

# SETTINGS
#######################################
locale.setlocale(locale.LC_TIME, "nl_NL")


# FUNCTIONS
#######################################
def next_month():
  global CURRENT_MONTH
  CURRENT_MONTH = 1 if CURRENT_MONTH + 1 > 12 else CURRENT_MONTH + 1
  update_month()


def previous_month():
  global CURRENT_MONTH
  CURRENT_MONTH = 12 if CURRENT_MONTH - 1 < 1 else CURRENT_MONTH - 1
  update_month()


def current_month():
  global CURRENT_MONTH
  CURRENT_MONTH = get_current_month()
  update_month()


def update_month():
  ELEMENT_CURRENT_MONTH.configure(text=create_date())


def get_current_year() -> int:
  x = datetime.datetime.now()
  return int(x.strftime("%Y"))


def get_current_month() -> int:
  x = datetime.datetime.now()
  return int(x.strftime("%m"))


def create_date():
  current_year = get_current_year()
  year = current_year if CURRENT_MONTH >= NOW_MONTH else current_year - 1

  d = datetime.date(year, CURRENT_MONTH, 1)
  return d.strftime("%B %Y")


def create_element_date(append: CTkFrame) -> str:
  global ELEMENT_CURRENT_MONTH

  current_year = get_current_year()
  year = current_year - 1 if NOW_MONTH > CURRENT_MONTH else current_year

  d = datetime.date(year, NOW_MONTH, 1)
  content = d.strftime("%B %Y")

  ELEMENT_CURRENT_MONTH = Elements.header(append, content, 0, 4, 20, (20, 10))


def create_navigation(append: CTkFrame):
  Elements.button_inverse(append, "<<", previous_month, 0, 5, W20, W20)
  Elements.button_inverse(append, "NU", current_month, 1, 5, W20, W20)
  Elements.button_inverse(append, ">>", next_month, 2, 5, W20, W20)


# GLOBALS
#######################################
CURRENT_MONTH = get_current_month()
NOW_MONTH = get_current_month()
ELEMENT_CURRENT_MONTH: CTkLabel
