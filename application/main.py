from application.screen.pennytracker import PennyTracker
from application.database.database_search import Database_Search
from application.database.database_mutations import Database_Mutations
from application.database.database_categories import Database_Categories

# NAME
#######################################
# PennyTracker

# PACKAGES
#######################################
# pyinstaller
# customtkinter

# COMPILE
#######################################
# pyinstaller --onefile --noconsole --icon=favicon.ico main.py

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
