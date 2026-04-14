import sys
# Cesta musí odpovídat tomu, jak ji vidí operační systém ROBOTA
# Pokud je to Linux (EV3/Pi), bude to pravděpodobně /media/... nebo /mnt/...
sys.path.append("/modules") # Uprav podle reálné cesty v robotovi

try:
    from rubik_solver import utils
    print("Knihovna úspěšně načtena!")
except ImportError:
    print("Knihovna nenalezena, zkontroluj sys.path")
    import os
    print(os.listdir("/")) # Koukni se, kde je tvá karta (často /mnt, /media nebo /sdcard)

# Příklad použití pro rubik-solver:
# solution = utils.solve(kociemba_string, 'KOCIEMBA')