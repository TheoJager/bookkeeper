from typing import Dict
from tkinter import END

from customtkinter import CTkFrame, CTkTextbox, CTkComboBox, CTkLabel

from ui.message import Message
from ui.elements import Elements
from constants import W20
from functions import format_amount
from database.database_search import Database_Search
from database.database_categories import Database_Categories


class View_Search:
  ELEMENT: CTkFrame = None
  ELEMENT_PARENT: CTkFrame = None

  FORM_NAME: CTkTextbox = None
  FORM_MATCH: CTkTextbox = None
  FORM_CATEGORY: CTkComboBox = None
  FORM_TEXT: CTkTextbox = None

  COUNT: CTkLabel = 0

  @staticmethod
  def reset():
    View_Search.ELEMENT = None
    View_Search.ELEMENT_PARENT = None

    View_Search.FORM_NAME = None
    View_Search.FORM_MATCH = None
    View_Search.FORM_CATEGORY = None
    View_Search.FORM_TEXT = None

  @staticmethod
  def create_frame_headers( append: CTkFrame ) -> CTkFrame:
    frame = Elements.frame( append, 0, 1 )
    frame.configure( width = 1140, height = 50, fg_color = "transparent" )
    return frame

  @staticmethod
  def create_frame_rows( append: CTkFrame ) -> CTkFrame:
    frame = Elements.scroll( append, 0, 2 )
    frame.configure( width = 1140, height = 350, fg_color = "transparent" )
    View_Search.ELEMENT = frame
    return frame

  @staticmethod
  def create_row( append: CTkFrame, record: Dict, row: int, pady: int ):
    val1, val2, val3, val4, val5 = record
    Elements.label( append, val1, 0, row, W20, pady ).configure( width = 70 )  # date
    Elements.label( append, val2, 1, row, W20, pady ).configure( width = 5 )  # euro
    Elements.label( append, val3, 2, row, W20, pady ).configure( width = 50, anchor = "e" )  # amount

    label = Elements.label( append, val4, 3, row, W20, pady )  # description
    label.configure( wraplength = 700, width = 750 )

    if type( val5 ) is str:  # copy
      Elements.label( append, val5, 4, row, W20, pady ).configure( width = 200 )
    else:
      button = Elements.button_inverse( append, "copy", val5, 4, row, W20, 0 )
      button.configure( width = 75 )
      button.grid( sticky = "sw" )

  @staticmethod
  def create_form( append: CTkFrame ):

    row = 0

    Elements.label( append, "name", 0, row )
    Elements.label( append, "match", 1, row )
    Elements.label( append, "category", 2, row )
    Elements.label( append, "text", 3, row ).configure( width = 300 )
    Elements.button_inverse( append, "insert", View_Search.insert_record, 4, row ).grid( sticky = "sw" )

    categories = [ "== selecteer ==" ] + Database_Categories.categories()

    row += 1

    View_Search.FORM_NAME = Elements.text( append, "", 0, row, W20, 20 )
    View_Search.FORM_MATCH = Elements.text( append, "", 1, row, W20, 20 )
    View_Search.FORM_CATEGORY = Elements.select( append, categories, 2, row, W20, 20 )
    View_Search.FORM_TEXT = Elements.text( append, "", 3, row, W20, 20 )

    View_Search.FORM_NAME.configure( height = 5, fg_color = "transparent", border_width = 1 )
    View_Search.FORM_MATCH.configure( height = 5, fg_color = "transparent", border_width = 1 )
    View_Search.FORM_TEXT.configure( height = 75, width = 400, fg_color = "transparent", border_width = 1 )

    View_Search.FORM_NAME.grid( sticky = "nw" )
    View_Search.FORM_MATCH.grid( sticky = "nw" )
    View_Search.FORM_CATEGORY.grid( sticky = "nw" )
    View_Search.FORM_TEXT.grid( columnspan = 2, rowspan = 2 )

  @staticmethod
  def create_headers():
    append = View_Search.create_frame_headers( View_Search.ELEMENT_PARENT )

    View_Search.COUNT = Elements.label( append, "records : 0", 0, 0, W20, 0 )
    View_Search.update_count()

    View_Search.create_row( append,
      [ "date", "", "amount", "description", "copy to search" ],
      1, (20, 10) )

  @staticmethod
  def update_count():
    View_Search.COUNT.configure( text = "records : " + str( Database_Search.count_unsearched() ) )

  @staticmethod
  def create_records():
    append = View_Search.reset_frame_rows()

    row = 0
    for record in Database_Search.select_unsearched():
      mts_text = record[ "mts_text" ]
      data = [
        record[ "mts_date" ],
        "€", format_amount( record[ "mts_amount" ] ),
        record[ "mts_text" ],
        lambda mts_text = mts_text: View_Search.add_to_search( mts_text )
      ]

      View_Search.create_row( append, data, row, 3 )
      row += 1

  @staticmethod
  def insert_record():
    name = View_Search.FORM_NAME.get( "1.0", END ).strip()
    text = View_Search.FORM_TEXT.get( "1.0", END ).strip()
    match = View_Search.FORM_MATCH.get( "1.0", END ).strip()

    category = View_Search.FORM_CATEGORY.get()
    ctr = Database_Categories.record_by_name( category )
    ctr_id = 0 if not ctr else ctr[ 0 ][ "ctr_id" ]

    record = View_Search.validate_record( {
      "src_name" : name.upper(),
      "src_match": match.upper(),
      "src_text" : text,
      "ctr_id"   : ctr_id,
    } )

    if record:
      Database_Search.insert( record )
      View_Search.clear_form()
      View_Search.create_records()
      View_Search.update_count()

  @staticmethod
  def validate_record( record: Dict ) -> [ Dict, bool ]:
    if len( record[ "src_name" ] ) == 0:
      Message.ok( "", "Vul een naam in" )
      return False
    elif len( record[ "src_match" ] ) == 0:
      Message.ok( "", "Vul een zoekcriteria in" )
      return False
    elif record[ "ctr_id" ] == 0:
      Message.ok( "", "kies een categorie" )
      return False
    return record

  @staticmethod
  def add_to_search( value: str ):
    View_Search.FORM_TEXT.delete( '0.0', END )
    View_Search.FORM_TEXT.insert( "0.0", value )

  @staticmethod
  def clear_form():
    View_Search.FORM_NAME.delete( '0.0', END )
    View_Search.FORM_TEXT.delete( '0.0', END )
    View_Search.FORM_MATCH.delete( '0.0', END )
    View_Search.FORM_CATEGORY.set( "== selecteer ==" )

  @staticmethod
  def reset_frame_rows():
    View_Search.remove_frame( View_Search.ELEMENT )
    return View_Search.create_frame_rows( View_Search.ELEMENT_PARENT )

  @staticmethod
  def remove_frame( append: CTkFrame = None ):
    if append is not None:
      View_Search.ELEMENT = None
      append.destroy()
