from solver_core import search
from solver_core import color

def solve(cubestring, patternstring=None, max_depth=24):
    """
    Solve a Rubik's cube using the local pure-Python Two-Phase algorithm.
    Wrapper for solver_core logic.
    """
    errors = {
        'Error 1': 'There is not exactly one facelet of each colour',
        'Error 2': 'Not all 12 edges exist exactly once',
        'Error 3': 'Flip error: One edge has to be flipped',
        'Error 4': 'Not all corners exist exactly once',
        'Error 5': 'Twist error: One corner has to be twisted',
        'Error 6': 'Parity error: Two corners or two edges have to be exchanged',
        'Error 7': 'No solution exists for the given maxDepth',
        'Error 8': 'Timeout, no solution within given time'
    }

    if patternstring is not None:
        cubestring = search.patternize(cubestring, patternstring)
    
    # search.Search().solution(cube, max_depth, time_out, useSeparator)
    res = search.Search().solution(cubestring, max_depth, 1000, False).strip()
    
    if res in errors:
        raise ValueError(errors[res])
    else:
        return res

if __name__ == "__main__":
    # Test
    test_state = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
    print(f"Testing Solver with solved state: {test_state}")
    try:
        # Solved state returns empty string
        sol = solve(test_state)
        print(f"Result: '{sol}'")
    except Exception as e:
        print(f"Error: {e}")

    # Superflip
    sf = "DRLUUBFBRBLURRLRUBLRDDFDLFUFUFFDBRDUBRUFLLFDDBFLUBLRBD"
    print(f"Testing Solver with Superflip: {sf}")
    try:
        sol = solve(sf)
        print(f"Result: '{sol}'")
    except Exception as e:
        print(f"Error: {e}")
