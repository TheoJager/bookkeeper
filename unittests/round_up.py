import unittest

from functions import round_up

class TestDate( unittest.TestCase ):

  def test_given_number_round_up( self ):
    self.assertEqual( 1, round_up( 0.23 ) )
    self.assertEqual( 1, round_up( 0.2 ) )
    self.assertEqual( 3, round_up( 2 ) )
    self.assertEqual( 30, round_up( 23 ) )
    self.assertEqual( 300, round_up( 223 ) )
    self.assertEqual( 3000, round_up( 2123 ) )
    pass


if __name__ == '__main__':
  unittest.main()

# python -m unittest discover -s unittests -p "*.test.py" -v
# python -m unittest discover -s unittests -v
