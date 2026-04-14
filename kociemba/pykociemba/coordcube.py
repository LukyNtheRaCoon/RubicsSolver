from builtins import range
from .cubiecube import CubieCube, moveCube, getURtoDF

from builtins import range
from .cubiecube import CubieCube, moveCube, getURtoDF

def setPruning(table, index, value):
    """Set pruning value in table. Two values are stored in one byte."""
    if ((index & 1) == 0):
        table[index // 2] &= 0xf0 | value
    else:
        table[index // 2] &= 0x0f | (value << 4)

def getPruning(table, index):
    """Extract pruning value"""
    if ((index & 1) == 0):
        res = table[index // 2] & 0x0f
    else:
        res = (table[index // 2] & 0xf0) >> 4
    return res

# --- PŘESUNUTO SEM (Globální proměnné pro MicroPython) ---
N_TWIST = 2187
N_FLIP = 2048
N_SLICE1 = 495
N_SLICE2 = 24
N_PARITY = 2
N_URFtoDLF = 20160
N_FRtoBR = 11880
N_URtoUL = 1320
N_UBtoDF = 1320
N_URtoDF = 20160
N_URFtoDLB = 40320
N_URtoBR = 479001600
N_MOVE = 18
# ---------------------------------------------------------

class CoordCube(object):
    """Representation of the cube on the coordinate level"""

    # Ponecháme je i zde pro zpětnou kompatibilitu ostatních souborů
    N_TWIST = N_TWIST
    N_FLIP = N_FLIP
    N_SLICE1 = N_SLICE1
    N_SLICE2 = N_SLICE2
    N_PARITY = N_PARITY
    N_URFtoDLF = N_URFtoDLF
    N_FRtoBR = N_FRtoBR
    N_URtoUL = N_URtoUL
    N_UBtoDF = N_UBtoDF
    N_URtoDF = N_URtoDF
    N_URFtoDLB = N_URFtoDLB
    N_URtoBR = N_URtoBR
    N_MOVE = N_MOVE

    def __init__(self, c):
        """
        Generate a CoordCube from a CubieCube
        """
        self.twist = c.getTwist()
        self.flip = c.getFlip()
        self.parity = c.cornerParity()
        self.FRtoBR = c.getFRtoBR()
        self.URFtoDLF = c.getURFtoDLF()
        self.URtoUL = c.getURtoUL()
        self.UBtoDF = c.getUBtoDF()
        self.URtoDF = c.getURtoDF()     # only needed in phase2

    def move(self, m):
        """
        A move on the coordinate level
        """
        self.twist = self.twistMove[self.twist][m]
        self.flip = self.flipMove[self.flip][m]
        self.parity = self.parityMove[self.parity][m]
        self.FRtoBR = self.FRtoBR_Move[self.FRtoBR][m]
        self.URFtoDLF = self.URFtoDLF_Move[self.URFtoDLF][m]
        self.URtoUL = self.URtoUL_Move[self.URtoUL][m]
        self.UBtoDF = self.UBtoDF_Move[self.UBtoDF][m]
        if (self.URtoUL < 336 and self.UBtoDF < 336):
            self.URtoDF = self.MergeURtoULandUBtoDF[self.URtoUL][self.UBtoDF]

    # ******************************************Phase 1 move tables*****************************************************

    print('Generuji v RAM: twistMove...')
    twistMove = [[0] * N_MOVE for i in range(N_TWIST)]
    a = CubieCube()
    for i in range(N_TWIST):
        a.setTwist(i)
        for j in range(6):
            for k in range(3):
                a.cornerMultiply(moveCube[j])
                twistMove[i][3 * j + k] = a.getTwist()
            a.cornerMultiply(moveCube[j])

    print('Generuji v RAM: flipMove...')
    flipMove = [[0] * N_MOVE for i in range(N_FLIP)]
    a = CubieCube()
    for i in range(N_FLIP):
        a.setFlip(i)
        for j in range(6):
            for k in range(3):
                a.edgeMultiply(moveCube[j])
                flipMove[i][3 * j + k] = a.getFlip()
            a.edgeMultiply(moveCube[j])

    parityMove = [
        [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1],
        [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    ]

    # ***********************************Phase 1 and 2 movetable********************************************************
    
    print('Generuji v RAM: FRtoBR_Move...')
    FRtoBR_Move = [[0] * N_MOVE for i in range(N_FRtoBR)]
    a = CubieCube()
    for i in range(N_FRtoBR):
        a.setFRtoBR(i)
        for j in range(6):
            for k in range(3):
                a.edgeMultiply(moveCube[j])
                FRtoBR_Move[i][3 * j + k] = a.getFRtoBR()
            a.edgeMultiply(moveCube[j])

    print('Generuji v RAM: URFtoDLF_Move...')
    URFtoDLF_Move = [[0] * N_MOVE for i in range(N_URFtoDLF)]
    a = CubieCube()
    for i in range(N_URFtoDLF):
        a.setURFtoDLF(i)
        for j in range(6):
            for k in range(3):
                a.cornerMultiply(moveCube[j])
                URFtoDLF_Move[i][3 * j + k] = a.getURFtoDLF()
            a.cornerMultiply(moveCube[j])

    print('Generuji v RAM: URtoDF_Move...')
    URtoDF_Move = [[0] * N_MOVE for i in range(N_URtoDF)]
    a = CubieCube()
    for i in range(N_URtoDF):
        a.setURtoDF(i)
        for j in range(6):
            for k in range(3):
                a.edgeMultiply(moveCube[j])
                URtoDF_Move[i][3 * j + k] = a.getURtoDF()
            a.edgeMultiply(moveCube[j])

    print('Generuji v RAM: URtoUL_Move...')
    URtoUL_Move = [[0] * N_MOVE for i in range(N_URtoUL)]
    a = CubieCube()
    for i in range(N_URtoUL):
        a.setURtoUL(i)
        for j in range(6):
            for k in range(3):
                a.edgeMultiply(moveCube[j])
                URtoUL_Move[i][3 * j + k] = a.getURtoUL()
            a.edgeMultiply(moveCube[j])

    print('Generuji v RAM: UBtoDF_Move...')
    UBtoDF_Move = [[0] * N_MOVE for i in range(N_UBtoDF)]
    a = CubieCube()
    for i in range(N_UBtoDF):
        a.setUBtoDF(i)
        for j in range(6):
            for k in range(3):
                a.edgeMultiply(moveCube[j])
                UBtoDF_Move[i][3 * j + k] = a.getUBtoDF()
            a.edgeMultiply(moveCube[j])

    print('Generuji v RAM: MergeURtoULandUBtoDF...')
    MergeURtoULandUBtoDF = [[0] * 336 for i in range(336)]
    for uRtoUL in range(336):
        for uBtoDF in range(336):
            MergeURtoULandUBtoDF[uRtoUL][uBtoDF] = getURtoDF(uRtoUL, uBtoDF)

    # ****************************************Pruning tables for the search*********************************************
    
    print('Generuji v RAM (to potrva dele): Slice_URFtoDLF_Parity_Prun...')
    Slice_URFtoDLF_Parity_Prun = [-1] * (N_SLICE2 * N_URFtoDLF * N_PARITY // 2)
    depth = 0
    setPruning(Slice_URFtoDLF_Parity_Prun, 0, 0)
    done = 1
    while (done != N_SLICE2 * N_URFtoDLF * N_PARITY):
        for i in range(N_SLICE2 * N_URFtoDLF * N_PARITY):
            parity = i % 2
            URFtoDLF = (i // 2) // N_SLICE2
            _slice = (i // 2) % N_SLICE2
            if getPruning(Slice_URFtoDLF_Parity_Prun, i) == depth:
                for j in range(18):
                    if j in (3, 5, 6, 8, 12, 14, 15, 17):
                        continue
                    else:
                        newSlice = FRtoBR_Move[_slice][j]
                        newURFtoDLF = URFtoDLF_Move[URFtoDLF][j]
                        newParity = parityMove[parity][j]
                        if (getPruning(Slice_URFtoDLF_Parity_Prun, (N_SLICE2 * newURFtoDLF + newSlice) * 2 + newParity) == 0x0f):
                            setPruning(
                                Slice_URFtoDLF_Parity_Prun,
                                (N_SLICE2 * newURFtoDLF + newSlice) * 2 + newParity,
                                (depth + 1) & 0xff
                            )
                            done += 1
        depth += 1

    print('Generuji v RAM (to potrva dele): Slice_URtoDF_Parity_Prun...')
    Slice_URtoDF_Parity_Prun = [-1] * (N_SLICE2 * N_URtoDF * N_PARITY // 2)
    depth = 0
    setPruning(Slice_URtoDF_Parity_Prun, 0, 0)
    done = 1
    while (done != N_SLICE2 * N_URtoDF * N_PARITY):
        for i in range(N_SLICE2 * N_URtoDF * N_PARITY):
            parity = i % 2
            URtoDF = (i // 2) // N_SLICE2
            _slice = (i // 2) % N_SLICE2
            if (getPruning(Slice_URtoDF_Parity_Prun, i) == depth):
                for j in range(18):
                    if j in (3, 5, 6, 8, 12, 14, 15, 17):
                        continue
                    else:
                        newSlice = FRtoBR_Move[_slice][j]
                        newURtoDF = URtoDF_Move[URtoDF][j]
                        newParity = parityMove[parity][j]
                        if (getPruning(Slice_URtoDF_Parity_Prun, (N_SLICE2 * newURtoDF + newSlice) * 2 + newParity) == 0x0f):
                            setPruning(
                                Slice_URtoDF_Parity_Prun,
                                (N_SLICE2 * newURtoDF + newSlice) * 2 + newParity,
                                (depth + 1) & 0xff
                            )
                            done += 1
        depth += 1

    print('Generuji v RAM: Slice_Twist_Prun...')
    Slice_Twist_Prun = [-1] * (N_SLICE1 * N_TWIST // 2 + 1)
    depth = 0
    setPruning(Slice_Twist_Prun, 0, 0)
    done = 1
    while (done != N_SLICE1 * N_TWIST):
        for i in range(N_SLICE1 * N_TWIST):
            twist = i // N_SLICE1
            _slice = i % N_SLICE1
            if (getPruning(Slice_Twist_Prun, i) == depth):
                for j in range(18):
                    newSlice = FRtoBR_Move[_slice * 24][j] // 24
                    newTwist = twistMove[twist][j]
                    if (getPruning(Slice_Twist_Prun, N_SLICE1 * newTwist + newSlice) == 0x0f):
                        setPruning(Slice_Twist_Prun, N_SLICE1 * newTwist + newSlice, (depth + 1) & 0xff)
                        done += 1
        depth += 1

    print('Generuji v RAM: Slice_Flip_Prun...')
    Slice_Flip_Prun = [-1] * (N_SLICE1 * N_FLIP // 2)
    depth = 0
    setPruning(Slice_Flip_Prun, 0, 0)
    done = 1
    while (done != N_SLICE1 * N_FLIP):
        for i in range(N_SLICE1 * N_FLIP):
            flip = i // N_SLICE1
            _slice = i % N_SLICE1
            if (getPruning(Slice_Flip_Prun, i) == depth):
                for j in range(18):
                    newSlice = FRtoBR_Move[_slice * 24][j] // 24
                    newFlip = flipMove[flip][j]
                    if (getPruning(Slice_Flip_Prun, N_SLICE1 * newFlip + newSlice) == 0x0f):
                        setPruning(Slice_Flip_Prun, N_SLICE1 * newFlip + newSlice, (depth + 1) & 0xff)
                        done += 1
        depth += 1