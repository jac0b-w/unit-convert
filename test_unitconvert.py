import unittest
import unitconvert

# https://docs.python.org/3/library/unittest.html#unittest.TestCase.debug

bot_name = unitconvert.Const.bot_name

class TestApp(unittest.TestCase):
    def test_ParseComment(self):
        result = unitconvert.ParseComment("test test testing \n\n test test "\
            f"this text is irrelevant \n{bot_name} 10  miles   to    meters m km")
        self.assertEqual(result.from_, "10 miles")
        self.assertEqual(result.to_units, ["meters", "m", "km"])

        result = unitconvert.ParseComment(f"{bot_name} 10 **2m ^2 in miles ^⁴")
        self.assertEqual(result.from_, "10**2m**2")
        self.assertEqual(result.to_units, ["miles**4"])

        result = unitconvert.ParseComment(f"{bot_name} ⅘ ⁴m^⅛ in miles **⅛ planck_lengths")
        self.assertEqual(result.from_, "0.8**4m**0.125")
        self.assertEqual(result.to_units, ["miles**0.125", "planck_lengths"])

        result = unitconvert.ParseComment(f"{bot_name} 1 TB in MB")
        self.assertEqual(result.from_, "1 TB")
        self.assertEqual(result.to_units, ["MB"])

        with self.assertRaises(unitconvert.InvalidSyntaxError):
            unitconvert.ParseComment(f"{bot_name} thisisinvalidsyntax")
            unitconvert.ParseComment(f"{bot_name} meter in miles")
            unitconvert.ParseComment(f"{bot_name} 10 **2 in miles")

    def test_format_body(self):
        ureg = unitconvert.pint.UnitRegistry(autoconvert_offset_to_baseunit=True)
        q1 = ureg("10e10m")
        q2 = (ureg("20000000miles"),ureg("-5245634664 degC"))
        self.assertEqual(unitconvert.Reply.format_body(q1,q2),"1e11 meter is:\n  - 2e07 mile\n  - -5.245635e09 degree Celsius")

        self.assertEqual(unitconvert.Reply.format_body(q1,[q2[0]]),"1e11 meter is 2e07 mile")

    def test_Reply(self):
        pass


if __name__ == '__main__':
    unittest.main()