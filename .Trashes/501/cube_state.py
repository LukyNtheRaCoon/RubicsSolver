# cube_state.py

class CubeState:
    """
    Represents the state of a 3x3 Rubik's Cube.
    The state is stored as a string of 54 characters, where each character
    represents the color of a sticker. The order of the stickers is
    consistent with Kociemba's algorithm notation (Up, Right, Front, Down, Left, Back).

    Colors are typically represented by their first letter:
    U (Up): White (W)
    R (Right): Red (R)
    F (Front): Green (G)
    D (Down): Yellow (Y)
    L (Left): Orange (O)
    B (Back): Blue (B)
    """

    def __init__(self, state_string: str = None):
        """
        Initializes the CubeState.
        If no state_string is provided, it initializes to a solved state.
        """
        if state_string is None:
            # Solved state: UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB
            # Using common color abbreviations: W R G Y O B
            # 9 Up stickers (White)
            # 9 Right stickers (Red)
            # 9 Front stickers (Green)
            # 9 Down stickers (Yellow)
            # 9 Left stickers (Orange)
            # 9 Back stickers (Blue)
            self.state = "WWWWWWWWWRRRRRRRRRGGGGGGGGGYYYYYYYYYOOOOOOOOOBBBBBBBBB"
        else:
            if len(state_string) != 54:
                raise ValueError("Cube state string must be 54 characters long.")
            self.state = state_string

    def __str__(self):
        """
        Returns a string representation of the cube state, formatted for readability.
        """
        s = self.state
        output = []

        # Up face (U) - 3x3 block
        output.append(f"        {s[0:3]}")
        output.append(f"        {s[3:6]}")
        output.append(f"        {s[6:9]}")
        output.append("") # Empty line for separation

        # Middle row: Left (L), Front (F), Right (R), Back (B)
        # Each face is a 3x3 block, displayed side-by-side
        # L: s[36:45], F: s[18:27], R: s[9:18], B: s[45:54]

        # First row of L, F, R, B
        output.append(f"{s[36:39]} {s[18:21]} {s[9:12]} {s[45:48]}")
        # Second row of L, F, R, B
        output.append(f"{s[39:42]} {s[21:24]} {s[12:15]} {s[48:51]}")
        # Third row of L, F, R, B
        output.append(f"{s[42:45]} {s[24:27]} {s[15:18]} {s[51:54]}")
        output.append("") # Empty line for separation

        # Down face (D) - 3x3 block
        output.append(f"        {s[27:30]}")
        output.append(f"        {s[30:33]}")
        output.append(f"        {s[33:36]}")

        return "\n".join(output)

    def apply_move(self, move: str) -> 'CubeState':
        """
        Applies a single Rubik's Cube move to the current state and returns a new CubeState object.
        This is a placeholder for actual cube manipulation logic.
        For a full solver, this would involve complex permutation logic for each move.
        For Kociemba, the library itself handles this internally based on its string notation.
        However, if we are to *simulate* a move or verify robot actions, we would need this.

        For simplicity, let's assume we're primarily using an external library for solving
        which takes the initial state string and returns a sequence of moves.
        We'll need to define how to interpret those moves and apply them to the robot.

        Example:
        - 'U': Turn Up face clockwise
        - 'U'': Turn Up face counter-clockwise
        - 'U2': Turn Up face 180 degrees

        For now, this method will be a stub. The primary use of this CubeState class
        will be to hold the current state and provide it to the solver, and potentially
        to visualize or verify moves.
        """
        # A real implementation would involve complex permutation logic for each sticker.
        # This is left as a future exercise if manual state manipulation is required
        # beyond what the solver library provides.
        print(f"Applying move: {move} (Not actually implemented yet in CubeState.apply_move)")
        return CubeState(self.state) # Returns current state for now

    def to_kociemba_string(self) -> str:
        """
        Converts the internal state representation to a string format expected by the Kociemba solver.
        Assuming our internal representation already matches Kociemba's standard string format.
        """
        # Ensure our internal color mapping (W, R, G, Y, O, B) matches Kociemba's convention.
        # Kociemba often uses U, R, F, D, L, B as face identifiers and then the color of the
        # face center for the stickers, e.g., 'U' for Up face color.
        # Our current `self.state` string is already in the order Up, Right, Front, Down, Left, Back.
        # So if the colors map correctly, this should be direct.
        # Standard Kociemba string format usually follows:
        # U face (9 stickers), R face (9 stickers), F face (9 stickers),
        # D face (9 stickers), L face (9 stickers), B face (9 stickers)
        # For instance, a solved cube with standard colors (White-Up, Green-Front, Red-Right)
        # might be represented as:
        # UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB
        # where 'U' here means the color of the Up face center, etc.
        # So if 'W' is Up, 'R' is Right, 'G' is Front, etc., then the string
        # "WWWWWWWWWRRRRRRRRRGGGGGGGGGYYYYYYYYYOOOOOOOOOBBBBBBBBB" is correct.
        return self.state

    @classmethod
    def from_kociemba_string(cls, kociemba_string: str) -> 'CubeState':
        """
        Creates a CubeState object from a Kociemba-style string representation.
        """
        return cls(kociemba_string)

# Example Usage:
if __name__ == "__main__":
    solved_cube = CubeState()
    print("Solved Cube:")
    print(solved_cube)

    # Example of a scrambled cube (for demonstration, not actually scrambled yet)
    # This would typically come from sensor input.
    scrambled_state_string = "WWWWWWWWRRGGGGGGGGGRRRRRRRRRYYYYYYYYYOOOOOOOOOBBBBBBBBB" # Slightly different
    scrambled_cube = CubeState(scrambled_state_string)
    print("\nScrambled Cube:")
    print(scrambled_cube)

    # Test apply_move (currently a stub)
    new_cube = solved_cube.apply_move("U")
    print("\nCube after applying 'U' (stub):")
    print(new_cube)
