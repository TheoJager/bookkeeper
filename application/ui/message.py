import ctypes  # An included library with Python install.


##  Styles:
##  0 : OK
##  1 : OK | Cancel
##  2 : Abort | Retry | Ignore
##  3 : Yes | No | Cancel
##  4 : Yes | No
##  5 : Retry | Cancel
##  6 : Cancel | Try Again | Continue

class Message:

  @staticmethod
  def box( title: str, text: str, style: int ):
    return ctypes.windll.user32.MessageBoxW( 0, text, title, style )

  @staticmethod
  def ok( title: str, text: str ):
    return Message.box( title, text, 0 )
