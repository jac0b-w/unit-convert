import unittest
import unitconvert

# https://docs.python.org/3/library/unittest.html#unittest.TestCase.debug

class TestApp(unittest.TestCase):
    def test_ParseComment(self):
        result = unitconvert.ParseComment("test test testing \n\n test test u/unit-convert 10 miles to meters m km")
        self.assertEqual(result.from_, "10 miles")
        self.assertEqual(result.to_units, ["meters", "m", "km"])

        result = unitconvert.ParseComment(":))) u/unit-convert 1 TB in MB")
        self.assertEqual(result.from_, "1 TB")
        self.assertEqual(result.to_units, ["MB"])

        with self.assertRaises(unitconvert.InvalidSyntaxError):
            unitconvert.ParseComment("adsfjk")

    def test_format_body(self):
        ureg = unitconvert.pint.UnitRegistry(autoconvert_offset_to_baseunit=True)
        q1 = ureg("10e10m")
        q2 = (ureg("20000000miles"),ureg("-5245634664 degC"))
        self.assertEqual(unitconvert.Reply.format_body(q1,q2),"1e11 meter is:\n  - 2e07 mile\n  - -5.245635e09 degree Celsius")

        self.assertEqual(unitconvert.Reply.format_body(q1,[q2[0]]),"1e11 meter is 2e07 mile")

if __name__ == '__main__':
    unittest.main()