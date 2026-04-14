class CubeState:
    """
    Represents the state of the Rubik's Cube.
    """
    def __init__(self, states: list):
        # List of lists of 9 colors each, representing the 6 sides
        self.states = states

    def is_solved(self) -> bool:
        solved_string = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
        # Note: This is a simplified check. A cube can be solved in different orientations.
        string = "".join(self.states)
        return  string == solved_string