import logging
import os.path
import pickle

from .cubiecube import CubieCube, moveCube, getURtoDF

log = logging.getLogger(__name__)

# Ensure pruning tables are stored in a subdirectory
cache_dir = os.path.join(os.path.dirname(__file__), 'prunetables')
if not os.path.exists(cache_dir):
    try:
        os.makedirs(cache_dir)
    except OSError:
        pass # Might exist now

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

def load_cachetable(name):
    obj = None
    try:
        with open(os.path.join(cache_dir, name + '.pkl'), 'rb') as f:
            obj = pickle.load(f)
    except (IOError, OSError) as e:
        # log.warning('could not read cache for %s: %s. Recalculating it...', name, e)
        pass
    return obj

def dump_cachetable(obj, name):
    try:
        with open(os.path.join(cache_dir, name + '.pkl'), 'wb') as f:
            pickle.dump(obj, f)
    except (IOError, OSError):
        pass

class CoordCube:
    """Representation of the cube on the coordinate level"""

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

    def __init__(self, c):
        self.twist = c.getTwist()
        self.flip = c.getFlip()
        self.parity = c.cornerParity()
        self.FRtoBR = c.getFRtoBR()
        self.URFtoDLF = c.getURFtoDLF()
        self.URtoUL = c.getURtoUL()
        self.UBtoDF = c.getUBtoDF()
        self.URtoDF = c.getURtoDF()

    def move(self, m):
        self.twist = self.twistMove[self.twist][m]
        self.flip = self.flipMove[self.flip][m]
        self.parity = self.parityMove[self.parity][m]
        self.FRtoBR = self.FRtoBR_Move[self.FRtoBR][m]
        self.URFtoDLF = self.URFtoDLF_Move[self.URFtoDLF][m]
        self.URtoUL = self.URtoUL_Move[self.URtoUL][m]
        self.UBtoDF = self.UBtoDF_Move[self.UBtoDF][m]
        if (self.URtoUL < 336 and self.UBtoDF < 336):
            self.URtoDF = self.MergeURtoULandUBtoDF[self.URtoUL][self.UBtoDF]

    # --- Static Initializers (Lazy loaded usually, but here strict) ---
    
    # twistMove
    twistMove = load_cachetable('twistMove')
    if not twistMove:
        twistMove = [[0] * N_MOVE for i in range(N_TWIST)]
        a = CubieCube()
        for i in range(N_TWIST):
            a.setTwist(i)
            for j in range(6):
                for k in range(3):
                    a.cornerMultiply(moveCube[j])
                    twistMove[i][3 * j + k] = a.getTwist()
                a.cornerMultiply(moveCube[j])
        dump_cachetable(twistMove, 'twistMove')

    # flipMove
    flipMove = load_cachetable('flipMove')
    if not flipMove:
        flipMove = [[0] * N_MOVE for i in range(N_FLIP)]
        a = CubieCube()
        for i in range(N_FLIP):
            a.setFlip(i)
            for j in range(6):
                for k in range(3):
                    a.edgeMultiply(moveCube[j])
                    flipMove[i][3 * j + k] = a.getFlip()
                a.edgeMultiply(moveCube[j])
        dump_cachetable(flipMove, 'flipMove')

    # parityMove
    parityMove = [
        [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1],
        [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    ]

    # FRtoBR_Move
    FRtoBR_Move = load_cachetable('FRtoBR_Move')
    if not FRtoBR_Move:
        FRtoBR_Move = [[0] * N_MOVE for i in range(N_FRtoBR)]
        a = CubieCube()
        for i in range(N_FRtoBR):
            a.setFRtoBR(i)
            for j in range(6):
                for k in range(3):
                    a.edgeMultiply(moveCube[j])
                    FRtoBR_Move[i][3 * j + k] = a.getFRtoBR()
                a.edgeMultiply(moveCube[j])
        dump_cachetable(FRtoBR_Move, 'FRtoBR_Move')

    # URFtoDLF_Move
    URFtoDLF_Move = load_cachetable('URFtoDLF_Move')
    if not URFtoDLF_Move:
        URFtoDLF_Move = [[0] * N_MOVE for i in range(N_URFtoDLF)]
        a = CubieCube()
        for i in range(N_URFtoDLF):
            a.setURFtoDLF(i)
            for j in range(6):
                for k in range(3):
                    a.cornerMultiply(moveCube[j])
                    URFtoDLF_Move[i][3 * j + k] = a.getURFtoDLF()
                a.cornerMultiply(moveCube[j])
        dump_cachetable(URFtoDLF_Move, 'URFtoDLF_Move')

    # URtoDF_Move
    URtoDF_Move = load_cachetable('URtoDF_Move')
    if not URtoDF_Move:
        URtoDF_Move = [[0] * N_MOVE for i in range(N_URtoDF)]
        a = CubieCube()
        for i in range(N_URtoDF):
            a.setURtoDF(i)
            for j in range(6):
                for k in range(3):
                    a.edgeMultiply(moveCube[j])
                    URtoDF_Move[i][3 * j + k] = a.getURtoDF()
                a.edgeMultiply(moveCube[j])
        dump_cachetable(URtoDF_Move, 'URtoDF_Move')

    # URtoUL_Move
    URtoUL_Move = load_cachetable('URtoUL_Move')
    if not URtoUL_Move:
        URtoUL_Move = [[0] * N_MOVE for i in range(N_URtoUL)]
        a = CubieCube()
        for i in range(N_URtoUL):
            a.setURtoUL(i)
            for j in range(6):
                for k in range(3):
                    a.edgeMultiply(moveCube[j])
                    URtoUL_Move[i][3 * j + k] = a.getURtoUL()
                a.edgeMultiply(moveCube[j])
        dump_cachetable(URtoUL_Move, 'URtoUL_Move')

    # UBtoDF_Move
    UBtoDF_Move = load_cachetable('UBtoDF_Move')
    if not UBtoDF_Move:
        UBtoDF_Move = [[0] * N_MOVE for i in range(N_UBtoDF)]
        a = CubieCube()
        for i in range(N_UBtoDF):
            a.setUBtoDF(i)
            for j in range(6):
                for k in range(3):
                    a.edgeMultiply(moveCube[j])
                    UBtoDF_Move[i][3 * j + k] = a.getUBtoDF()
                a.edgeMultiply(moveCube[j])
        dump_cachetable(UBtoDF_Move, 'UBtoDF_Move')

    # MergeURtoULandUBtoDF
    MergeURtoULandUBtoDF = load_cachetable('MergeURtoULandUBtoDF')
    if not MergeURtoULandUBtoDF:
        MergeURtoULandUBtoDF = [[0] * 336 for i in range(336)]
        for uRtoUL in range(336):
            for uBtoDF in range(336):
                MergeURtoULandUBtoDF[uRtoUL][uBtoDF] = getURtoDF(uRtoUL, uBtoDF)
        dump_cachetable(MergeURtoULandUBtoDF, 'MergeURtoULandUBtoDF')

    # Pruning Tables
    
    Slice_URFtoDLF_Parity_Prun = load_cachetable('Slice_URFtoDLF_Parity_Prun')
    if not Slice_URFtoDLF_Parity_Prun:
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
        dump_cachetable(Slice_URFtoDLF_Parity_Prun, 'Slice_URFtoDLF_Parity_Prun')

    Slice_URtoDF_Parity_Prun = load_cachetable('Slice_URtoDF_Parity_Prun')
    if not Slice_URtoDF_Parity_Prun:
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
        dump_cachetable(Slice_URtoDF_Parity_Prun, 'Slice_URtoDF_Parity_Prun')

    Slice_Twist_Prun = load_cachetable('Slice_Twist_Prun')
    if not Slice_Twist_Prun:
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
        dump_cachetable(Slice_Twist_Prun, 'Slice_Twist_Prun')

    Slice_Flip_Prun = load_cachetable('Slice_Flip_Prun')
    if not Slice_Flip_Prun:
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
        dump_cachetable(Slice_Flip_Prun, 'Slice_Flip_Prun')