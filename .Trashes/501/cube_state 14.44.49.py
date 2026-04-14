class CubeState:
    """
    Represents the state of the Rubik's Cube.
    """
    def __init__(self, states: list):
        # List of lists of 9 colors each, representing the 6 sides
        self.states = states

    def to_string(self) -> str:
        """
        Converts a list of 54 color initials into a Kociemba-compatible string.
        
        Expected input: ['w', 'w', 'g', 'r', ...] (total 54 elements)
        Order: U1-U9, R1-R9, F1-F9, D1-D9, L1-L9, B1-B9
        """
        if len(self.states) != 54:
            raise ValueError("The list must contain exactly 54 color values.")

        # In a Rubik's cube, the center stickers never move.
        # We use them to define which color represents which face.
        # Centers are at indices: 4(U), 13(R), 22(F), 31(D), 40(L), 49(B)
        centers = {
            self.states[4]:  'U',
            self.states[13]: 'L',
            self.states[22]: 'D',
            self.states[31]: 'R',
            self.states[40]: 'F',
            self.states[49]: 'B'
        }

        # Verify that we have 6 unique colors for the centers
        if len(centers) < 6:
            raise ValueError("Could not identify 6 unique center colors. Check your sensor data.")

        # Map each sticker color to its corresponding face notation
        try:
            kociemba_string = "".join([centers[color] for color in self.states])
            return kociemba_string
        except KeyError as e:
            return f"Error: Color {e} detected on a sticker does not match any center color."


    def is_solved(self) -> bool:
        solved_string = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
        # Note: This is a simplified check. A cube can be solved in different orientations.
        return self.to_string() == solved_string