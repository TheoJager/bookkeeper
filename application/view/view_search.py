from typing import Dict
from tkinter import END
from customtkinter import CTkFrame, CTkTextbox, CTkComboBox

from application.ui.message import Message
from application.ui.elements import Elements
from application.constants import W20, W10
from application.functions import format_amount
from application.database.database_search import Database_Search
from application.database.database_categories import Database_Categories


class View_Search:
  ELEMENT: CTkFrame = None
  ELEMENT_PARENT: CTkFrame = None

  FORM_NAME: CTkTextbox = None
  FORM_MATCH: CTkTextbox = None
  FORM_CATEGORY: CTkComboBox = None
  FORM_TEXT: CTkTextbox = None

  @staticmethod
  def create_frame_headers( append: CTkFrame ) -> CTkFrame:
    frame = Elements.frame( append, 0, 1 )
    frame.configure( width = 1140, height = 50, fg_color = "transparent" )
    return frame

  @staticmethod
  def create_frame_rows( append: CTkFrame ) -> CTkFrame:
    frame = Elements.scroll( append, 0, 2 )
    frame.configure( width = 1140, height = 450, fg_color = "transparent" )
    View_Search.ELEMENT = frame
    return frame

  @staticmethod
  def create_row( append: CTkFrame, record: Dict, row: int, pady: int ):
    val1, val2, val3, val4, val5 = record
    Elements.label( append, val1, 0, row, W20, pady ).configure( width = 70 )
    Elements.label( append, val2, 1, row, W20, pady ).configure( width = 5 )
    Elements.label( append, val3, 2, row, W20, pady ).configure( width = 50, anchor = "e" )

    label = Elements.label( append, val4, 3, row, W20, pady )
    label.configure( wraplength = 700 )

    if type( val5 ) is str:
      Elements.label( append, val5, 4, row, W20, pady ).configure( width = 200 )
    else:
      Elements.button( append, "copy to form", val5, 4, row, W10, pady )

  @staticmethod
  def create_form( append: CTkFrame ):

    Elements.label( append, "name", 0, 0 )
    Elements.label( append, "match", 1, 0 )
    Elements.label( append, "category", 2, 0 )
    Elements.label( append, "text", 3, 0 ).configure( width = 300 )
    Elements.button( append, "insert", View_Search.insert_record, 4, 0 )

    View_Search.FORM_NAME = Elements.text( append, "", 0, 1, W20, 20 )
    View_Search.FORM_MATCH = Elements.text( append, "", 1, 1, W20, 20 )
    View_Search.FORM_CATEGORY = Elements.select( append, Database_Categories.categories(), 2, 1, W20, 20 )
    View_Search.FORM_TEXT = Elements.text( append, "", 3, 1, W20, 20 )

    View_Search.FORM_NAME.configure( height = 5 )
    View_Search.FORM_MATCH.configure( height = 5 )
    View_Search.FORM_TEXT.configure( height = 75, width = 400 )

    View_Search.FORM_NAME.grid( sticky = "nw" )
    View_Search.FORM_MATCH.grid( sticky = "nw" )
    View_Search.FORM_CATEGORY.grid( sticky = "nw" )
    View_Search.FORM_TEXT.grid( columnspan = 2, rowspan = 2 )

  @staticmethod
  def insert_record():
    category = View_Search.FORM_CATEGORY.get()
    name = View_Search.FORM_NAME.get( "1.0", END ).strip()
    match = View_Search.FORM_MATCH.get( "1.0", END ).strip()
    text = View_Search.FORM_TEXT.get( "1.0", END ).strip()

    ctr = Database_Categories.record_by_name( category )

    if len( name ) == 0:
      Message.ok( "", "Vul een naam in" )
    elif len( match ) == 0:
      Message.ok( "", "Vul een zoekcriteria in" )
    elif len( category ) == 0:
      Message.ok( "", "kies een categorie" )

    record = {
      "src_name" : name,
      "src_match": match,
      "src_text" : text,
      "ctr_id"   : ctr[ 0 ][ "ctr_id" ],
    }
    Database_Search.insert( record )
    View_Search.clear_form()
    View_Search.create_records()

  @staticmethod
  def clear_form():
    View_Search.FORM_NAME.delete( '0.0', END )
    View_Search.FORM_MATCH.delete( '0.0', END )
    View_Search.FORM_TEXT.delete( '0.0', END )

  @staticmethod
  def create_headers():
    View_Search.create_row(
      View_Search.create_frame_headers( View_Search.ELEMENT_PARENT ),
      [ "date", "", "amount", "description", "add to search" ],
      0, (20, 10) )

  @staticmethod
  def create_records():
    append = View_Search.reset_frame_rows()

    row = 0
    # for record in Database_Mutations.select_uncategorized_year():
    for record in Database_Search.select_unsearched():
      mts_text = record[ "mts_text" ]
      data = [
        record[ "mts_date" ],
        "€",
        format_amount( record[ "mts_amount" ] ),
        record[ "mts_text" ],
        lambda mts_text = mts_text: View_Search.add_to_search( mts_text )
      ]

      View_Search.create_row( append, data, row, 3 )
      row += 1

  @staticmethod
  def add_to_search( value: str ):
    View_Search.FORM_TEXT.delete( '0.0', END )
    View_Search.FORM_TEXT.insert( "0.0", value )

  @staticmethod
  def reset_frame_rows():
    View_Search.remove_frame( View_Search.ELEMENT )
    return View_Search.create_frame_rows( View_Search.ELEMENT_PARENT )

  @staticmethod
  def remove_frame( append: CTkFrame = None ):
    if append is not None:
      append.destroy()
