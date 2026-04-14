class CubeState:
    """
    Represents the state of the Rubik's Cube.
    """
    def __init__(self, state_string: str):
        # String format: 54 chars UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB
        self.state_string = state_string

    def __str__(self):
        return self.state_string

    def to_kociemba_string(self) -> str:
        """
        Returns the string in the format expected by Kociemba solver.
        (U R F D L B order)
        """
        return self.state_string

    def is_solved(self) -> bool:
        solved_string = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
        # Note: This is a simplified check. A cube can be solved in different orientations.
        return self.state_string == solved_string
