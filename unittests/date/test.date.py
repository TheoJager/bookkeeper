import unittest

from application.date.date import date


class TestStringMethods(unittest.TestCase):

    def test_given_out_of_bound_dates__date__rolls_over_to_correct_date(self):
        self.assertEqual( "20080328", date( 2008, 3, 28 ) )
        self.assertEqual( "20080401", date( 2008, 3, 32 ) )
        self.assertEqual( "20090101", date( 2008, 13, 1 ) )
        self.assertEqual( "20100101", date( 2008, 25, 1 ) )
        self.assertEqual( "20090304", date( 2008, 14, 32 ) )
        self.assertEqual( "20080522", date( 2008, 2, 112 ) )
        self.assertEqual( "20100120", date( 2008, 22, 112 ) )
        self.assertEqual( "20080301", date( 2008, 2, 30 ) )
        self.assertEqual( "20000301", date( 2000, 2, 30 ) )
        self.assertEqual( "19000302", date( 1900, 2, 30 ) )
        self.assertEqual( "20080201", date( 2008, 2, 0 ) )
        self.assertEqual( "20080131", date( 2008, 2, -1 ) )
        self.assertEqual( "20080101", date( 2008, 2, -31 ) )
        self.assertEqual( "20071231", date( 2008, 2, -32 ) )
        self.assertEqual( "20081231", date( 2008, 12 + 1, -1 ) )

if __name__ == '__main__':
    unittest.main()

# python -m unittest discover -s unittests -p "*.test.py" -v
# python -m unittest discover -s unittests -v