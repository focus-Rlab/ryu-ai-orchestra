import inspect
import unittest

from gcd import gcd


class GcdTest(unittest.TestCase):
    def test_ac1_known_values(self):
        self.assertEqual(gcd(12, 18), 6)
        self.assertEqual(gcd(17, 5), 1)
        self.assertEqual(gcd(9, 9), 9)
        self.assertEqual(gcd(4, 8), 4)

    def test_ac2_commutative(self):
        self.assertEqual(gcd(12, 18), gcd(18, 12))
        self.assertEqual(gcd(17, 5), gcd(5, 17))
        self.assertEqual(gcd(9, 9), gcd(9, 9))
        self.assertEqual(gcd(4, 8), gcd(8, 4))

    def test_ac3_invalid_input_raises_value_error(self):
        with self.assertRaises(ValueError):
            gcd(0, 5)
        with self.assertRaises(ValueError):
            gcd(5, 0)
        with self.assertRaises(ValueError):
            gcd(-3, 5)
        with self.assertRaises(ValueError):
            gcd(5, -3)

    def test_ac4_signature_matches_approved_contract(self):
        sig = inspect.signature(gcd)
        params = list(sig.parameters.values())
        self.assertEqual([p.name for p in params], ["a", "b"])
        self.assertIs(params[0].annotation, int)
        self.assertIs(params[1].annotation, int)
        self.assertIs(sig.return_annotation, int)


if __name__ == "__main__":
    unittest.main()
