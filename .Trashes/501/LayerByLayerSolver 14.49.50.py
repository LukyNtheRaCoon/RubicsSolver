import collections
from cube_state import CubeState


def rotate(state, move):
    s = list(state)
    
    # Pomocná funkce pro otočení samotné stěny (9 nálepek)
    def rotate_face(idx):
        original = s[idx:idx+9]
        # Pořadí po rotaci o 90° po směru hodinových ručiček
        s[idx+0], s[idx+1], s[idx+2] = original[6], original[3], original[0]
        s[idx+3], s[idx+4], s[idx+5] = original[7], original[4], original[1]
        s[idx+6], s[idx+7], s[idx+8] = original[8], original[5], original[2]

    if move == "U":
        rotate_face(0)
        # Přesun hran: F -> L -> B -> R -> F
        s[18],s[19],s[20], s[36],s[37],s[38], s[45],s[46],s[47], s[9],s[10],s[11] = \
        s[9],s[10],s[11], s[18],s[19],s[20], s[36],s[37],s[38], s[45],s[46],s[47]
        
    elif move == "D":
        rotate_face(27)
        # Přesun hran: F -> R -> B -> L -> F
        s[24],s[25],s[26], s[15],s[16],s[17], s[51],s[52],s[53], s[42],s[43],s[44] = \
        s[42],s[43],s[44], s[24],s[25],s[26], s[15],s[16],s[17], s[51],s[52],s[53]

    elif move == "R":
        rotate_face(9)
        # Přesun hran: U -> B -> D -> F -> U
        s[2],s[5],s[8], s[45],s[48],s[51], s[29],s[32],s[35], s[20],s[23],s[26] = \
        s[20],s[23],s[26], s[2],s[5],s[8], s[45],s[48],s[51], s[29],s[32],s[35]

    elif move == "L":
        rotate_face(36)
        # Přesun hran: U -> F -> D -> B -> U
        s[0],s[3],s[6], s[18],s[21],s[24], s[27],s[30],s[33], s[47],s[50],s[53] = \
        s[47],s[50],s[53], s[0],s[3],s[6], s[18],s[21],s[24], s[27],s[30],s[33]

    elif move == "F":
        rotate_face(18)
        # Přesun hran: U -> R -> D -> L -> U
        s[6],s[7],s[8], s[9],s[12],s[15], s[27],s[28],s[29], s[38],s[41],s[44] = \
        s[44],s[41],s[38], s[6],s[7],s[8], s[15],s[12],s[9], s[27],s[28],s[29]

    elif move == "B":
        rotate_face(45)
        # Přesun hran: U -> L -> D -> R -> U
        s[0],s[1],s[2], s[36],s[39],s[42], s[33],s[34],s[35], s[11],s[14],s[17] = \
        s[11],s[14],s[17], s[0],s[1],s[2], s[42],s[39],s[36], s[33],s[34],s[35]

    return "".join(s)
def apply_move_complex(state, move):
    if "'" in move: # Např. "U'"
        state = rotate(state, move[0])
        state = rotate(state, move[0])
        return rotate(state, move[0])
    elif "2" in move: # Např. "U2"
        state = rotate(state, move[0])
        return rotate(state, move[0])
    else:
        return rotate(state, move)
    

def is_cross_solved(state):
    """Kontroluje, zda jsou 4 bílé hrany na svých místech a lícují se středy."""
    # Indexy: 7(U-F), 5(U-R), 1(U-B), 3(U-L) musí být bílé ('w')
    # A jejich sousedé: 19(F), 10(R), 46(B), 37(L) musí lícovat se středy (22, 13, 49, 40)
    if state[7] == 'w' and state[5] == 'w' and state[1] == 'w' and state[3] == 'w':
        if state[19] == state[22] and state[10] == state[13] and \
           state[46] == state[49] and state[37] == state[40]:
            return True
    return False

# Definice hran (každá dvojice indexů tvoří jednu hranu)
EDGES = {
    'UF': (7, 19), 'UR': (5, 10), 'UB': (1, 46), 'UL': (3, 37),
    'FR': (23, 12), 'FL': (21, 41), 'BR': (48, 14), 'BL': (50, 43),
    'DF': (28, 25), 'DR': (32, 16), 'DB': (34, 52), 'DL': (30, 44)
}

# Definice rohů (každá trojice indexů tvoří jeden roh)
CORNERS = {
    'UFR': (8, 20, 9),  'URB': (2, 11, 45), 'UBL': (0, 47, 36), 'ULF': (6, 38, 18),
    'DFR': (29, 26, 15), 'DRB': (35, 17, 51), 'DBL': (33, 53, 42), 'DLF': (27, 44, 24)
}

def find_edge(state, color1, color2):
    """Najde, na kterém místě (název hrany) jsou dané dvě barvy."""
    for name, (idx1, idx2) in EDGES.items():
        current_colors = {state[idx1], state[idx2]}
        if current_colors == {color1, color2}:
            return name
    return None

def find_corner(state, color1, color2, color3):
    """Najde název rohu podle tří barev."""
    for name, (idx1, idx2, idx3) in CORNERS.items():
        current_colors = {state[idx1], state[idx2], state[idx3]}
        if current_colors == {color1, color2, color3}:
            return name
    return None

