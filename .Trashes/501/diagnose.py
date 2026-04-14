import sys
import os

print("--- DIAGNOSTIC START ---")
print("1. Checking Python")
print(f"Platform: {sys.platform}")
try:
    print(f"Implementation: {sys.implementation.name}")
except:
    print("Implementation: Standard (CPython)")

print("\n2. Checking Imports")
modules = ["brian", "pickle", "collections", "time", "solver_core"]
for m in modules:
    try:
        __import__(m)
        print(f"  [OK] {m}")
    except ImportError as e:
        print(f"  [FAIL] {m}: {e}")
    except Exception as e:
        print(f"  [FAIL] {m} (Error): {e}")

print("\n3. Checking Solver Core")
try:
    import simple_solver
    print("  [OK] simple_solver imported")
    print("  Testing solve (Solved Cube)...")
    try:
        # Simple solved state should return empty string
        res = simple_solver.solve("UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB")
        print(f"  [OK] Solve result: '{res}'")
    except Exception as e:
        print(f"  [FAIL] Solve execution: {e}")
        import traceback
        traceback.print_exc()

except ImportError as e:
    print(f"  [FAIL] simple_solver import: {e}")
except Exception as e:
    print(f"  [FAIL] simple_solver unknown: {e}")

print("\n--- DIAGNOSTIC END ---")
