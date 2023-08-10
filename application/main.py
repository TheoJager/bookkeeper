from screen.pennytracker import PennyTracker
from database.database_search import Database_Search
from database.database_mutations import Database_Mutations
from database.database_categories import Database_Categories

# NAME
#######################################
# PennyTracker

# PACKAGES
#######################################
# pyinstaller
# customtkinter

# COMPILE
#######################################
# pyinstaller --onedir --noconsole --clean --collect-all customtkinter --icon=application/pennytracker.png --name pennytracker --upx-dir=upx application/main.py
# pyinstaller --onefile --noconsole --clean --collect-all customtkinter --icon=application/pennytracker.png --name pennytracker --upx-dir=venv/upx application/main.py

# DATABASE SETUP
#######################################

Database_Categories.create_table_if_not_exists()
Database_Categories.create_default_records()

Database_Mutations.create_table_if_not_exists()

Database_Search.create_table_if_not_exists()

# RUN
#######################################

if __name__ == '__main__':
  PennyTracker().mainloop()