def solve_white_cross_complete(state):
    # Cílové barvy středů pro orientaci: F=Green, R=Red, B=Blue, L=Orange
    # (Předpokládáme standardní rozložení)
    target_state = list(state)
    # Nastavíme cílový stav pro kříž
    target_indices = {7:'w', 5:'w', 1:'w', 3:'w', 19:'g', 10:'r', 46:'b', 37:'o'}
    
    def check_cross(s):
        for idx, val in target_indices.items():
            if s[idx] != val: return False
        return True

    # BFS hledání
    queue = collections.deque([(state, [])])
    visited = {state}
    while queue:
        curr, path = queue.popleft()
        if check_cross(curr):
            return curr, path
        if len(path) < 7: # Kříž lze vždy složit do 7-8 tahů
            for m in ["U","D","L","R","F","B","U'","D'","L'","R'","F'","B'","U2","D2","L2","R2","F2","B2"]:
                nxt = apply_move_complex(curr, m)
                if nxt not in visited:
                    visited.add(nxt)
                    queue.append((nxt, path + [m]))
    return state, []

def solve_white_corners_complete(state):
    all_moves = []
    # Definice rohů k vyřešení (bílá + barvy dvou sousedních středů)
    corners_to_solve = [
        ('w', 'g', 'r'), # DFR
        ('w', 'r', 'b'), # DRB
        ('w', 'b', 'l'), # DBL
        ('w', 'l', 'g')  # DLF
    ]
    
    # Pro každý roh uděláme:
    for c_colors in corners_to_solve:
        # 1. Najdi kde je
        pos = find_corner(state, *c_colors)
        
        # 2. Pokud je dole, ale špatně, vykopni ho nahoru
        if pos.startswith('D'):
            # Uděláme tahy podle toho, na kterém rohu jsme
            # Pro zjednodušení: rotujeme celou kostku/indexy tak, aby roh byl vždy vpravo-vpredu
            pass 

        # 3. Otoč U, dokud není nad správným slotem (např. nad DFR)
        # 4. Aplikuj R U R' U' dokud state[29] != 'w' (bílá dole)
        while state[29] != 'w' or state[26] != state[22] or state[15] != state[13]:
            for m in ["R", "U", "R'", "U'"]:
                state = apply_move_complex(state, m)
                all_moves.append(m)
                
        # Po každém rohu otočíme kostkou (virtuálně), abychom řešili další slot
        state = apply_move_complex(state, "y") # Pomocná rotace celou kostkou
        all_moves.append("y")

    return state, all_moves

def get_edge_colors(state, edge_name):
    """Vrátí barvy na dané hraně (např. 'FR')."""
    idx1, idx2 = EDGES[edge_name]
    return state[idx1], state[idx2]

def solve_second_layer_complete(state):
    moves = []
    # Definice hran: (Barva1, Barva2) -> (Cílový střed 1, Cílový střed 2)
    # side1 je barva, která bude lícovat se středem (přední stěna)
    targets = [('g', 'r'), ('r', 'b'), ('b', 'o'), ('o', 'g')]
    
    for c1, c2 in targets:
        # --- KROK 1: Najdi, kde se hrana nachází ---
        found_pos = None
        for name in EDGES:
            colors = get_edge_colors(state, name)
            if set(colors) == {c1, c2}:
                found_pos = name
                break
        
        # --- KROK 2: Pokud je v prostřední vrstvě, ale jinde nebo špatně, vykopni ji ---
        if found_pos in ['FR', 'BR', 'BL', 'FL']:
            if found_pos != 'FR' or get_edge_colors(state, 'FR') != (c1, c2):
                # Musíme hranu vykopnout pomocí vložení "žlutého nesmyslu"
                # Pokud je v jiném slotu, musíme tam nejdřív otočit kostku 'y'
                # Zjednodušeno: Předpokládáme, že řešíme slot FR
                alg = ["R", "U", "R'", "U'", "F'", "U'", "F"]
                for m in alg:
                    state = apply_move_complex(state, m)
                    moves.append(m)
                # Po vykopnutí musíme hranu znovu najít (teď bude v 'U' vrstvě)
                continue 

        # --- KROK 3: Dostaň hranu do 'U' vrstvy a zarovnej ---
        # Otáčej 'U', dokud barva na boku hrany nelícuje s předním středem
        count = 0
        while state[23] != c1 or state[7] != c2: # Příklad pro FR slot
            state = apply_move_complex(state, "U")
            moves.append("U")
            count += 1
            if count > 4: break # Pojistka

        # --- KROK 4: Vložení (Right vs Left) ---
        # Algoritmus pro vložení z U-F do F-R:
        # U R U' R' U' F' U F
        insert_alg = ["U", "R", "U'", "R'", "U'", "F'", "U", "F"]
        for m in insert_alg:
            state = apply_move_complex(state, m)
            moves.append(m)
            
        # Pootočíme kostku pro další hranu
        state = apply_move_complex(state, "y")
        moves.append("y")

    return state, moves

def solve(self, cube_state: CubeState):
    cross_moves = solve_white_cross_complete(cube_state)
    print(f"Tahy pro kříž: {cross_moves}")

    #TODO: Implementovat vykonání tahů na robotu

    # Aktualizace stavu pro další krok
    for move in cross_moves:
        cube_string = apply_move_complex(cube_string, move)