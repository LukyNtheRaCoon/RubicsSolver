import sys
import traceback

print(f"Python version: {sys.version}")
print(f"Platform: {sys.platform}")

print("\nAttempting to import kociemba...")
try:
    import kociemba
    print("SUCCESS: kociemba imported.")
except ImportError:
    print("FAILURE: ImportError caught.")
    traceback.print_exc()
except Exception:
    print("FAILURE: Other exception caught.")
    traceback.print_exc()

print("\nAttempting to import cffi (dependency)...")
try:
    import cffi
    print(f"SUCCESS: cffi imported from {cffi.__file__}")
except Exception:
    print("FAILURE: cffi import failed.")
    traceback.print_exc()
