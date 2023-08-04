import unittest

from application.date.date import date


class TestDate( unittest.TestCase ):

  def test_given_out_of_bound_dates__date__rolls_over_to_correct_date( self ):
    # up to 28th is normal
    self.assertEqual( "20080328", date( 2008, 3, 28 ) )

    # to many days and months rolls over
    self.assertEqual( "20080522", date( 2008, 2, 112 ) )
    self.assertEqual( "20100101", date( 2008, 25, 1 ) )
    self.assertEqual( "20100120", date( 2008, 22, 112 ) )

    # to many days in leapyear february rolls over over to 1st
    self.assertEqual( "20080301", date( 2008, 2, 30 ) )
    self.assertEqual( "20000301", date( 2000, 2, 30 ) )

    # to manu days in none leapyear february rolls over to 2nd
    self.assertEqual( "19000302", date( 1900, 2, 30 ) )

    # zero day adjusts to last day|month
    self.assertEqual( "20080131", date( 2008, 2, 0 ) )
    self.assertEqual( "20071201", date( 2008, 0, 1 ) )

    # -1 days is last day previous month
    self.assertEqual( "20080131", date( 2008, 2, -1 ) )
    # -1 month is last month previous year
    self.assertEqual( "20071201", date( 2008, -1, 1 ) )

    # minus previous results in 1st
    self.assertEqual( "20080101", date( 2008, 2, -31 ) )
    self.assertEqual( "20070101", date( 2008, -12, 1 ) )

    # minus previous + 1 results in 1st - 1
    self.assertEqual( "20071231", date( 2008, 2, -32 ) )
    self.assertEqual( "20061201", date( 2008, -13, 1 ) )

    # +1 month -1 day == last day current month
    self.assertEqual( "20081231", date( 2008, 12 + 1, -1 ) )

    # -1 month + days_in_month + 1
    self.assertEqual( "20080101", date( 2008, -1, 32 ) )


if __name__ == '__main__':
  unittest.main()

# python -m unittest discover -s unittests -p "*.test.py" -v
# python -m unittest discover -s unittests -v
