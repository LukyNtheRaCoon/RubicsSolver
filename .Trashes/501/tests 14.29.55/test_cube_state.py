# tests/test_cube_state.py

import unittest
from cube_state import CubeState

class TestCubeState(unittest.TestCase):

    def test_init_solved_state(self):
        """
        Test initialization with a solved state.
        """
        cube = CubeState()
        expected_solved_string = "WWWWWWWWWRRRRRRRRRGGGGGGGGGYYYYYYYYYOOOOOOOOOBBBBBBBBB"
        self.assertEqual(cube.state, expected_solved_string)

    def test_init_custom_state(self):
        """
        Test initialization with a custom state string.
        """
        custom_string = "WWWWWWWWWRRRRRRRRRGGGGGGGGGYYYYYYYYYOOOOOOOOOBBBBBBBBB" # A solved-like string
        cube = CubeState(custom_string)
        self.assertEqual(cube.state, custom_string)

    def test_init_invalid_length(self):
        """
        Test initialization with an invalid length string.
        """
        with self.assertRaises(ValueError):
            CubeState("SHORT")
        with self.assertRaises(ValueError):
            CubeState("A" * 53)
        with self.assertRaises(ValueError):
            CubeState("A" * 55)

    def test_to_kociemba_string(self):
        """
        Test conversion to Kociemba string (should be direct).
        """
        solved_string = "WWWWWWWWWRRRRRRRRRGGGGGGGGGYYYYYYYYYOOOOOOOOOBBBBBBBBB"
        cube = CubeState(solved_string)
        self.assertEqual(cube.to_kociemba_string(), solved_string)

        custom_string = "OWWWWWWWWRRRRRRRRRGGGGGGGGGYYYYYYYYYOOOOOOOOOBBBBBBBBB" # Scrambled-like string, 54 chars
        cube = CubeState(custom_string)
        self.assertEqual(cube.to_kociemba_string(), custom_string)

    def test_from_kociemba_string(self):
        """
        Test creating CubeState from Kociemba string.
        """
        kociemba_str = "WWWWWWWWWRRRRRRRRRGGGGGGGGGYYYYYYYYYOOOOOOOOOBBBBBBBBB"
        cube = CubeState.from_kociemba_string(kociemba_str)
        self.assertEqual(cube.state, kociemba_str)

    def test_str_representation(self):
        """
        Test the __str__ representation for correct formatting.
        """
        cube = CubeState()
        s_repr = str(cube)
        lines = s_repr.split('\n')

        # Check Up face (first 3 lines + empty line)
        self.assertEqual(lines[0], "        WWW")
        self.assertEqual(lines[1], "        WWW")
        self.assertEqual(lines[2], "        WWW")
        self.assertEqual(lines[3], "")

        # Check middle row of faces (next 3 lines + empty line)
        # Solved: L(O) F(G) R(R) B(B)
        self.assertEqual(lines[4], "OOO GGG RRR BBB")
        self.assertEqual(lines[5], "OOO GGG RRR BBB")
        self.assertEqual(lines[6], "OOO GGG RRR BBB")
        self.assertEqual(lines[7], "")

        # Check Down face (last 3 lines)
        self.assertEqual(lines[8], "        YYY")
        self.assertEqual(lines[9], "        YYY")
        self.assertEqual(lines[10], "        YYY")

        # Check total number of lines
        self.assertEqual(len(lines), 11)

if __name__ == '__main__':
    unittest.main()
